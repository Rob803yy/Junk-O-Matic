"""Reproducible software and artifact checks; no upload or hardware interaction."""
import argparse,hashlib,json,subprocess,sys,tempfile,sqlite3
from pathlib import Path
from contextlib import closing
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'reports/v2';OUT.mkdir(parents=True,exist_ok=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('--arduino-cli',required=True);args=p.parse_args();results=[]
    def command(name,cmd,expect_success=True,expected_text=None):
        r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        # Redact local home paths from portable public validation receipts.
        receipt=(r.stdout+r.stderr).replace(str(Path.home()),'<USER_HOME>').replace(str(ROOT),'<REPOSITORY>')
        (OUT/(name+'.txt')).write_text(receipt,encoding='utf-8')
        passed=(r.returncode==0) if expect_success else (r.returncode!=0 and expected_text in receipt)
        results.append({'check':name,'passed':passed,'exit_code':r.returncode,'receipt':name+'.txt'})
        if not passed:raise RuntimeError(name+' failed: '+receipt)
    command('python-tests',[sys.executable,'-m','pytest','software/v2/tests','-q'])
    with tempfile.TemporaryDirectory(prefix='litterbuggy-v2-') as temp:
        for name,flags,success in [('uno-default','',True),('uno-drivers-feedback','-DENABLE_IMU=1 -DENABLE_RANGE=1 -DRANGE_PROFILE=1 -DENABLE_FEEDBACK=1 -DTRIG_PIN=6 -DECHO_PIN=7 -DLED_PIN=8 -DBUZZER_PIN=9 -DALARM_DISTANCE_MM=200',True),('uno-reject-unassigned-pins','-DENABLE_RANGE=1',False)]:
            cmd=[args.arduino_cli,'compile','--fqbn','arduino:avr:uno','--build-path',str(Path(temp)/name)]
            if flags:cmd+=['--build-property','compiler.cpp.extra_flags='+flags]
            command(name,cmd+['software/v2/arduino/litterbuggy_v2'],success,'Review and assign separate digital trigger/echo pins')
        command('replay-cli',[sys.executable,'software/v2/raspberry_pi/logger.py','--replay','software/v2/tests/fixtures/disabled.ndjson','--output-root',str(Path(temp)/'runs')])
        command('uno-reject-uart-as-trigger-echo',[args.arduino_cli,'compile','--fqbn','arduino:avr:uno','--build-path',str(Path(temp)/'reject-uart'),'--build-property','compiler.cpp.extra_flags=-DENABLE_RANGE=1 -DRANGE_PROFILE=2 -DTRIG_PIN=6 -DECHO_PIN=7','software/v2/arduino/litterbuggy_v2'],False,'A02YYUW UART is not implemented')
        run=next((Path(temp)/'runs').iterdir());m=json.loads((run/'manifest.json').read_text());assert m['valid_frames']==2 and m['range_samples']==m['imu_samples']==0 and m['mode']=='replay'
        with closing(sqlite3.connect(run/'run.sqlite3')) as db:assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert (run/'serial.raw').read_bytes()==(ROOT/'software/v2/tests/fixtures/disabled.ndjson').read_bytes()
        results.append({'check':'replay-raw-database-manifest','passed':True})
    for ext in ['drawio','qet']:
        fs=list((ROOT/'hardware/v2').rglob('*.'+ext));assert fs
        for f in fs:ET.parse(f)
        results.append({'check':ext+'-xml','passed':True,'files':len(fs)})
    held=json.loads((ROOT/'docs/reconciliation/export-status.json').read_text())
    for pdf in held['held_pdfs']:
        assert hashlib.sha256((ROOT/pdf['path']).read_bytes()).hexdigest()==pdf['sha256'],pdf['path']
    results.append({'check':'prior-pdf-bytes-unchanged','passed':True,'files':len(held['held_pdfs'])})
    summary={'revision':'V2-R1','review_date':'2026-11-21','checks':results,'limits':['No hardware upload or sensor bench test','No measured mechanical dimensions or physical fit validation','No electrical polarity/rating/continuity verification','Systemd and real camera not exercised on Pi','PDF regeneration deferred pending owner review']}
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
