"""Review sheets rendered from tessellated FreeCAD proxy geometry."""
import json, math
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'hardware/v2/mechanical';OUT=BASE/'exports'
meshes=json.loads((OUT/'review-meshes.json').read_text())
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
    c.setFont('Helvetica-Bold',14);c.setFillColorRGB(.7,.25,.05);c.drawString(40,924,'DRAFT R0 - ALL DIMENSIONS ILLUSTRATIVE - NOT FOR FABRICATION')
    c.setFillColorRGB(.1,.15,.2);c.setFont('Helvetica',12);c.drawString(40,899,'Units: mm | Measured dimensions: UNKNOWN | Parameters editable in native FreeCAD spreadsheet')
def footer(c):
    c.setFont('Helvetica',11);c.drawString(40,30,'2026-11-21 | Proxy geometry checked in FreeCAD; fit, travel, load capacity and mounting patterns remain unverified.')
for name,objects in meshes.items():
    im=picture(objects);im.save(OUT/(name+'.png'))
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
        for i,t in enumerate(['Tub L x W x H: 820 x 500 x 270 (LAYOUT)', 'Wheelbase: 500; wheel centre spacing: 380 (LAYOUT)', 'Tyre radius: 88; width: 65 (LAYOUT)', 'Tub base Z: 285; top Z: 555 (LAYOUT)', 'Enclosure: 210 x 130 x 90 (LAYOUT)', 'Dock: 110 x 80 x 25 (LAYOUT)', 'Actual dimension cells: null in dimensions.json', 'Measure hole patterns and moving clearances first.']):c.drawString(730,430-i*30,t)
        footer(c);c.showPage()
        title(c,name+' / service layout')
        pic=picture([o for o in objects if o['name']!='CartTub'])
        c.drawImage(ImageReader(pic),40,240,width=1320,height=630,preserveAspectRatio=True,anchor='c')
        c.setFont('Helvetica',14);c.drawString(40,180,'Tub hidden for review: rails, coilover envelopes, metal support, enclosure, dock and sensor bracket.')
        c.drawString(40,150,'All shown placements remain illustrative; no current-build interference or structural conclusion is claimed.')
        footer(c);c.showPage()
    c.save()
print('Five rendered mechanical PDFs/PNGs; assembly includes orthographic reference views.')
