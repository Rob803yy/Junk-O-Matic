"""Generate editable diagrams and review exports from the same scene geometry."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
import textwrap
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[2]
W,H=1500,1000
COLORS={'confirmed':'#216e4e','unknown':'#b26a00','proposed':'#7251a3','historical':'#3978a8','conflicting':'#b33a3a'}
class NoPDF:
    """Leave prior PDFs unchanged until the owner reviews the corrected sources."""
    def __getattr__(self,name):
        if name=='beginPath':return lambda:self
        return lambda *args,**kwargs:None

class Page:
    def __init__(self,title,subtitle):
        self.title,self.subtitle=title,subtitle; self.boxes=[]; self.edges=[]; self.notes=[]
    def box(self,id,x,y,w,h,title,lines,status='unknown'):
        self.boxes.append(dict(id=id,x=x,y=y,w=w,h=h,title=title,lines=lines,status=status)); return id
    def edge(self,a,b,label,kind='unknown'):
        self.edges.append(dict(a=a,b=b,label=label,status=kind))
    def note(self,x,y,text):self.notes.append((x,y,text))

def render(page,path,emit_pdf=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    model=ET.Element('mxGraphModel',dx='1500',dy='1000',grid='1',gridSize='10',page='1',pageWidth=str(W),pageHeight=str(H))
    root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1500" height="1000" fill="#f5f7fa"/>']
    pdf=Canvas(str(path.with_suffix('.pdf')),pagesize=(W,H)) if emit_pdf else NoPDF()
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
    footer='DRAFT R1 | 2026-11-21 | Dashed links = unresolved/proposed, not an instruction to wire | Technical review pending'
    txt(40,975,footer,13)
    textcell('footer',40,950,1420,35,footer,13)
    svg.append('</svg>');path.with_suffix('.svg').write_text('\n'.join(svg),encoding='utf-8')
    mx=ET.Element('mxfile',host='app.diagrams.net',version='24.7.17');d=ET.SubElement(mx,'diagram',id=path.stem,name=page.title);d.append(model)
    ET.indent(mx);ET.ElementTree(mx).write(path.with_suffix('.drawio'),encoding='utf-8',xml_declaration=True)
    pdf.showPage();pdf.save()

def architecture():
    d=ROOT/'hardware/v2/architecture'
    p=Page('LitterBuggy V2 / system overview','Existing build reconstruction | component identities and interfaces have separate evidence status')
    p.box('rc',40,140,340,150,'RC drive system',['3S propulsion pack (owner scope)','Stock SCX6: 4WD / two-speed','Installed modifications unverified'])
    p.box('frame',560,140,360,150,'SCX6 + cart mounting interface',['Raised tub and metal interface','Visible in historical photos','Dimensions and joints unmeasured'],'historical')
    p.box('cart',1100,140,350,150,'Gorilla Cart / payload',['Tub above chassis in photos','Payload offset changes lean','No validated load envelope'],'historical')
    p.box('aux',40,410,340,170,'Auxiliary power',['Kobalt pack / blue KBT adapter','Red + black leads visible','Polarity and cutoff unverified'],'historical')
    p.box('rails',560,410,360,170,'Converters / distribution',['5V 10A + separate 5V 3A listed','12V branch is a proposal','Settings / routing unverified'])
    p.box('pi',1100,410,350,170,'Raspberry Pi / model conflict',['Pi 3B in S06; Pi 4 elsewhere','Power entry, OS and fitting TBD','New draft: logging only'],'conflicting')
    p.box('uno',560,720,360,150,'Elegoo Uno R3',['Board identity confirmed by owner','Existing sketch not recovered','New draft defaults to idle sensors'],'confirmed')
    p.box('sensors',1100,720,350,150,'Sensors / availability conflict',['HC-SR04 reported lost (S06)','A02YYUW UART is proposed','IMU / LED / buzzer fitting TBD'],'conflicting')
    p.edge('rc','frame','drive / support: trace');p.edge('frame','cart','mechanical: dimensions TBD','historical')
    p.edge('aux','rails','source feed: trace');p.edge('rails','pi','power entry TBD');p.edge('rails','uno','Uno supply route TBD');p.edge('uno','pi','USB / serial: confirm');p.edge('uno','sensors','I/O mapping TBD')
    p.note(40,650,'Owner confirms Uno; other claims source-attributed.\nS01-S14: docs/reconciliation/source-inventory.json\nVersion map is provisional: V2 reconstruction,\nV3 future capability concepts; owner review pending.\nPosters do not prove installation or performance.\nGrounds, mount dimensions and Pi remain unresolved.')
    render(p,d/'v2_system_overview')
    p=Page('LitterBuggy V2 / power domains','Intended domain separation; all source paths and power entries require physical trace')
    for args in [('b1',40,160,310,140,'B1 / propulsion pack',['3S named in owner scope','Chemistry / connector TBD']),('esc',560,160,340,140,'ESC + BEC / receiver',['BEC topology unverified','Steering, shift and motor']),('load',1100,160,350,140,'Propulsion loads',['Motor + servos','No Pi control in draft']),('b2',40,470,310,140,'B2 / auxiliary pack',['Kobalt 24V designation','Actual range / cutoff TBD']),('prot',560,470,340,140,'Adapter + protection',['Dock / fuse / switch','Installed order and rating TBD']),('buck',1100,470,350,140,'DC/DC converters',['5V / 12V from repository','Input ratings / settings TBD'])]:p.box(*args)
    p.box('auxload',1100,750,350,130,'Auxiliary loads',['Pi / Uno / sensors / lights','USB backfeed review required'])
    for a,b,t in [('b1','esc','+ and return: trace'),('esc','load','power / signals TBD'),('b2','prot','polarity: verify'),('prot','buck','feed / returns TBD'),('buck','auxload','branch feeds TBD')]:p.edge(a,b,t)
    p.note(40,740,'U5: source-listed 5V 10A; U5A: separate source-listed 5V 3A.\nU5A routing is OPEN; outputs are not paralleled.\n12V converter is a proposal; fitted lighting voltage unknown.\nKB624-03 is a battery designation, not a fuse/switch.\nNo shared ground, isolation or selected fuse value is assumed.\nDetailed review drawing: ../electrical/v2_electrical.qet')
    render(p,d/'v2_power_domains')
    p=Page('LitterBuggy V2 / data flow','Proposed editable acquisition pipeline | actual old serial output remains to be captured')
    for args in [('s',40,200,310,160,'Sensor readings',['Raw IMU + distance','No synthetic measurements']),('u',560,200,340,160,'Uno R3 firmware draft',['Versioned JSON lines','Sequence + uptime + validity']),('p',1100,200,350,160,'Pi logger draft',['Validate / preserve raw bytes','Reconnect and record faults'])]:p.box(*args,status='proposed')
    p.box('store',1100,550,350,170,'Run evidence',['SQLite + raw serial + metadata','Config hash and receive time','Export to CSV'],'proposed')
    p.edge('s','u','I2C / echo TBD','proposed');p.edge('u','p','USB, 115200 proposed','proposed');p.edge('p','store','local disk / UTC','proposed')
    p.note(40,560,'New contract: JSON protocol 2, proposed 10Hz records; drivers default OFF.\nS06 CSV D/H protocol and 20Hz IMU + 1Hz status remain source proposals.\nLegacy 50-100Hz IMU targets are not implemented or field-verified.\nOriginal running sketch / format has not been recovered.\nRaw MPU-6050 data does not provide validated absolute heading.\nNo RC commands, motion watchdog, GPS, sorting or autonomous navigation.\nOptional camera capture is separate; no synchronization accuracy claim.')
    render(p,d/'v2_data_flow')
    p=Page('LitterBuggy V2 / digital connectivity','Review of logical interfaces | logical pin functions are not verified physical wiring')
    p.box('pi',40,150,370,160,'Pi model unresolved',['Pi 3B vs Pi 4 source conflict','USB host serial proposed','No GPIO or RC control assumed'],'conflicting')
    p.box('uno',560,150,370,160,'Elegoo Uno R3',['Owner confirms board identity','USB serial, 115200 proposed','Existing running software unknown'],'confirmed')
    p.box('imu',1100,150,350,160,'MPU-6050 candidate',['I2C SDA=A4 / SCL=A5 on Uno','Breakout / supply / pullups TBD','Driver default OFF'],'proposed')
    p.box('range',560,490,370,170,'Historical HC-SR04 profile',['Reported lost in S06','Trigger / echo pins unassigned','Driver default OFF'],'conflicting')
    p.box('uart',1100,490,350,170,'Replacement candidate',['A02YYUW / SEN0311 proposed','UART 9600; different protocol','OPEN: no driver / pins selected'],'proposed')
    p.box('out',40,490,370,170,'Local feedback candidate',['LED resistor / buzzer drive TBD','Pins / threshold unassigned','Outputs default OFF'],'proposed')
    p.edge('pi','uno','USB / serial: trace','proposed')
    p.edge('uno','imu','I2C: verify board','proposed')
    p.edge('uno','range','Historical profile only','proposed')
    p.note(40,760,'OPEN: Pi power entry; USB power coexistence; sensor supply levels and physical connector views.\nA02YYUW is not connected to HC-SR04 trigger/echo pins. Candidate replacement remains unselected.\nCamera path, OLED, encoders, PCA9685, GPS/RTK, LiDAR and motion-control interfaces: future / unresolved.\nMPU-6050 has no magnetometer. No absolute yaw, odometry or obstacle-avoidance capability is established.\nSources: S04 BOM; S06 research report; owner Uno confirmation; REC-001..038 discrepancy register.')
    render(p,d/'v2_digital_connectivity')

if __name__=='__main__': architecture()
