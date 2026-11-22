"""Export validated telemetry only; rejected/raw data remains in the run archive."""
import argparse,csv,sqlite3
from contextlib import closing
from pathlib import Path
def export(run_dir,output):
    uri=(Path(run_dir)/'run.sqlite3').resolve().as_uri()+'?mode=ro'
    with closing(sqlite3.connect(uri,uri=True)) as db,Path(output).open('x',newline='',encoding='utf-8') as f:
        rows=db.execute('SELECT f.id,f.session_id,f.received_utc,t.fw,t.sequence,t.uptime_ms,t.flags,t.imu_raw_json,t.echo_us,t.distance_mm FROM telemetry t JOIN frames f ON f.id=t.frame_id ORDER BY f.id')
        writer=csv.writer(f);writer.writerow([d[0] for d in rows.description]);writer.writerows(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run_dir',type=Path);p.add_argument('output',type=Path);a=p.parse_args();export(a.run_dir,a.output)
