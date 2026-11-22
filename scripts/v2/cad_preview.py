"""Render photo-review sheets from exported native CAD meshes. No PDFs."""
import json,math,base64,io,sys
from pathlib import Path
from html import escape
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'hardware/v2/mechanical';OUT=BASE/'exports'
M=json.loads((OUT/'review-meshes.json').read_text());D=json.loads((BASE/'dimensions.json').read_text())
if '--pdf' in sys.argv:raise SystemExit('PDF generation is held pending owner content review.')
def font(size,bold=False):
    for name in [('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'),'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if Path(name).exists():return ImageFont.truetype(name,size)
    return ImageFont.load_default()
def project(v,view):
    x,y,z=v
    if view=='top':return x,-y,z
    if view=='side':return x,-z,-y
    if view=='front':return y,-z,x
    if view=='opposite':return (y-x)*.7071068,(x+y)*.3535534-z*.8660254,(x+y)*.6123724+z*.5
    return (x+y)*.7071068,(x-y)*.3535534-z*.8660254,(x-y)*.6123724+z*.5
def picture(objects,view='iso',size=(1600,900)):
    allp=[project(v,view) for o in objects for v in o['vertices']]
    lo=[min(p[i] for p in allp) for i in range(2)];hi=[max(p[i] for p in allp) for i in range(2)]
    scale=min((size[0]-90)/max(1,hi[0]-lo[0]),(size[1]-90)/max(1,hi[1]-lo[1]));ox=(size[0]-(hi[0]-lo[0])*scale)/2;oy=(size[1]-(hi[1]-lo[1])*scale)/2
    def pix(p):return ox+(p[0]-lo[0])*scale,oy+(p[1]-lo[1])*scale
    rgb=np.full((size[1],size[0],3),[245.,247.,249.]);depth=np.full((size[1],size[0]),-np.inf)
    triangles=[]
    for o in objects:
        vs=o['vertices'];ps=[project(v,view) for v in vs];alpha=o.get('opacity',1.)
        for tri in o['triangles']:
            a,b,c=[np.array(vs[i]) for i in tri];n=np.cross(b-a,c-a);norm=np.linalg.norm(n) or 1
            shade=.60+.40*abs(np.dot(n,[-.25,-.45,.86])/norm);color=np.array(o['color'])*255*shade
            triangles.append((alpha,sum(ps[i][2] for i in tri)/3,[pix(ps[i]) for i in tri],[ps[i][2] for i in tri],color))
    # Opaque first; translucent facets afterwards, far-to-near without obscuring opaque geometry behind them.
    triangles.sort(key=lambda t:(t[0]<.999,t[1] if t[0]<.999 else 0))
    for alpha,mean,pp,zz,color in triangles:
        (x0,y0),(x1,y1),(x2,y2)=pp;den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(den)<1e-8:continue
        lx=max(0,int(min(x for x,y in pp)));hx=min(size[0]-1,int(max(x for x,y in pp))+1);ly=max(0,int(min(y for x,y in pp)));hy=min(size[1]-1,int(max(y for x,y in pp))+1)
        if hx<lx or hy<ly:continue
        xx,yy=np.meshgrid(np.arange(lx,hx+1),np.arange(ly,hy+1));aa=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den;bb=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den;cc=1-aa-bb
        z=aa*zz[0]+bb*zz[1]+cc*zz[2];old=depth[ly:hy+1,lx:hx+1];mask=(aa>=-1e-6)&(bb>=-1e-6)&(cc>=-1e-6)&(z>old)
        sub=rgb[ly:hy+1,lx:hx+1];sub[mask]=sub[mask]*(1-alpha)+color*alpha
        if alpha>=.999:old[mask]=z[mask]
    return Image.fromarray(np.clip(rgb,0,255).astype('uint8'))
def sheet(name,objects):
    assembly=name=='v2_assembly';image=Image.new('RGB',(1800,1450),'white');draw=ImageDraw.Draw(image);labels=[];frames=[]
    def label(pos,t,font,fill):
        draw.text(pos,t,font=font,fill=fill);labels.append((pos,t,font.size,fill))
    def panel(im,pos):image.paste(im,pos);frames.append((im,pos))
    title='V2 assembly / photo review' if assembly else name.replace('v2_','').replace('_',' ')
    if name=='v2_sensor_mounts':title='Front lighting / reserved sensor interface'
    label((45,26),'LitterBuggy  |  '+title,font=font(32,True),fill='#203c54')
    label((45,75),'CAD-R2  |  +X = yellow-handle FRONT  |  bucket omitted by owner' if assembly else 'CAD-R2  |  component local frame  |  assembly front = yellow-handle end',font=font(21,True),fill='#203c54')
    label((45,110),'PHOTO-INFORMED SHAPE / PLACEMENT  —  NUMERIC DIMENSIONS UNMEASURED',font=font(21),fill='#a65d00')
    hero=picture(objects,'iso',(1710,800));panel(hero,(45,150));label((60,160),'ENCLOSURE-SIDE OBLIQUE' if assembly else 'COMPONENT LOCAL VIEW',font=font(18,True),fill='#203c54')
    if assembly:
        for view,x,caption in [('opposite',45,'OPPOSITE-SIDE OBLIQUE'),('side',635,'ENCLOSURE SIDE / +X FRONT →'),('front',1225,'FRONT / LOOKING TOWARD -X')]:
            panel(picture(objects,view,(530,310)),(x,980));label((x,1295),caption,font=font(17,True),fill='#203c54')
    else:
        for i,t in enumerate(['Appearance is reconstructed from CAD-P01/P02/P03; exact sections, holes and fasteners remain open.','Enclosure internals, battery identity and sensor fitting are not inferred from these photos.','Native document: editable Parameters, component groups and constrained profiles. STEP: visible geometry only.']):label((45,1000+i*38),t,font=font(20),fill='#33485a')
    label((45,1340),'Source catalog enclosure size is unverified. Proportions, tilt and cosmetic details are layout choices.',font=font(20),fill='#33485a')
    label((45,1380),'CAD-R2  |  Geometry checks do not establish physical fit, load capacity or fabrication dimensions.  |  PDFs held.',font=font(19),fill='#33485a')
    image.save(OUT/(name+'.png'))
    # SVG retains editable annotation text, with native geometry raster preview embedded.
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1450" viewBox="0 0 1800 1450"><rect width="1800" height="1450" fill="white"/>']
    for im,(x,y) in frames:
        buf=io.BytesIO();im.save(buf,format='PNG');data=base64.b64encode(buf.getvalue()).decode();svg.append(f'<image x="{x}" y="{y}" width="{im.width}" height="{im.height}" href="data:image/png;base64,{data}"/>')
    for (x,y),t,size,color in labels:svg.append(f'<text x="{x}" y="{y+size}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{escape(t)}</text>')
    svg.append('</svg>');(OUT/(name+'.svg')).write_text('\n'.join(svg),encoding='utf-8')
    return image
for name,objects in M.items():
    sheet(name,objects)
    if name=='v2_assembly':
        picture(objects,'iso',(1800,1100)).save(OUT/'v2_assembly_iso.png')
        picture(objects,'opposite',(1600,1000)).save(OUT/'v2_assembly_opposite.png')
        picture(objects,'front',(1200,1000)).save(OUT/'v2_assembly_front.png')
        # Service view: explicit hiding of cart/accessories reveals unresolved supports; no new physical fit claim.
        hidden=('CartTub','RolledRim','FloorRib','StripHousing','RedStrip','MoldedEndPanel','Yellow','HandleArm')
        picture([o for o in objects if not o['name'].startswith(hidden)],'iso',(1600,1000)).save(OUT/'v2_assembly_tub_hidden.png')
    print('Rendered',name,flush=True)
print('CAD-R2 sheets/oblique/front/service previews complete; no PDFs generated.')
