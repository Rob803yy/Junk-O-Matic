"""Render/validate three architecture scenes. JSON is authoritative.

Native drawio contains real editable vertex/text/edge cells, not an image.
SVG and PNG share explicit routes and text rows. Pillow measures actual text.
No PDF writer or digital-connectivity regeneration is included.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from functools import lru_cache
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/'hardware/v2/architecture'
MODEL=DIR/'architecture-model.json'
COLORS={'confirmed':'#216e4e','conflicting':'#b33a3a','proposed':'#7251a3','unknown':'#a45b00'}
INK='#243347';BG='#f8fafc';LINE=23

@lru_cache(maxsize=32)
def font(size,bold=False):
    paths=(['C:/Windows/Fonts/arialbd.ttf','/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if bold else
           ['C:/Windows/Fonts/arial.ttf','/usr/share/fonts/truetype/msttcorefonts/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for path in paths:
        if Path(path).exists():return ImageFont.truetype(path,size)
    raise RuntimeError('Arial or DejaVu Sans required for measured text layout')

def text_items(p,m):
    """Editable text rows. Coordinates are absolute top-left except local children."""
    out=[]
    def add(id,x,y,w,value,size=16,bold=False,color=INK,parent='1',local=None):
        out.append(dict(id=id,x=x,y=y,w=w,h=size+7,value=value,size=size,bold=bold,color=color,parent=parent,local=local))
    add('title',40,28,p['width']-80,p['title'],30,True)
    add('subtitle',40,76,p['width']-80,p['subtitle'],16)
    add('legend',40,114,p['width']-80,'CONFIRMED = stated scope only   |   CONFLICTING = evidence disagrees   |   PROPOSED = intent   |   UNKNOWN = insufficient evidence',15)
    for q in p['panels']:add(q['id']+'-title',q['x']+22,q['y']+20,q['w']-44,q['title'],16,True)
    for n in p['nodes']:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];c=COLORS[n['status']]
        def child(suffix,rx,ry,value,size=16,bold=False,color=INK):
            add(n['id']+'-'+suffix,x+rx,y+ry,w-28,value,size,bold,color,n['id'],[rx,ry])
        child('title',14,14,n['title'],18,True,c)
        for i,value in enumerate(n['lines']):child(f'line-{i}',14,49+i*LINE,value)
        child('basis',14,h-42,n['basis'],12,False,'#475569')
        child('status',14,h-22,n['status'].upper()+'  /  '+n['id'],11,True,c)
    for t in p['texts']:
        for i,value in enumerate(t['lines']):add(t['id']+f'-{i}',t['x'],t['y']+i*(t['size']+10),t.get('w',p['width']-t['x']-50),value,t['size'],t['bold'],t['color'])
    add('footer',40,p['height']-42,p['width']-80,f"{m['revision']} | {m['review_date']} | Editable source + SVG/PNG | PDFs HELD | Scope and evidence: architecture-model.json / README.md",14)
    return out

def route(e,nodes):
    def port(n,xy):return [n['x']+n['w']*xy[0],n['y']+n['h']*xy[1]]
    start=port(nodes[e['source']],e['source_port']);end=port(nodes[e['target']],e['target_port']);via=e['via']
    if not via and start[0]!=end[0] and start[1]!=end[1]:
        mid=(start[0]+end[0])/2;via=[[mid,start[1]],[mid,end[1]]]
    return [start]+via+[end]

def midpoint(pts):
    lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])];left=sum(lengths)/2
    for a,b,length in zip(pts,pts[1:],lengths):
        if left<=length and length:
            f=left/length;return a[0]+f*(b[0]-a[0]),a[1]+f*(b[1]-a[1]),a[0]==b[0]
        left-=length
    return *pts[-1],False

def label_rect(e,pts):
    if not e['label']:return None
    x,y,_=midpoint(pts);vertical=abs(pts[-1][0]-pts[0][0])<abs(pts[-1][1]-pts[0][1]);w=math.ceil(font(13,True).getlength(e['label']))+14
    return (x+10,y-12,w,24) if vertical else (x-w/2,y-31,w,24)

def native(p,m):
    mx=ET.Element('mxfile',host='app.diagrams.net');d=ET.SubElement(mx,'diagram',id=p['id'],name=p['title'])
    gm=ET.SubElement(d,'mxGraphModel',dx=str(p['width']),dy=str(p['height']),grid='1',gridSize='10',page='1',pageWidth=str(p['width']),pageHeight=str(p['height']),background=BG)
    root=ET.SubElement(gm,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    def vertex(parent,id,x,y,w,h,style,value=''):
        c=ET.SubElement(parent,'mxCell',id=id,value=value,style=style,vertex='1',parent='1')
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'});return c
    for q in p['panels']:vertex(root,q['id'],q['x'],q['y'],q['w'],q['h'],f"rounded=1;arcSize=4;fillColor={q['fill']};strokeColor=#d4dde7;connectable=0;")
    for n in p['nodes']:
        obj=ET.SubElement(root,'object',id=n['id'],label='',verification_status=n['status'],evidence_scope=n['basis'],evidence_ids=', '.join(n['evidence']),architecture_revision=m['revision'])
        c=vertex(obj,n['id'],n['x'],n['y'],n['w'],n['h'],f"rounded=1;arcSize=7;fillColor=#ffffff;strokeColor={COLORS[n['status']]};strokeWidth=2;recursiveResize=0;container=1;collapsible=0;")
        del c.attrib['id'] # object supplies the graph ID and editable evidence properties.
    nodes={n['id']:n for n in p['nodes']}
    for e in p['edges']:
        pts=route(e,nodes);color=COLORS[e['status']];sp,tp=e['source_port'],e['target_port']
        obj=ET.SubElement(root,'object',id=e['id'],label=e['label'],verification_status=e['status'],interface_type=e['kind'])
        c=ET.SubElement(obj,'mxCell',style=(f"edgeStyle=none;rounded=0;html=0;strokeWidth=2;strokeColor={color};dashed={int(e['status']!='confirmed')};dashPattern=7 5;"
            f"endArrow={'block' if e['arrow'] else 'none'};endFill=1;exitX={sp[0]};exitY={sp[1]};exitPerimeter=0;entryX={tp[0]};entryY={tp[1]};entryPerimeter=0;"
            f"fontFamily=Arial;fontSize=13;fontStyle=1;fontColor={color};labelBackgroundColor={BG};"),edge='1',parent='1',source=e['source'],target=e['target'])
        g=ET.SubElement(c,'mxGeometry',relative='1',x='0',y='-19',**{'as':'geometry'})
        if abs(pts[-1][0]-pts[0][0])<abs(pts[-1][1]-pts[0][1]):
            r=label_rect(e,pts);g.set('y','0')
            if r:ET.SubElement(g,'mxPoint',x=str(r[2]/2+10),y='0',**{'as':'offset'})
        if len(pts)>2:
            arr=ET.SubElement(g,'Array',**{'as':'points'})
            for x,y in pts[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    for t in text_items(p,m):
        x,y=t['local'] or [t['x'],t['y']]
        c=vertex(root,t['id'],x,y,t['w'],t['h'],f"text;html=0;align=left;verticalAlign=top;whiteSpace=nowrap;overflow=visible;spacing=0;fontFamily=Arial;fontSize={t['size']};fontStyle={int(t['bold'])};fontColor={t['color']};",t['value'])
        c.set('parent',t['parent']);c.set('connectable','0')
    ET.indent(mx)
    return '<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(mx,encoding='unicode')+'\n'

def visual(p,m):
    w,h=p['width'],p['height'];nodes={n['id']:n for n in p['nodes']};im=Image.new('RGB',(w,h),BG);draw=ImageDraw.Draw(im)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',f'<title>{escape(p["title"])}</title><desc>{escape(p["subtitle"])}. ARCH-R2; see README for scope.</desc>',f'<rect width="{w}" height="{h}" fill="{BG}"/>']
    for q in p['panels']:
        x,y,w,h=q['x'],q['y'],q['w'],q['h'];svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{q["fill"]}" stroke="#d4dde7"/>');draw.rounded_rectangle((x,y,x+w,y+h),12,fill=q['fill'],outline='#d4dde7')
    for e in p['edges']:
        pts=route(e,nodes);c=COLORS[e['status']];dashed=e['status']!='confirmed'
        svg.append(f'<polyline id="{e["id"]}" points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{c}" stroke-width="2"'+(' stroke-dasharray="7 5"' if dashed else '')+'/>')
        for a,b in zip(pts,pts[1:]):
            if not dashed:draw.line([tuple(a),tuple(b)],fill=c,width=2)
            else:
                distance=math.dist(a,b)
                if not distance:continue
                for start in range(0,math.ceil(distance),12):
                    end=min(start+7,distance)
                    points=[(a[0]+(b[0]-a[0])*v/distance,a[1]+(b[1]-a[1])*v/distance) for v in (start,end)];draw.line(points,fill=c,width=2)
        if e['arrow']:
            end=pts[-1];prev=next(q for q in reversed(pts[:-1]) if q!=end);dx,dy=end[0]-prev[0],end[1]-prev[1];length=math.hypot(dx,dy);dx/=length;dy/=length
            tri=[end,[end[0]-11*dx+5*dy,end[1]-11*dy-5*dx],[end[0]-11*dx-5*dy,end[1]-11*dy+5*dx]]
            svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in tri)+f'" fill="{c}"/>');draw.polygon([tuple(q) for q in tri],fill=c)
    for n in p['nodes']:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];c=COLORS[n['status']]
        svg.append(f'<rect id="{n["id"]}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="{c}" stroke-width="2"><title>{escape(n["basis"]+" | "+", ".join(n["evidence"]))}</title></rect>');draw.rounded_rectangle((x,y,x+w,y+h),8,fill='white',outline=c,width=2)
    def txt(x,y,value,size,color,bold,id):
        f=font(size,bold);baseline=y+f.getmetrics()[0]
        svg.append(f'<text id="{id}" x="{x}" y="{baseline}" font-family="Arial,DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')
        draw.text((x,baseline),value,font=f,fill=color,anchor='ls')
    for t in text_items(p,m):txt(t['x'],t['y'],t['value'],t['size'],t['color'],t['bold'],t['id'])
    for e in p['edges']:
        r=label_rect(e,route(e,nodes))
        if r:
            x,y,w,h=r;svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BG}"/>');draw.rectangle((x,y,x+w,y+h),fill=BG)
            txt(x+7,y+3,e['label'],13,COLORS[e['status']],True,e['id']+'-label')
    return '\n'.join(svg+['</svg>'])+'\n',im

def intersects_segment(a,b,r):
    x,y,w,h=r
    if a[0]==b[0]:return x<a[0]<x+w and max(min(a[1],b[1]),y)<min(max(a[1],b[1]),y+h)
    if a[1]==b[1]:return y<a[1]<y+h and max(min(a[0],b[0]),x)<min(max(a[0],b[0]),x+w)
    raise ValueError('Non-orthogonal route')

def overlap(a,b):
    x,y,w,h=a;X,Y,W,H=b
    return min(x+w,X+W)>max(x,X) and min(y+h,Y+H)>max(y,Y)

def validate(m):
    assert m['schema_version']==1 and len(m['pages'])==3
    assert set(m['status_definitions'])==set(COLORS);rows=[]
    for p in m['pages']:
        ids=[n['id'] for n in p['nodes']]+[e['id'] for e in p['edges']];assert len(ids)==len(set(ids))
        nodes={n['id']:n for n in p['nodes']}
        for n in nodes.values():
            assert n['status'] in COLORS and n['basis'] and n['evidence']
            for ref in n['evidence']:assert ref in m['evidence'],ref
            assert 49+(len(n['lines'])-1)*LINE+19<=n['h']-46,(n['id'],'body/basis collision')
            assert 0<=n['x'] and n['x']+n['w']<=p['width'] and n['y']+n['h']<p['height']-55
        for i,n in enumerate(p['nodes']):
            for other in p['nodes'][i+1:]:assert not overlap(tuple(n[k] for k in ('x','y','w','h')),tuple(other[k] for k in ('x','y','w','h'))),(n['id'],other['id'])
        for t in text_items(p,m):
            measured=font(t['size'],t['bold']).getlength(t['value'])
            assert measured<=t['w']+1,(p['id'],t['id'],'text too wide',round(measured),t['w'])
            assert t['y']+t['h']<=p['height'] and t['x']+measured<=p['width']-30
        for e in p['edges']:
            assert e['source'] in nodes and e['target'] in nodes and e['status'] in COLORS
            for port in (e['source_port'],e['target_port']):assert len(port)==2 and all(0<=v<=1 for v in port) and any(v in (0,1) for v in port)
            pts=route(e,nodes)
            for a,b in zip(pts,pts[1:]):
                assert a[0]==b[0] or a[1]==b[1],(e['id'],'non orthogonal')
                for n in p['nodes']:
                    assert not intersects_segment(a,b,tuple(n[k] for k in ('x','y','w','h'))),(e['id'],n['id'],'route enters node interior')
            r=label_rect(e,pts)
            if r:
                for n in p['nodes']:assert not overlap(r,tuple(n[k] for k in ('x','y','w','h'))),(e['id'],n['id'],'label overlaps node')
        xml=ET.fromstring(native(p,m));cells=xml.findall('.//mxCell');objects=xml.findall('.//object')
        cellids=[c.get('id') for c in cells if c.get('id')]+[c.get('id') for c in objects];assert len(cellids)==len(set(cellids))
        for t in text_items(p,m):
            found=next(c for c in cells if c.get('id')==t['id']);assert found.get('value')==t['value'] and found.get('parent')==t['parent']
        for e in p['edges']:
            cell=next(o for o in objects if o.get('id')==e['id']).find('mxCell')
            assert cell.get('source')==e['source'] and cell.get('target')==e['target']
            actual=[[float(q.get('x')),float(q.get('y'))] for q in cell.findall('./mxGeometry/Array/mxPoint')];assert actual==route(e,nodes)[1:-1]
        rows.append(dict(page=p['id'],nodes=len(nodes),edges=len(p['edges']),editable_text_rows=len(text_items(p,m)),result='passed'))
    input_hashes={}
    for key,ref in m['evidence'].items():
        path=ROOT/ref['path'];assert path.exists(),(key,ref['path'])
        paths=sorted(path.glob('*')) if path.is_dir() else [path]
        for item in paths:
            # These inputs are text. Normalize CRLF so the receipt survives Git checkout eol settings.
            if item.is_file():input_hashes[item.relative_to(ROOT).as_posix()]=hashlib.sha256(item.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if ref.get('record_id'):
            data=json.loads(path.read_text(encoding='utf-8'))
            def record_ids(value):
                if isinstance(value,dict):
                    yield value.get('id')
                    for v in value.values():yield from record_ids(v)
                elif isinstance(value,list):
                    for v in value:yield from record_ids(v)
            assert ref['record_id'] in set(record_ids(data)),(key,'Missing evidence record')
    import importlib.util
    spec=importlib.util.spec_from_file_location('arch_protocol',ROOT/'software/v2/raspberry_pi/protocol.py');protocol=importlib.util.module_from_spec(spec);spec.loader.exec_module(protocol)
    assert protocol.MAX_LINE_BYTES==512 and protocol.FIELDS=={'v','type','fw','seq','ms','imu_raw','echo_us','distance_mm','flags'}
    assert protocol.parse_line(b'{"v":2,"type":"telemetry","fw":"v2-r1","seq":0,"ms":0,"imu_raw":null,"echo_us":null,"distance_mm":null,"flags":5}\r\n')['flags']==5
    cfg=(ROOT/'software/v2/arduino/litterbuggy_v2/config.h').read_text()
    for token in ('#define SERIAL_BAUD 115200UL','#define SAMPLE_INTERVAL_MS 100UL','#define ENABLE_IMU 0','#define ENABLE_RANGE 0','#define ENABLE_FEEDBACK 0'):assert token in cfg,token
    power=next(p for p in m['pages'] if p['id']=='v2_power_domains');assert not any(e['source']=='PWR-U5A' for e in power['edges'])
    overview=next(p for p in m['pages'] if p['id']=='v2_system_overview')
    assert not any(e['source']=='SYS-RAILS' and e['target']=='SYS-UNO1' for e in overview['edges'])
    assert not any(e['kind']!='mechanical' and e['status']=='confirmed' for e in overview['edges'])
    pdfs=json.loads((ROOT/'docs/reconciliation/export-status.json').read_text())['held_pdfs']
    for pdf in pdfs:assert hashlib.sha256((ROOT/pdf['path']).read_bytes()).hexdigest()==pdf['sha256'],pdf['path']
    return dict(revision=m['revision'],review_date=m['review_date'],configuration_id=m['configuration_id'],scene_sha256=hashlib.sha256(MODEL.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),evidence_input_sha256_lf=input_hashes,pages=rows,held_pdf_hashes_verified=len(pdfs),
        checks=['Evidence paths / claim scopes; four verification states','Measured text width; body/basis spacing; node bounds / non-overlap',
                'Orthogonal routes; no unrelated node or label/node intersections','Native XML readback: unique IDs, editable text, endpoints / waypoints',
                'Protocol keys / default null frame / line limit / firmware defaults match source','U5A output open; Uno external power open; no confirmed electrical trace','Held PDF SHA256 values match reconciliation register'],
        limits=['Native XML and shared-scene previews checked; diagrams.net application rendering not claimed.',
                'No physical trace, measurement, hardware upload, deployment or field validation.','Digital connectivity R1 and PDFs outside regeneration scope.'])

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true',help='Validate and compare drawio/SVG without rewriting.');args=ap.parse_args()
    m=json.loads(MODEL.read_text(encoding='utf-8'));receipt=validate(m)
    for p in m['pages']:
        drawio=native(p,m);svg,im=visual(p,m)
        for suffix,value in (('.drawio',drawio),('.svg',svg)):
            path=DIR/(p['id']+suffix)
            if args.check:assert path.read_text(encoding='utf-8')==value,('Stale generated file',str(path))
            else:path.write_text(value,encoding='utf-8',newline='\n')
        if not args.check:im.save(DIR/(p['id']+'.png'))
    if not args.check:(ROOT/'reports/v2/architecture-r2-validation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
