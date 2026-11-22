#!/usr/bin/env python3
"""Single-writer serial/replay acquisition. No vehicle command writes exist."""
from __future__ import annotations
import argparse, hashlib, json, math, os, platform, shutil, signal, sqlite3, sys, time, uuid
from datetime import datetime,timezone
from pathlib import Path
import yaml
from protocol import Framer,ProtocolError,SequenceTracker,parse_line

def utc():return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

def load_config(path):
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    if type(data) is not dict or data.get('schema_version')!=1:raise ValueError('config schema_version must be 1')
    required={'schema_version','configuration_revision','output_root','serial','expected_interval_ms','health_interval_s','min_free_mb'}
    if set(data)!=required:raise ValueError('missing or unknown configuration field')
    if not isinstance(data['configuration_revision'],str) or not data['configuration_revision'].strip():raise ValueError('configuration revision required')
    if not isinstance(data['output_root'],str) or not data['output_root'].strip():raise ValueError('output_root required')
    s=data['serial']
    if type(s) is not dict or set(s)!={'port','baud','timeout_s','reconnect_s'}:raise ValueError('invalid serial configuration')
    if s['port'] is not None and (not isinstance(s['port'],str) or not s['port'].strip()):raise ValueError('invalid port')
    if type(s['baud']) is not int or s['baud']!=115200:raise ValueError('draft protocol baud must be 115200')
    for name,val,minimum in [('timeout_s',s['timeout_s'],.01),('reconnect_s',s['reconnect_s'],.1),('expected_interval_ms',data['expected_interval_ms'],60),('health_interval_s',data['health_interval_s'],.1),('min_free_mb',data['min_free_mb'],1)]:
        if type(val) not in (int,float) or not math.isfinite(val) or val<minimum:raise ValueError('invalid '+name)
    return data

class Recorder:
    def __init__(self,root,config,mode,config_bytes=b''):
        self.run_dir=Path(root)/('LB-V2-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
        self.run_dir.mkdir(parents=True,exist_ok=False)
        self.db=sqlite3.connect(self.run_dir/'run.sqlite3');self.db.executescript(Path(__file__).with_name('schema.sql').read_text())
        self.db.execute('PRAGMA synchronous=FULL')
        self.raw=(self.run_dir/'serial.raw').open('wb');self.offset=0;self.sid=None;self.tracker=SequenceTracker();self.framer=Framer();self.closed=False
        self.manifest={'protocol':2,'stage':'V2-R0 draft','configuration_revision':config['configuration_revision'],'mode':mode,'replay_is_physical_evidence':False,'started_utc':utc(),'python':platform.python_version(),'platform':platform.platform(),'config':config,'config_sha256':hashlib.sha256(config_bytes).hexdigest(),'logger_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'firmware_correspondence':'unverified','status':'running'}
        (self.run_dir/'config_snapshot.yml').write_bytes(config_bytes)
        self.save_manifest()
    def save_manifest(self):
        for k,v in self.manifest.items():self.db.execute('INSERT OR REPLACE INTO metadata VALUES (?,?)',(k,json.dumps(v,allow_nan=False)))
        self.db.commit();tmp=self.run_dir/'manifest.tmp';tmp.write_text(json.dumps(self.manifest,indent=2,allow_nan=False),encoding='utf-8');tmp.replace(self.run_dir/'manifest.json')
    def event(self,kind,detail=''):
        self.db.execute('INSERT INTO events(utc,monotonic_ns,session_id,kind,detail) VALUES (?,?,?,?,?)',(utc(),time.monotonic_ns(),self.sid,kind,str(detail)));self.db.commit()
    def begin_session(self,source):
        self.sid=self.db.execute('INSERT INTO sessions(source,started_utc) VALUES (?,?)',(source,utc())).lastrowid
        self.framer=Framer(self.offset);self.tracker=SequenceTracker();self.event('session_start',source)
    def frame(self,entry):
        start,length,raw,error=entry;sample=None
        if not error:
            try:sample=parse_line(raw)
            except ProtocolError as exc:error=str(exc)
        fid=self.db.execute('INSERT INTO frames(session_id,received_utc,received_monotonic_ns,raw_offset,raw_length,valid,error) VALUES (?,?,?,?,?,?,?)',(self.sid,utc(),time.monotonic_ns(),start,length,int(error is None),error)).lastrowid
        if sample is not None:
            self.db.execute('INSERT INTO telemetry VALUES (?,?,?,?,?,?,?,?)',(fid,sample['fw'],sample['seq'],sample['ms'],sample['flags'],None if sample['imu_raw'] is None else json.dumps(sample['imu_raw']),sample['echo_us'],sample['distance_mm']))
            anomaly=self.tracker.observe(sample)
            if anomaly:self.event('sequence',anomaly)
    def consume(self,chunk):
        if self.sid is None:raise RuntimeError('no acquisition session')
        self.raw.write(chunk);self.raw.flush();self.offset+=len(chunk)
        for entry in self.framer.feed(chunk):self.frame(entry)
        self.db.commit()
    def end_session(self,reason):
        if self.sid is None:return
        for entry in self.framer.finish():self.frame(entry)
        self.db.execute('UPDATE sessions SET ended_utc=?,end_reason=? WHERE id=?',(utc(),reason,self.sid));self.event('session_end',reason);self.sid=None
    def health(self):
        free=shutil.disk_usage(self.run_dir).free;temp=None
        try:temp=int(Path('/sys/class/thermal/thermal_zone0/temp').read_text())/1000
        except (OSError,ValueError):pass
        self.db.execute('INSERT INTO health(utc,monotonic_ns,disk_free_bytes,cpu_temp_c) VALUES (?,?,?,?)',(utc(),time.monotonic_ns(),free,temp));self.db.commit();return free
    def close(self,status='complete',error=None):
        if self.closed:return
        try:
            self.end_session(status);self.raw.flush();os.fsync(self.raw.fileno());self.raw.close()
            # Streaming hash preserves bounded memory for long field runs.
            digest=hashlib.sha256()
            with (self.run_dir/'serial.raw').open('rb') as f:
                while chunk:=f.read(65536):digest.update(chunk)
            self.manifest.update(ended_utc=utc(),status=status,error=error,raw_bytes=self.offset,raw_sha256=digest.hexdigest(),valid_frames=self.db.execute('SELECT count(*) FROM frames WHERE valid=1').fetchone()[0],rejected_frames=self.db.execute('SELECT count(*) FROM frames WHERE valid=0').fetchone()[0],imu_samples=self.db.execute('SELECT count(*) FROM telemetry WHERE imu_raw_json IS NOT NULL').fetchone()[0],range_samples=self.db.execute('SELECT count(*) FROM telemetry WHERE echo_us IS NOT NULL').fetchone()[0])
            self.save_manifest()
        finally:
            if not self.raw.closed:self.raw.close()
            self.db.close();self.closed=True

def acquire_serial(rec,config,stop,duration=None,serial_factory=None):
    if serial_factory is None:
        import serial
        serial_factory=serial.Serial
    s=config['serial'];start=time.monotonic();health_at=0.;port=None
    def ended():return stop() or (duration is not None and time.monotonic()-start>=duration)
    try:
        while not ended():
            now=time.monotonic()
            if now>=health_at:
                if rec.health()<config['min_free_mb']*1024**2:raise OSError('minimum free disk space reached')
                health_at=now+config['health_interval_s']
            if port is None:
                try:port=serial_factory(s['port'],s['baud'],timeout=s['timeout_s'])
                except (OSError,ValueError) as exc:
                    rec.event('serial_open_failed',exc)
                    until=time.monotonic()+s['reconnect_s']
                    while time.monotonic()<until and not ended():time.sleep(.05)
                    continue
                rec.begin_session(s['port']);rec.event('serial_open','DTR defaults may reset Uno; new session created')
            try:chunk=port.read(256)
            except OSError as exc:
                rec.event('serial_disconnect',exc);rec.end_session('disconnect');port.close();port=None;continue
            if chunk:rec.consume(chunk)
    finally:
        if port is not None:port.close()
        rec.end_session('acquisition_stopped')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,default=Path(__file__).with_name('config.example.yml'));p.add_argument('--replay',type=Path);p.add_argument('--output-root',type=Path);p.add_argument('--duration-seconds',type=float);a=p.parse_args(argv)
    cfg=load_config(a.config)
    if a.duration_seconds is not None and (not math.isfinite(a.duration_seconds) or a.duration_seconds<=0):p.error('duration must be positive finite seconds')
    if not a.replay and cfg['serial']['port'] is None:p.error('set verified serial port, or use --replay')
    stopping=[False]
    def stop_signal(*_):stopping[0]=True
    signal.signal(signal.SIGINT,stop_signal);signal.signal(signal.SIGTERM,stop_signal)
    root=a.output_root or Path(cfg['output_root']);rec=Recorder(root,cfg,'replay' if a.replay else 'serial',a.config.read_bytes());print(rec.run_dir,flush=True)
    try:
        if a.replay:
            rec.begin_session('replay:'+str(a.replay));rec.health()
            with a.replay.open('rb') as f:
                while not stopping[0] and (chunk:=f.read(256)):rec.consume(chunk)
            rec.end_session('replay_eof' if not stopping[0] else 'signal')
        else:acquire_serial(rec,cfg,lambda:stopping[0],a.duration_seconds)
        rec.close('stopped' if stopping[0] else 'complete');return 0
    except Exception as exc:
        try:rec.close('failed',str(exc))
        finally:print(str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':raise SystemExit(main())
