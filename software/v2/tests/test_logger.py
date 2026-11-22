import json,sqlite3
from pathlib import Path
import pytest
from logger import Recorder,load_config,acquire_serial
from export import export
from test_protocol import encoded
CONFIG=Path(__file__).resolve().parents[1]/'raspberry_pi/config.example.yml'

def test_raw_evidence_storage_rejections_and_export(tmp_path):
    cfg=load_config(CONFIG);r=Recorder(tmp_path,cfg,'replay',CONFIG.read_bytes());r.begin_session('test')
    raw=encoded()+b'bad\n'+encoded(seq=3,ms=400)+b'partial'
    for i in range(0,len(raw),7):r.consume(raw[i:i+7])
    r.close();m=json.loads((r.run_dir/'manifest.json').read_text())
    assert m['valid_frames']==2 and m['rejected_frames']==2
    assert m['imu_samples']==m['range_samples']==0
    assert (r.run_dir/'serial.raw').read_bytes()==raw
    with sqlite3.connect(r.run_dir/'run.sqlite3') as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert db.execute("SELECT detail FROM events WHERE kind='sequence'").fetchone()[0]=='sequence_gap:2'
        assert sum(row[0] for row in db.execute('SELECT raw_length FROM frames'))==len(raw)
    export(r.run_dir,tmp_path/'export.csv');assert len((tmp_path/'export.csv').read_text().splitlines())==3
    with pytest.raises(FileExistsError):export(r.run_dir,tmp_path/'export.csv')

def test_session_boundaries_do_not_join_partial_lines(tmp_path):
    r=Recorder(tmp_path,load_config(CONFIG),'replay');r.begin_session('a');r.consume(encoded()[:20]);r.end_session('disconnect')
    r.begin_session('b');r.consume(encoded());r.close()
    with sqlite3.connect(r.run_dir/'run.sqlite3') as db:
        assert db.execute('SELECT count(*) FROM sessions').fetchone()[0]==2
        assert db.execute('SELECT count(*) FROM telemetry').fetchone()[0]==1

def test_serial_reconnect_and_shutdown_close_ports(tmp_path):
    cfg=load_config(CONFIG);cfg['serial']['port']='TEST';cfg['min_free_mb']=1
    r=Recorder(tmp_path,cfg,'serial');state={'n':0,'done':False};ports=[]
    class Port:
        def __init__(self,index):self.index=index;self.reads=0;self.closed=False
        def read(self,n):
            self.reads+=1
            if self.index==0:raise OSError('disconnect')
            state['done']=True;return encoded()
        def close(self):self.closed=True
    def factory(*args,**kw):
        p=Port(len(ports));ports.append(p);return p
    acquire_serial(r,cfg,lambda:state['done'],duration=1,serial_factory=factory);r.close()
    assert len(ports)==2 and all(p.closed for p in ports)
    with sqlite3.connect(r.run_dir/'run.sqlite3') as db:assert db.execute('SELECT count(*) FROM telemetry').fetchone()[0]==1

def test_low_disk_stops_capture(tmp_path,monkeypatch):
    cfg=load_config(CONFIG);r=Recorder(tmp_path,cfg,'serial');monkeypatch.setattr(r,'health',lambda:0)
    with pytest.raises(OSError,match='free disk'):acquire_serial(r,cfg,lambda:False,serial_factory=lambda *a,**k:None)
    r.close('failed','test low disk')

def test_invalid_config_fails_before_acquisition(tmp_path):
    import yaml
    cfg=load_config(CONFIG);cfg['serial']['timeout_s']=float('nan');p=tmp_path/'bad.yml';p.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError):load_config(p)

def test_camera_unavailable_is_recorded(tmp_path):
    from capture_video import record
    class ClosedCamera:
        def isOpened(self):return False
        def release(self):pass
    class CV:
        def VideoCapture(self,device):return ClosedCamera()
    with pytest.raises(RuntimeError,match='camera open'):record(tmp_path/'video.mp4',1,cv=CV())
    assert json.loads((tmp_path/'video.json').read_text())['status']=='failed'
