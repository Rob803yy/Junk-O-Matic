"""Optional USB/OpenCV camera capture. Separate from serial acquisition."""
import argparse,json,time
from datetime import datetime,timezone
from pathlib import Path
def record(output,seconds,device=0,cv=None):
    if cv is None:import cv2 as cv
    output=Path(output)
    if output.exists() or output.with_suffix('.json').exists():raise FileExistsError(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();cap=None;writer=None;frames=0
    metadata={'started_utc':datetime.now(timezone.utc).isoformat(),'status':'failed','frames':0,'synchronization':'unverified; not sensor sample timestamps'}
    try:
        cap=cv.VideoCapture(device)
        if not cap.isOpened():raise RuntimeError('camera open failed')
        ok,frame=cap.read()
        if not ok:raise RuntimeError('camera first frame failed')
        h,w=frame.shape[:2];fps=float(cap.get(cv.CAP_PROP_FPS))
        if not 1<=fps<=240:fps=30.;metadata['fps_assumed']=True
        metadata.update(width=w,height=h,writer_fps=fps)
        writer=cv.VideoWriter(str(output),cv.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
        if not writer.isOpened():raise RuntimeError('video writer open failed')
        while time.monotonic()-start<seconds:
            if frame.shape[:2]!=(h,w):raise RuntimeError('camera frame dimensions changed')
            writer.write(frame);frames+=1;ok,frame=cap.read()
            if not ok:raise RuntimeError('camera frame read failed')
        if frames==0:raise RuntimeError('no frames recorded')
        metadata['status']='complete'
    except BaseException as exc:metadata['error']=str(exc);raise
    finally:
        if writer is not None:writer.release()
        if cap is not None:cap.release()
        metadata.update(frames=frames,elapsed_s=time.monotonic()-start,ended_utc=datetime.now(timezone.utc).isoformat())
        output.with_suffix('.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    return metadata
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);p.add_argument('--seconds',type=float,required=True);p.add_argument('--device',type=int,default=0);a=p.parse_args()
    if not 0<a.seconds<86400:p.error('seconds must be finite and within 0..86400')
    print(json.dumps(record(a.output,a.seconds,a.device),indent=2))
