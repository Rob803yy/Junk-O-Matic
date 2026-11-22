"""Generate editable diagrams and review exports from the same scene geometry."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
import textwrap
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[2]
W,H=1500,1000
COLORS={'confirmed':'#216e4e','unknown':'#b26a00','proposed':'#7251a3','historical':'#3978a8'}

class Page:
    def __init__(self,title,subtitle):
        self.title,self.subtitle=title,subtitle; self.boxes=[]; self.edges=[]; self.notes=[]
    def box(self,id,x,y,w,h,title,lines,status='unknown'):
        self.boxes.append(dict(id=id,x=x,y=y,w=w,h=h,title=title,lines=lines,status=status)); return id
    def edge(self,a,b,label,kind='unknown'):
        self.edges.append(dict(a=a,b=b,label=label,status=kind))
    def note(self,x,y,text):self.notes.append((x,y,text))

def render(page,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    model=ET.Element('mxGraphModel',dx='1500',dy='1000',grid='1',gridSize='10',page='1',pageWidth=str(W),pageHeight=str(H))
    root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1500" height="1000" fill="#f5f7fa"/>']
    pdf=Canvas(str(path.with_suffix('.pdf')),pagesize=(W,H))
    pdf.setFillColor(HexColor('#f5f7fa'));pdf.rect(0,0,W,H,fill=1,stroke=0)
    def txt(x,y,text,size=15,color='#243347',bold=False):
        svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(text)}</text>')
        pdf.setFont('Helvetica-Bold' if bold else 'Helvetica',size);pdf.setFillColor(HexColor(color));pdf.drawString(x,H-y,text)
    def textcell(id,x,y,w,h,text,size):
        c=ET.SubElement(root,'mxCell',id=id,value=text,style=f'text;html=0;align=left;verticalAlign=top;fontSize={size};',vertex='1',parent='1');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'})
    txt(40,48,page.title,28,bold=True);txt(40,78,page.subtitle,15)
    textcell('title',40,20,1420,40,page.title,28);textcell('sub',40,60,1420,30,page.subtitle,15)
    lookup={b['id']:b for b in page.boxes}
    for n,e in enumerate(page.edges):
        a,b=lookup[e['a']],lookup[e['b']]
        if b['x']>=a['x']+a['w']:
            x1,y1=a['x']+a['w'],a['y']+a['h']/2;x2,y2=b['x'],b['y']+b['h']/2
        else:x1,y1=a['x']+a['w']/2,a['y']+a['h'];x2,y2=b['x']+b['w']/2,b['y']
        color=COLORS[e['status']]; dash=e['status']!='confirmed'
        mid=(x1+x2)/2; pts=[(x1,y1),(mid,y1),(mid,y2),(x2,y2)]
        svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="2"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
        pdf.setStrokeColor(HexColor(color));pdf.setLineWidth(2);pdf.setDash([7,5] if dash else [])
        p=pdf.beginPath();p.moveTo(x1,H-y1)
        for x,y in pts[1:]:p.lineTo(x,H-y)
        pdf.drawPath(p);pdf.setDash([])
        txt(min(x1,x2)+8,(y1+y2)/2-8,e['label'],12,color)
        c=ET.SubElement(root,'mxCell',id=f'e{n}',value=e['label'],style=f'edgeStyle=orthogonalEdgeStyle;html=0;endArrow=none;strokeColor={color};dashed={int(dash)};fontSize=12;',edge='1',parent='1',source=e['a'],target=e['b']);ET.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'})
    for b in page.boxes:
        x,y,w,h=b['x'],b['y'],b['w'],b['h'];color=COLORS[b['status']]
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="{color}" stroke-width="2"/>')
        pdf.setFillColor(HexColor('#ffffff'));pdf.setStrokeColor(HexColor(color));pdf.roundRect(x,H-y-h,w,h,8,fill=1,stroke=1)
        txt(x+14,y+26,b['title'],17,color,True)
        for i,line in enumerate(b['lines']):txt(x+14,y+52+i*20,line,14)
        txt(x+14,y+h-12,b['status'].upper(),11,color,True)
        value=b['title']+'\n'+'\n'.join(b['lines'])+'\n['+b['status'].upper()+']'
        c=ET.SubElement(root,'mxCell',id=b['id'],value=value,style=f'rounded=1;whiteSpace=wrap;html=0;align=left;spacing=12;fontSize=16;fillColor=#ffffff;strokeColor={color};',vertex='1',parent='1');ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'})
    for i,(x,y,t) in enumerate(page.notes):
        for j,line in enumerate(t.split('\n')):txt(x,y+j*21,line,14)
        textcell(f'n{i}',x,y-15,1400,len(t.split('\n'))*23,t,14)
    footer='DRAFT R0 | 2026-11-21 | Dashed links = unresolved/proposed, not an instruction to wire | Technical review pending'
    txt(40,975,footer,13)
    textcell('footer',40,950,1420,35,footer,13)
    svg.append('</svg>');path.with_suffix('.svg').write_text('\n'.join(svg),encoding='utf-8')
    mx=ET.Element('mxfile',host='app.diagrams.net',version='24.7.17');d=ET.SubElement(mx,'diagram',id=path.stem,name=page.title);d.append(model)
    ET.indent(mx);ET.ElementTree(mx).write(path.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
    pdf.showPage();pdf.save()

def architecture():
    d=ROOT/'hardware/v2/architecture'
    p=Page('LitterBuggy V2 / system overview','Existing build reconstruction | component identities and interfaces have separate evidence status')
    p.box('rc',40,140,340,150,'RC drive system',['3S propulsion pack (owner scope)','ESC / receiver / servos / motor','Exact models and driven axles TBD'])
    p.box('frame',560,140,360,150,'SCX6 + cart mounting interface',['Raised tub and metal interface','Visible in historical photos','Dimensions and joints unmeasured'],'historical')
    p.box('cart',1100,140,350,150,'Gorilla Cart / payload',['Tub above chassis in photos','Payload offset changes lean','No validated load envelope'],'historical')
    p.box('aux',40,410,340,170,'Auxiliary power',['Kobalt pack / blue KBT adapter','Red + black leads visible','Polarity and cutoff unverified'],'historical')
    p.box('rails',560,410,360,170,'Converters / distribution',['5V and 12V rails in repository','Fuse, switch and returns TBD','Trace current build before wiring'])
    p.box('pi',1100,410,350,170,'Raspberry Pi',['Model, power entry and OS TBD','USB acquisition + local logger','No drive-control interface planned'])
    p.box('uno',560,720,360,150,'Elegoo Uno R3',['Board identity confirmed by owner','Existing sketch not recovered','New draft defaults to idle sensors'],'confirmed')
    p.box('sensors',1100,720,350,150,'Sensors / local feedback',['MPU-6050 + HC-SR04 in history','LED + buzzer in history','OLED / camera fitting TBD'])
    p.edge('rc','frame','drive / support: trace');p.edge('frame','cart','mechanical: dimensions TBD','historical')
    p.edge('aux','rails','source feed: trace');p.edge('rails','pi','power entry TBD');p.edge('rails','uno','Uno supply route TBD');p.edge('uno','pi','USB / serial: confirm');p.edge('uno','sensors','I/O mapping TBD')
    p.note(40,650,'Evidence: owner Uno confirmation; historical photos.\nPhoto IDs: 1963-1971 and 3718-3721.\nNo stock dimensions are measured V2 facts.\nEnclosure and battery placement: measure first.\nNo RC-to-auxiliary power tie is drawn.\nPhysical isolation and grounds: unresolved.')
    render(p,d/'v2_system_overview')
    p=Page('LitterBuggy V2 / power domains','Intended domain separation; all source paths and power entries require physical trace')
    for args in [('b1',40,160,310,140,'B1 / propulsion pack',['3S named in owner scope','Chemistry / connector TBD']),('esc',560,160,340,140,'ESC + BEC / receiver',['BEC topology unverified','Steering, shift and motor']),('load',1100,160,350,140,'Propulsion loads',['Motor + servos','No Pi control in draft']),('b2',40,470,310,140,'B2 / auxiliary pack',['Kobalt 24V designation','Actual range / cutoff TBD']),('prot',560,470,340,140,'Adapter + protection',['Dock / fuse / switch','Installed order and rating TBD']),('buck',1100,470,350,140,'DC/DC converters',['5V / 12V from repository','Input ratings / settings TBD'])]:p.box(*args)
    p.box('auxload',1100,750,350,130,'Auxiliary loads',['Pi / Uno / sensors / lights','USB backfeed review required'])
    for a,b,t in [('b1','esc','+ and return: trace'),('esc','load','power / signals TBD'),('b2','prot','polarity: verify'),('prot','buck','feed / returns TBD'),('buck','auxload','branch feeds TBD')]:p.edge(a,b,t)
    p.note(40,740,'No shared ground is assumed.\nNo electrical isolation claim is made.\nNo fuse size, converter setting or wire gauge is invented.\nDetailed review drawing: ../electrical/v2_electrical.qet')
    render(p,d/'v2_power_domains')
    p=Page('LitterBuggy V2 / data flow','Proposed editable acquisition pipeline | actual old serial output remains to be captured')
    for args in [('s',40,200,310,160,'Sensor readings',['Raw IMU + distance','No synthetic measurements']),('u',560,200,340,160,'Uno R3 firmware draft',['Versioned JSON lines','Sequence + uptime + validity']),('p',1100,200,350,160,'Pi logger draft',['Validate / preserve raw bytes','Reconnect and record faults'])]:p.box(*args,status='proposed')
    p.box('store',1100,550,350,170,'Run evidence',['SQLite + raw serial + metadata','Config hash and receive time','Export to CSV'],'proposed')
    p.edge('s','u','I2C / echo TBD','proposed');p.edge('u','p','USB, 115200 proposed','proposed');p.edge('p','store','local disk / UTC','proposed')
    p.note(40,560,'Existing firmware behaviour is not claimed to match this proposed protocol.\nVoltage, yaw, temperature and emergency-stop measurements are omitted\nuntil fitted hardware and acquisition methods are established.\nLED/buzzer thresholds default disabled; no motor commands exist.\nOptional camera is a separate capture tool; no measured synchronization claim.')
    render(p,d/'v2_data_flow')

if __name__=='__main__': architecture()
