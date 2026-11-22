"""Self-contained QET project with embedded symbols and real terminal references.

All nets are draft hypotheses. QET terminal IDs are logical IDs, not connector pins.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import uuid
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'hardware/v2/electrical'
def sub(p,tag,**a): return E.SubElement(p,tag,{k:str(v) for k,v in a.items()})
def uid():return '{'+str(uuid.uuid4())+'}'
project=E.Element('project',title='LitterBuggy V2 DRAFT R0 - NOT AS BUILT',version='0.90')
collection=sub(project,'collection');cat=sub(collection,'category',name='v2')
nextid=0
def sheet(title,order):
    d=sub(project,'diagram',title=title,version='0.90',cols=22,colsize=60,rows=12,rowsize=60,height=800,folio='%id',order=order,date='20261121',author='LitterBuggy',displaycols='false',displayrows='false',displayAt='bottom')
    sub(d,'defaultconductor',type='multi',num='',condsize=1,displaytext=1)
    return d,sub(d,'elements'),sub(d,'conductors'),sub(d,'inputs')
def text(inputs,x,y,t,size=12):sub(inputs,'input',x=x,y=y,rotation=0,font=f'Sans Serif,{size},-1,5,50,0,0,0,0,0',text=t)
def block(elements,id,x,y,label,detail,kind='module'):
    global nextid
    name=id+'.elmt';entry=sub(cat,'element',name=name)
    df=sub(entry,'definition',type='element',version='0.90',width=180,height=110,hotspot_x=0,hotspot_y=0,link_type='simple')
    names=sub(df,'names');sub(names,'name',lang='en').text=label
    desc=sub(df,'description');style='line-style:normal;line-weight:normal;filling:none;color:black'
    sub(desc,'rect',x=10,y=0,width=160,height=100,style=style,antialias='false')
    for i,t in enumerate([id+' '+label,*detail]):sub(desc,'text',x=18,y=20+i*18,text=t,size=9)
    # Drawing terminals are semantic nets only; no physical pin numbering implied.
    terms=[('IN+',0,35,'w',3),('IN_RET',0,75,'w',3),('OUT+',180,35,'e',1),('OUT_RET',180,75,'e',1)]
    ids={};el=sub(elements,'element',type='embed://v2/'+name,x=x,y=y,orientation=0,z=10,uuid=uid())
    ts=sub(el,'terminals')
    for label,tx,ty,ori,nori in terms:
        sub(desc,'terminal',x=tx,y=ty,orientation=ori)
        sub(desc,'line',x1=tx,y1=ty,x2=10 if tx==0 else 170,y2=ty,style=style,end1='none',end2='none')
        sub(ts,'terminal',x=tx,y=ty,orientation=nori,id=nextid,name=label,number=label,nameHidden=1);ids[label]=nextid;nextid+=1
    sub(el,'inputs');return ids
def wire(cs,a,b,name):
    sub(cs,'conductor',terminal1=a,terminal2=b,uuid=uid(),type='multi',num=name+' / TBD',condsize=1,numsize=7,displaytext=1,text_color='#b26a00',color='#b26a00')
def pair(cs,a,b,label):wire(cs,a['OUT+'],b['IN+'],label+' POS');wire(cs,a['OUT_RET'],b['IN_RET'],label+' RET')
def header(inp,t):
    text(inp,40,30,'DRAFT R0 | '+t,18)
    text(inp,40,70,'All drawn nets are PROPOSED / UNTRACED. Logical terminal labels are NOT physical connector pin numbers.',11)
    text(inp,40,100,'Confirm models, polarity, ratings, fuse locations, returns and power entry before wiring. No ratings are assigned.',11)
    text(inp,40,700,'2026-11-21 | Owner confirms Elegoo Uno R3. Historical Nano references are superseded for this draft.',11)

d,es,cs,inp=sheet('01 Auxiliary source and distribution - proposed trace',1);header(inp,'AUXILIARY SOURCE')
b=block(es,'B2',40,220,'Kobalt pack',['24V designation','Range / cutoff TBD'])
a=block(es,'A1',290,220,'KBT adapter',['Blue dock in photos','Polarity TBD'])
f=block(es,'F1',540,220,'Main fuse',['Installed? Rating TBD','RET shown bypass role'])
s=block(es,'S1',790,220,'Main switch',['Installed? Poles TBD','RET shown bypass role'])
t=block(es,'XT1',1040,220,'Distribution',['Physical type TBD','Branch feeds sheet 02'])
for src,dst,name in [(b,a,'H01'),(a,f,'H02'),(f,s,'H03'),(s,t,'H04')]:pair(cs,src,dst,name)
text(inp,40,450,'F1/S1 are functional placeholders: only positive switching/protection is intended in this draft.',12)
text(inp,40,480,'Return pass-through is NOT an assertion of a fuse or switch on return. Exact topology must be traced.',12)
text(inp,40,530,'No RC-to-auxiliary power or ground tie is assumed. Adapter lead colours do not establish polarity.',12)

d,es,cs,inp=sheet('02 Auxiliary conversion and load branches - proposed trace',2);header(inp,'CONVERTERS AND LOADS')
t5=block(es,'XT5',40,190,'AUX feed ref',['From XT1 logically','No pin ID assigned'])
u5=block(es,'U5',370,190,'5V converter',['24V to 5V per repo','Rating / setting TBD'])
pi=block(es,'PI1',1040,190,'Raspberry Pi',['Model TBD','USB-C / GPIO TBD'])
pair(cs,t5,u5,'H05');pair(cs,u5,pi,'H06')
t12=block(es,'XT12',40,400,'AUX feed ref',['From XT1 logically','Same source intended'])
u12=block(es,'U12',370,400,'12V converter',['24V to 12V per repo','Rating / setting TBD'])
l=block(es,'L1',1040,400,'Lights / loads',['Visible in videos','Supply voltage TBD'])
pair(cs,t12,u12,'H07');pair(cs,u12,l,'H08')
text(inp,40,570,'UNO1 (Elegoo Uno R3): power entry unresolved. External buck supply and USB discussed historically.',12)
text(inp,40,600,'No external 5V/VIN/barrel/USB power route is connected here until simultaneous-source review.',12)
text(inp,40,630,'Sensor and camera power entries: TBD. 12V lighting feed is a hypothesis, not observed wiring.',12)

d,es,cs,inp=sheet('03 RC propulsion and control - proposed trace',3);header(inp,'RC PROPULSION')
b1=block(es,'B1',40,190,'3S pack',['Owner scope','Chemistry / plug TBD'])
esc=block(es,'ESC1',370,190,'ESC',['Exact model TBD','LVC / BEC TBD'])
motor=block(es,'M1',1040,190,'Motor interface',['Motor type TBD','Phase count TBD'])
pair(cs,b1,esc,'H09')
text(inp,620,225,'ESC-to-motor interface:',12);text(inp,620,255,'NOT CONNECTED; identify first',11)
text(inp,40,440,'RX1 receiver / steering / shift servo and BEC: record models, supply paths and channel assignments.',12)
text(inp,40,480,'No PWM pins, receiver channel numbers, motor phase count, fuse rating or stock-drive claim is invented.',12)
text(inp,40,520,'Pi and Uno firmware draft contains no steering, throttle or receiver output commands.',12)
OUT.mkdir(parents=True,exist_ok=True);E.indent(project);E.ElementTree(project).write(OUT/'v2_electrical.qet',encoding='utf-8',xml_declaration=True)
ids={t.get('id') for t in project.findall('.//elements/element/terminals/terminal')}
for c in project.findall('.//conductors/conductor'):
    assert c.get('terminal1') in ids and c.get('terminal2') in ids
print('QET:',len(project.findall('diagram')),'sheets;',len(ids),'terminal IDs;',len(project.findall('.//conductors/conductor')),'draft conductors')
