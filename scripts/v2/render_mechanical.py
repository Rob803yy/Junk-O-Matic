"""Review sheets rendered from tessellated FreeCAD proxy geometry."""
import json, math,sys,base64
from html import escape
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'hardware/v2/mechanical';OUT=BASE/'exports'
meshes=json.loads((OUT/'review-meshes.json').read_text())
CFG=json.loads((BASE/'dimensions.json').read_text())
def project(v,view='iso'):
    x,y,z=v
    if view=='top':return x,-y,z
    if view=='side':return x,-z,y
    if view=='front':return y,-z,x
    return (x-y)*.866,(x+y)*.5-z,x+y+z
def picture(objects,view='iso',size=(1800,1000)):
    allp=[project(v,view) for o in objects for v in o['vertices']]
    lo=[min(p[i] for p in allp) for i in range(2)];hi=[max(p[i] for p in allp) for i in range(2)]
    scale=min((size[0]-60)/(hi[0]-lo[0]),(size[1]-60)/(hi[1]-lo[1]))
    ox=(size[0]-(hi[0]-lo[0])*scale)/2;oy=(size[1]-(hi[1]-lo[1])*scale)/2
    def pix(p):return ox+(p[0]-lo[0])*scale,oy+(p[1]-lo[1])*scale
    tris=[]
    for obj in objects:
        vs=obj['vertices'];ps=[project(v,view) for v in vs]
        for t in obj['triangles']:
            a,b,c=[vs[i] for i in t];u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
            n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];norm=math.sqrt(sum(k*k for k in n)) or 1
            shade=.68+.30*abs(sum(n[i]*[.3,-.4,.85][i] for i in range(3))/norm)
            color=tuple(min(255,int(255*c*shade)) for c in obj['color'])
            tris.append((sum(ps[i][2] for i in t)/3,[pix(ps[i]) for i in t],color))
    # Depth buffer avoids painter-order artefacts inside the hollow tub.
    rgb=np.full((size[1],size[0],3),[244,246,248],dtype=np.uint8)
    depthbuf=np.full((size[1],size[0]),-np.inf)
    for obj in objects:
        vs=obj['vertices'];ps=[project(v,view) for v in vs]
        for t in obj['triangles']:
            pp=[pix(ps[i]) for i in t];(x0,y0),(x1,y1),(x2,y2)=pp
            den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(den)<1e-8:continue
            lx=max(0,int(min(x for x,y in pp)));hx=min(size[0]-1,int(max(x for x,y in pp))+1)
            ly=max(0,int(min(y for x,y in pp)));hy=min(size[1]-1,int(max(y for x,y in pp))+1)
            xx,yy=np.meshgrid(np.arange(lx,hx+1),np.arange(ly,hy+1))
            aa=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den
            bb=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den;cc=1-aa-bb
            z=aa*ps[t[0]][2]+bb*ps[t[1]][2]+cc*ps[t[2]][2]
            old=depthbuf[ly:hy+1,lx:hx+1];mask=(aa>=-1e-6)&(bb>=-1e-6)&(cc>=-1e-6)&(z>old)
            a,b,c=[vs[i] for i in t];u=np.subtract(b,a);v=np.subtract(c,a);n=np.cross(u,v);norm=np.linalg.norm(n) or 1
            shade=.68+.3*abs(np.dot(n,[.3,-.4,.85])/norm);col=[min(255,int(255*c*shade)) for c in obj['color']]
            old[mask]=z[mask];rgb[ly:hy+1,lx:hx+1][mask]=col
    return Image.fromarray(rgb)
def title(c,name):
    c.setFont('Helvetica-Bold',25);c.drawString(40,953,'LitterBuggy V2 / '+name.replace('v2_','').replace('_',' '))
    c.setFont('Helvetica-Bold',14);c.setFillColorRGB(.7,.25,.05);c.drawString(40,924,'DRAFT R1 - LAYOUT / SOURCE SPECS UNVERIFIED - NOT FOR FABRICATION')
    c.setFillColorRGB(.1,.15,.2);c.setFont('Helvetica',12);c.drawString(40,899,'Units: mm | Measured dimensions: UNKNOWN | Parameters editable in native FreeCAD spreadsheet')
def footer(c):
    c.setFont('Helvetica',11);c.drawString(40,30,'2026-11-21 | Proxy geometry checked in FreeCAD; fit, travel, load capacity and mounting patterns remain unverified.')
for name,objects in meshes.items():
    im=picture(objects);im.save(OUT/(name+'.png'))
    # Source sheets are SVG/PNG by default. PDF generation requires a later explicit request.
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1200" viewBox="0 0 1400 1200"><rect width="1400" height="1200" fill="white"/>']
    def text(x,y,t,size=16,color='#203c54'):
        svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{escape(t)}</text>')
    text(40,45,'LitterBuggy V2 / '+name.replace('v2_','').replace('_',' '),28)
    text(40,80,'R1 - NOT FOR FABRICATION | Measured dimensions UNKNOWN | Geometry is a review proxy',18,'#a65200')
    text(40,110,'Enclosure: nominal source spec only. Other dimensions: illustrative layout. No released payload or clearance.',15)
    svg.append(f'<image x="40" y="130" width="1320" height="650" href="data:image/png;base64,{base64.b64encode((OUT/(name+".png")).read_bytes()).decode()}"/>')
    if name=='v2_assembly':
        import io
        for i,view in enumerate(['top','side','front']):
            pic=picture(objects,view,(600,280));buf=io.BytesIO();pic.save(buf,format='PNG')
            svg.append(f'<image x="{40+i*450}" y="780" width="420" height="190" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>')
            text(40+i*450,990,view.upper()+' / ILLUSTRATIVE',14)
    else:
        text(40,820,'Component relationships follow historical descriptions; placements are proposed.',18)
        text(40,850,'Historical HC-SR04 profile is shown; S06 reports that sensor lost. Replacement mount remains open.',17)
        text(40,880,'No new cradle, trailer, dual-bin sorter or intake mechanism has been adopted as existing hardware.',17)
    for i,line in enumerate(['Units: mm. Cart layout 820 x 500 x 270; wheelbase 500; wheel centres 380. These are NOT measured.',
        'Enclosure envelope 292.1 x 190.5 x 129.54: source-listed 11.5 x 7.5 x 5.1 inches (S04 V1.0 C16), NOT verified fit.',
        'Dock layout 110 x 80 x 25. Mount holes, latch clearances, steering/suspension travel and load capacity UNKNOWN.',
        'Editable parameters: native FreeCAD Parameters sheet / dimensions.json. STEP is geometry only; provenance is in native files.',
        '2026-11-21 | CFG-V2-R1 | Physical inspection and technical review pending; PDFs held for owner review.']):text(40,1040+i*28,line,15)
    svg.append('</svg>');(OUT/(name+'.svg')).write_text('\n'.join(svg),encoding='utf-8')
    if '--pdf' not in sys.argv:continue
    c=Canvas(str(OUT/(name+'.pdf')),pagesize=(1400,1000));title(c,name);c.drawImage(ImageReader(im),40,255,width=1320,height=630,preserveAspectRatio=True,anchor='c')
    lines=['Geometry reconstructs component relationships from historical photos; proportions are layout choices.',
           'No mounting holes, material strength, tolerances, release clearances or electrical interfaces are certified.',
           'Colours: dark = chassis/tub/tyres; silver = support; blue = dock; orange = enclosure; green = boards.',
           'Enclosure, dock and sensor positions are proposed. Raised cart/support relationship follows photos.']
    for i,t in enumerate(lines):c.setFont('Helvetica',14);c.drawString(40,210-i*26,t)
    footer(c);c.showPage()
    if name=='v2_assembly':
        title(c,name+' / reference views')
        for view,x,y in [('top',40,500),('side',730,500),('front',40,135)]:
            pic=picture(objects,view,(1000,460));c.drawImage(ImageReader(pic),x,y,width=620,height=285);c.setFont('Helvetica-Bold',14);c.drawString(x,y+300,view.upper()+' - ILLUSTRATIVE')
        c.setFont('Helvetica',14)
        for i,t in enumerate(['Tub L x W x H: 820 x 500 x 270 (LAYOUT)', 'Wheelbase: 500; wheel centre spacing: 380 (LAYOUT)', 'Tyre radius: 88; width: 65 (LAYOUT)', 'Tub base Z: 285; top Z: 555 (LAYOUT)', 'Enclosure: 292.1 x 190.5 x 129.54 (SOURCE SPEC)', 'Dock: 110 x 80 x 25 (LAYOUT)', 'Actual dimension cells: null in dimensions.json', 'Measure hole patterns and moving clearances first.']):c.drawString(730,430-i*30,t)
        footer(c);c.showPage()
        title(c,name+' / service layout')
        pic=picture([o for o in objects if o['name']!='CartTub'])
        c.drawImage(ImageReader(pic),40,240,width=1320,height=630,preserveAspectRatio=True,anchor='c')
        c.setFont('Helvetica',14);c.drawString(40,180,'Tub hidden for review: rails, coilover envelopes, metal support, enclosure, dock and sensor bracket.')
        c.drawString(40,150,'All shown placements remain illustrative; no current-build interference or structural conclusion is claimed.')
        footer(c);c.showPage()
    c.save()
print('Five mechanical SVG sheets and PNGs generated; PDF generation '+('requested' if '--pdf' in sys.argv else 'held'))
