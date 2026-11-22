"""Generate WireViz review harnesses; all connections remain proposed/untraced."""
from pathlib import Path
import csv
import yaml
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'hardware/v2/wiring';OUT.mkdir(parents=True,exist_ok=True)
def connector(name,pins):return {'type':name+' / DRAFT - physical connector TBD','pins':pins,'pinlabels':pins,'notes':'Logical functions only; physical order/view, part number and ratings TBD.'}
def write(name,conns,cables,paths):
    data={'metadata':{'title':name+' / DRAFT R0 - NOT AS BUILT','revision':'R0','notes':'All links proposed or untraced. Wire gauge, colour, length and physical pin numbering TBD.'},'connectors':conns,'cables':cables,'connections':paths}
    (OUT/(name+'.yml')).write_text(yaml.safe_dump(data,sort_keys=False),encoding='utf-8')
    return data
power={};cables={};paths=[]
links=[('H01','B2','Kobalt pack','A1_IN','Adapter contacts'),('H02','A1_OUT','Adapter leads','F1_IN','Protection input'),('H03','F1_OUT','Protection output','S1_IN','Switch input'),('H04','S1_OUT','Switch output','XT1','Auxiliary distribution'),('H05','XT1','Auxiliary distribution','U5_IN','5V converter input'),('H06','U5_OUT','5V converter output','PI1','Pi power entry TBD'),('H07','XT1','Auxiliary distribution','U12_IN','12V converter input'),('H08','U12_OUT','12V converter output','L1','Lighting supply TBD'),('H09','B1','3S propulsion pack','ESC1','ESC input')]
for h,a,an,b,bn in links:
    for id,title in [(a,an),(b,bn)]:power[id]=connector(title,['POS_TBD','RET_TBD'])
    cables[h]={'wirecount':2,'notes':h+' proposed trace; no colour, gauge or length specified.'}
    paths.append([{a:['POS_TBD','RET_TBD']},{h:[1,2]},{b:['POS_TBD','RET_TBD']}])
p=write('v2_power_harness',power,cables,paths)
sensors={
 'UNO1_I2C':connector('Elegoo Uno R3 proposed I2C',['SDA_A4','SCL_A5','SUPPLY_TBD','GND']),
 'IMU1':connector('MPU-6050 breakout identity unverified',['SDA','SCL','VCC_TBD','GND']),
 'UNO1_RANGE':connector('Elegoo Uno R3 digital pins unresolved',['TRIG_PIN_TBD','ECHO_PIN_TBD','SUPPLY_TBD','GND']),
 'RANGE1':connector('HC-SR04 identity unverified',['TRIG','ECHO','VCC_TBD','GND']),
 'UNO1_LED':connector('Uno LED output unresolved',['LED_PIN_TBD','GND']),
 'LED1':connector('LED with series resistor TBD',['RESISTOR_LED_PATH','GND']),
 'UNO1_BUZZ':connector('Uno buzzer output unresolved',['BUZZ_PIN_TBD','GND']),
 'BZ1':connector('Buzzer drive interface TBD',['CONTROL_TBD','GND'])}
sp=[];sc={}
for h,a,b in [('H10','UNO1_I2C','IMU1'),('H11','UNO1_RANGE','RANGE1'),('H12','UNO1_LED','LED1'),('H13','UNO1_BUZZ','BZ1')]:
    n=len(sensors[a]['pins']);sc[h]={'wirecount':n,'notes':'Proposed functional mapping only. Verify supplies, pullups, driver parts and pin assignments.'};sp.append([{a:sensors[a]['pins']},{h:list(range(1,n+1))},{b:sensors[b]['pins']}])
s=write('v2_sensor_harness',sensors,sc,sp)
with (OUT/'connector_register.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['logical_id','description','logical_functions','physical_part','physical_pin_order','view_direction','status'])
    for data in [p,s]:
        for id,c in data['connectors'].items():w.writerow([id,c['type'],';'.join(c['pins']),'TBD','TBD','TBD','proposed'])
with (OUT/'connection_register.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['harness','conductor','from_id','from_function','to_id','to_function','colour','gauge','length_mm','status'])
    for data in [p,s]:
        for a,h,b in data['connections']:
            ai=next(iter(a));bi=next(iter(b));hi=next(iter(h))
            for n,(ap,bp) in enumerate(zip(a[ai],b[bi]),1):w.writerow([hi,n,ai,ap,bi,bp,'TBD','TBD','TBD','proposed'])
print('Draft connectors:',len(power)+len(sensors),'functional wire rows:',sum(len(p[1][next(iter(p[1]))]) for p in paths+sp))
