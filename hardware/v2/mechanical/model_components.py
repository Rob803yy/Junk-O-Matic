"""CAD-R2: native constrained profiles, lofts and photo-informed component proxies.

No custom FeaturePython dependency is needed to edit native geometry. Numeric
layout values are unmeasured; cosmetic tread detail is regenerated from source.
"""
from pathlib import Path
import json,math
import FreeCAD as App
import Part,Sketcher
BASE=Path(__file__).resolve().parent
CFG=json.loads((BASE/'dimensions.json').read_text(encoding='utf-8'))
OUT=BASE/'exports';OUT.mkdir(exist_ok=True)
V={k:v.get('layout_mm',v.get('layout_deg')) for k,v in CFG['parameters'].items()}
COL={'cart':(.13,.15,.16),'rim':(.20,.22,.23),'chassis':(.13,.16,.18),'tyre':(.075,.085,.09),'tread':(.11,.12,.13),'wheel':(.19,.20,.21),'metal':(.68,.70,.70),'orange':(.95,.31,.055),'lid':(.66,.72,.75),'blue':(.025,.22,.80),'yellow':(.98,.78,.035),'red':(.95,.04,.07),'white':(.89,.96,1.),'reference':(.50,.55,.57)}
meshes={};checks=[]
def value(e):return eval(str(e).replace('Parameters.',''),{'__builtins__':{}},V)
def ex(o,p,v):o.setExpression(p,str(v))
def prop(o,k,v,t='App::PropertyString'):
    if k not in o.PropertiesList:o.addProperty(t,k,'Review evidence')
    setattr(o,k,v)
def tag(o,c='cart',role='render',evidence='CAD-P01;CAD-P02;CAD-P03',note='Photo-informed proxy; numerical geometry unmeasured.',alpha=1.):
    for k,v in [('DraftColor',c),('ReviewRole',role),('AppearanceEvidence',evidence),('DimensionStatus','proposed / unmeasured'),('ReviewNote',note)]:prop(o,k,v)
    prop(o,'ReviewOpacity',float(alpha),'App::PropertyFloat')
    if App.GuiUp and o.ViewObject:
        o.ViewObject.Visibility=role=='render';o.ViewObject.ShapeColor=COL[c];o.ViewObject.LineColor=(.08,.09,.10);o.ViewObject.Transparency=int((1-alpha)*100)
    return o
def newdoc(name,label):
    d=App.newDocument(name);d.Label=label+' | CAD-R2 / unmeasured';s=d.addObject('Spreadsheet::Sheet','Parameters')
    s.set('A1','CAD-R2 PHOTO-INFORMED LAYOUT - NO MEASURED DIMENSIONS')
    for cell,t in [('A2','parameter'),('B2','layout value'),('C2','measured'),('D2','unit'),('E2','source / qualification')]:s.set(cell,t)
    for row,(k,v) in enumerate(CFG['parameters'].items(),3):
        s.set('A'+str(row),k);s.set('B'+str(row),str(V[k]));s.setAlias('B'+str(row),k);s.set('C'+str(row),'UNKNOWN');s.set('D'+str(row),'deg' if k.endswith('_deg') else 'mm');s.set('E'+str(row),v['source'])
    for col,width in [('A',210),('B',110),('C',100),('D',70),('E',650)]:s.setColumnWidth(col,width)
    s.setStyle('A1:E2','bold','add');d.recompute();return d
def group(d,name,label,evidence='CAD-P01;CAD-P02;CAD-P03',role='render'):
    o=d.addObject('App::Part',name);o.Label=label;return tag(o,role=role,evidence=evidence)
def box(d,g,name,L,W,H,x,y,z,c='chassis',role='render',note='Unmeasured envelope; section/fasteners unknown.',alpha=1):
    o=d.addObject('Part::Box',name);g.addObject(o)
    for p,v in zip(['Length','Width','Height','Placement.Base.x','Placement.Base.y','Placement.Base.z'],[L,W,H,x,y,z]):ex(o,p,v)
    return tag(o,c,role,note=note,alpha=alpha)
def cylinder(d,g,name,r,h,x,y,z,c='metal',axis='z',role='render'):
    o=d.addObject('Part::Cylinder',name);g.addObject(o)
    for p,v in zip(['Radius','Height','Placement.Base.x','Placement.Base.y','Placement.Base.z'],[r,h,x,y,z]):ex(o,p,v)
    if axis=='y':o.Placement.Rotation=App.Rotation(App.Vector(1,0,0),90)
    if axis=='x':o.Placement.Rotation=App.Rotation(App.Vector(0,1,0),90)
    return tag(o,c,role)
def softbox(d,g,name,L,W,H,x,y,z,c,r=4,note='Photo-informed rounded envelope; exact profile unmeasured.'):
    base=box(d,g,name+'Base',L,W,H,x,y,z,c,'construction')
    o=d.addObject('Part::Fillet',name);g.addObject(o);o.Base=base;o.Edges=[(i,r,r) for i in range(1,13)];return tag(o,c,note=note)
def rounded(d,g,name,L,W,R,z):
    """Native fully constrained 4-line/4-arc rounded rectangle, centred on XY."""
    s=d.addObject('Sketcher::SketchObject',name);g.addObject(s);tag(s,role='construction')
    lv,wv,rv=map(value,[L,W,R]);centres=[(lv/2-rv,-wv/2+rv),(lv/2-rv,wv/2-rv),(-lv/2+rv,wv/2-rv),(-lv/2+rv,-wv/2+rv)]
    for i,((x,y),a) in enumerate(zip(centres,[-90,0,90,180])):
        s.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x,y,0),App.Vector(0,0,1),rv),math.radians(a),math.radians(a+90)),False)
        for typ,expr,v in [('DistanceX',f'({L})/2-({R})' if x>0 else f'-({L})/2+({R})',x),('DistanceY',f'({W})/2-({R})' if y>0 else f'-({W})/2+({R})',y)]:
            ci=s.addConstraint(Sketcher.Constraint(typ,i,3,v));ex(s,'Constraints['+str(ci)+']',expr)
        ci=s.addConstraint(Sketcher.Constraint('Radius',i,rv));ex(s,'Constraints['+str(ci)+']',R)
        s.addConstraint(Sketcher.Constraint('Vertical' if i%2==0 else 'Horizontal',i,1,i,3));s.addConstraint(Sketcher.Constraint('Horizontal' if i%2==0 else 'Vertical',i,2,i,3))
    for i in range(4):
        li=s.addGeometry(Part.LineSegment(s.Geometry[i].EndPoint,s.Geometry[(i+1)%4].StartPoint),False)
        s.addConstraint(Sketcher.Constraint('Coincident',li,1,i,2));s.addConstraint(Sketcher.Constraint('Coincident',li,2,(i+1)%4,1))
    ex(s,'Placement.Base.z',z);return s
def loft(d,g,name,L0,W0,R0,z0,L1,W1,R1,z1,c='cart',role='render'):
    a=rounded(d,g,name+'Lower',L0,W0,R0,z0);b=rounded(d,g,name+'Upper',L1,W1,R1,z1)
    o=d.addObject('Part::Loft',name);g.addObject(o);o.Sections=[a,b];o.Solid=True;o.Ruled=True;return tag(o,c,role)
def ring(d,g,name,L,W,R,z,h,w,c='rim'):
    a=loft(d,g,name+'Outer',L,W,R,z,L,W,R,f'({z})+({h})',c,'construction')
    b=loft(d,g,name+'Void',f'({L})-2*({w})',f'({W})-2*({w})',f'({R})-({w})',f'({z})-1',f'({L})-2*({w})',f'({W})-2*({w})',f'({R})-({w})',f'({z})+({h})+1',c,'construction')
    o=d.addObject('Part::Cut',name);g.addObject(o);o.Base=a;o.Tool=b;return tag(o,c)
def worldshape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def finish(d,objects):
    d.recompute();items=[]
    for o in objects:
        s=worldshape(o);assert not s.isNull() and s.isValid() and s.Volume>0,(d.Name,o.Name,o.State)
        checks.append({'document':d.Name,'object':o.Name,'valid':True,'solid_count':len(s.Solids),'volume_mm3':s.Volume,'dimension_status':'unmeasured layout'})
        vs,ts=s.tessellate(2);items.append({'name':o.Name,'label':o.Label,'color':COL[o.DraftColor],'opacity':o.ReviewOpacity,'vertices':[[v.x,v.y,v.z] for v in vs],'triangles':ts})
    for o in d.Objects:
        if App.GuiUp and o.ViewObject and hasattr(o,'ReviewRole'):o.ViewObject.Visibility=o.ReviewRole=='render'
    if App.GuiUp:App.Gui.activeDocument().activeView().viewAxonometric();App.Gui.activeDocument().activeView().fitAll()
    name=d.Name;d.saveAs(str(BASE/(name+'.FCStd')))
    temp=App.newDocument('Export_'+name);leaves=[]
    for o in objects:
        leaf=temp.addObject('Part::Feature',o.Name);leaf.Label=o.Label;leaf.Shape=worldshape(o);leaves.append(leaf)
    temp.recompute();stepfile=OUT/(name+'.step');Part.export(leaves,str(stepfile));App.closeDocument(temp.Name)
    stepfile.write_text('\n'.join(line.rstrip() for line in stepfile.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    meshes[name]=items;App.closeDocument(name);r=App.openDocument(str(BASE/(name+'.FCStd')));assert r.Objects;App.closeDocument(r.Name)
    s=Part.Shape();s.read(str(OUT/(name+'.step')));assert s.isValid() and s.Volume>0,name
def mount(d):
    g=group(d,'CartSupports','Visible strips / inferred under-tub supports');objects=[]
    for i,x in enumerate([-170,170]):objects.append(box(d,g,'CrossSupport'+str(i),26,'Parameters.cart_bottom_width-30',20,x,'-Parameters.cart_bottom_width/2+15','Parameters.mount_z-20','metal',note='Occluded joint layout inferred; fastening and load path unknown.'))
    for i,y in enumerate([-230,224]):
        o=box(d,g,'VisibleSideStrip'+str(i),26,6,190,90,y,95,'metal',note='Strip visible in CAD-P01/P03; lower end and attachments unmeasured.');o.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-8);objects.append(o)
    return objects
def tub(d):
    g=group(d,'Cart','Flared Gorilla tub / molded-feature proxies');ex(g,'Placement.Base.x','Parameters.cart_offset_x')
    a=loft(d,g,'TubOuter','Parameters.cart_bottom_length','Parameters.cart_bottom_width','Parameters.cart_bottom_radius','Parameters.mount_z','Parameters.cart_length','Parameters.cart_width','Parameters.cart_corner_radius','Parameters.mount_z+Parameters.cart_height','cart','construction')
    L='Parameters.cart_bottom_length+(Parameters.cart_length-Parameters.cart_bottom_length)*Parameters.wall/Parameters.cart_height-2*Parameters.wall';W='Parameters.cart_bottom_width+(Parameters.cart_width-Parameters.cart_bottom_width)*Parameters.wall/Parameters.cart_height-2*Parameters.wall'
    b=loft(d,g,'TubVoid',L,W,'Parameters.cart_bottom_radius-Parameters.wall','Parameters.mount_z+Parameters.wall','Parameters.cart_length-2*Parameters.wall','Parameters.cart_width-2*Parameters.wall','Parameters.cart_corner_radius-Parameters.wall','Parameters.mount_z+Parameters.cart_height+1','cart','construction')
    cut=d.addObject('Part::Cut','CartTub');g.addObject(cut);cut.Base=a;cut.Tool=b;tag(cut,'cart',note='Observed flared rounded tub; exact mold profile and dimensions unmeasured.')
    objects=[cut,ring(d,g,'RolledRim','Parameters.cart_length+2*Parameters.rim_overhang','Parameters.cart_width+2*Parameters.rim_overhang','Parameters.cart_corner_radius+Parameters.rim_overhang','Parameters.mount_z+Parameters.cart_height-Parameters.rim_height/2','Parameters.rim_height',16)]
    for i,y in enumerate([-144,-72,0,72,144]):objects.append(box(d,g,'FloorRib'+str(i),'Parameters.cart_bottom_length-95',8,7,'-Parameters.cart_bottom_length/2+48',y,'Parameters.mount_z+Parameters.wall-1','rim',note='Stylized floor molding; exact rib count/section unknown.'))
    return objects
def enclosure(d,assembly=False):
    g=group(d,'ElectronicsCase','External orange case / vertical lid','CAD-P01;CAD-P02')
    if assembly:
        g.Placement.Rotation=App.Rotation(App.Vector(1,0,0),90);ex(g,'Placement.Base.x','Parameters.enclosure_x');ex(g,'Placement.Base.z','Parameters.enclosure_z')
        ex(g,'Placement.Base.y','-Parameters.cart_width/2-Parameters.rim_overhang-Parameters.enclosure_gap')
    a=loft(d,g,'CaseOuter','Parameters.enclosure_length','Parameters.enclosure_height',12,0,'Parameters.enclosure_length','Parameters.enclosure_height',12,'Parameters.enclosure_width','orange','construction')
    b=loft(d,g,'CaseVoid','Parameters.enclosure_length-10','Parameters.enclosure_height-10',7,5,'Parameters.enclosure_length-10','Parameters.enclosure_height-10',7,'Parameters.enclosure_width+1','orange','construction')
    case=d.addObject('Part::Cut','EnclosureShell');g.addObject(case);case.Base=a;case.Tool=b;tag(case,'orange',note='Vertical orientation observed; nominal catalog size unverified. Internal layout unknown.')
    lid=loft(d,g,'ClearLid','Parameters.enclosure_length-8','Parameters.enclosure_height-8',8,'Parameters.enclosure_width','Parameters.enclosure_length-8','Parameters.enclosure_height-8',8,'Parameters.enclosure_width+3','lid');tag(lid,'lid',alpha=.28,note='Translucent lid proxy. No invented Pi/Uno placement.')
    objects=[case,lid,ring(d,g,'LidOrangeRim','Parameters.enclosure_length','Parameters.enclosure_height',12,'Parameters.enclosure_width-2',6,7,'orange')]
    for i,x in enumerate([-115,105]):
        for j,sgn in enumerate([-1,1]):objects.append(box(d,g,'CaseLatch'+str(i)+str(j),14,10,8,x,f'{sgn}*Parameters.enclosure_height/2-5','Parameters.enclosure_width-1','orange',note='Latch/ear appearance only; mounting pattern unverified.'))
    return objects
def dock(d,assembly=False):
    g=group(d,'BatteryCorner','Blue pack / dark adapter / slide-rail proxies','CAD-P01;CAD-P02')
    if assembly:
        for p,k in [('x','dock_x'),('y','dock_y'),('z','dock_z')]:ex(g,'Placement.Base.'+p,'Parameters.'+k)
        g.Placement.Rotation=App.Rotation(App.Vector(0,0,1),V['dock_yaw_deg'])*App.Rotation(App.Vector(1,0,0),90+V['dock_tilt_deg'])
        prop(g,'AngleQualification','Yaw/tilt are unmeasured visual estimates; regenerate after editing angle parameters.')
    objects=[box(d,g,'AdapterPlate','Parameters.dock_length','Parameters.dock_width','Parameters.dock_height','-Parameters.dock_length/2','-Parameters.dock_width/2',0),softbox(d,g,'BluePack','Parameters.battery_length','Parameters.battery_width','Parameters.battery_depth','-Parameters.battery_length/2','-Parameters.battery_width/2','Parameters.dock_height','blue',note='Blue pack-like envelope; brand, voltage, dimensions and retention unresolved.'),box(d,g,'PackBlackTop','Parameters.battery_length',12,'Parameters.battery_depth+2','-Parameters.battery_length/2','Parameters.battery_width/2-8','Parameters.dock_height')]
    for i,y in enumerate([-30,22]):objects.append(box(d,g,'AdapterRail'+str(i),'Parameters.dock_length-8',8,7,'-Parameters.dock_length/2+4',y,-7,'metal',note='Rail appearance; no conductive contact/latch-clearance claim.'))
    objects.append(box(d,g,'ReleaseFeature',24,12,8,-12,'-Parameters.battery_width/2-7','Parameters.dock_height+20',note='Unidentified dark feature; no release mechanism design implied.'))
    return objects
def lighting(d,assembly=False):
    g=group(d,'FrontLighting','Two front light points / reserved sensor interface','CAD-P02')
    if assembly:ex(g,'Placement.Base.x','Parameters.cart_offset_x+Parameters.cart_bottom_length/2+35');ex(g,'Placement.Base.z','Parameters.mount_z-45')
    objects=[box(d,g,'LampSupport',18,175,15,-9,-87.5,0,note='Support envelope; exact bracket and holes unresolved.')]
    for i,sgn in enumerate([-1,1]):
        objects.append(cylinder(d,g,'LampHousing'+str(i),12,16,5,f'{sgn}*Parameters.front_lamp_spacing/2',7.5,'chassis','x'))
        objects.append(cylinder(d,g,'WhiteLamp'+str(i),8,3,21,f'{sgn}*Parameters.front_lamp_spacing/2',7.5,'white','x'))
    if not assembly:
        ref=group(d,'UnselectedSensorReference','HISTORICAL HC-SR04 / unselected / excluded from STEP','S06 research report','reference')
        hist=box(d,ref,'HistoricalSensorBoard',46,20,2,-23,-10,-60,'reference','reference');prop(hist,'AppearanceEvidence','S06 historical description; not observed in CAD-P01..03')
        for i,x in enumerate([-13,13]):
            hist=cylinder(d,ref,'HistoricalTransducer'+str(i),8,12,x,0,-58,'reference',role='reference');prop(hist,'AppearanceEvidence','S06 historical description; not observed in CAD-P01..03')
    return objects
def accessories(d):
    g=group(d,'TubAccessories','Yellow front handle and rim lights');ex(g,'Placement.Base.x','Parameters.cart_offset_x')
    front='Parameters.cart_bottom_length/2+(Parameters.cart_length-Parameters.cart_bottom_length)*0.57/2'
    objects=[box(d,g,'MoldedEndPanel',9,175,100,front,-87.5,'Parameters.mount_z+35','cart'),box(d,g,'YellowHandleBack',22,'Parameters.handle_width-25','Parameters.handle_height-45',f'({front})+9','-Parameters.handle_width/2+12.5','Parameters.mount_z+28','yellow'),softbox(d,g,'YellowGrip',18,'Parameters.handle_width',18,f'({front})+48','-Parameters.handle_width/2','Parameters.mount_z+102','yellow')]
    for i,sgn in enumerate([-1,1]):objects.append(box(d,g,'HandleArm'+str(i),48,14,45,f'({front})+10',f'{sgn}*(Parameters.handle_width/2-7)-7','Parameters.mount_z+65','yellow'))
    for side,sgn in enumerate([-1,1]):
        for i,x in enumerate([-330,-140,50]):
            objects.append(box(d,g,'StripHousing'+str(side)+str(i),76,9,15,x,f'{sgn}*(Parameters.cart_width/2+6)-4.5','Parameters.mount_z+Parameters.cart_height-4'))
            objects.append(box(d,g,'RedStrip'+str(side)+str(i),66,3,9,x+5,f'{sgn}*(Parameters.cart_width/2+12)-1.5','Parameters.mount_z+Parameters.cart_height-1','red',note='Strip-light appearance; diode/group counts stylized, power/wiring unresolved.'))
    return objects
def chassis(d):
    g=group(d,'Chassis','SCX6 chassis / simplified visible envelopes');objects=[]
    for i,sgn in enumerate([-1,1]):objects.append(box(d,g,'ChassisRail'+str(i),'Parameters.rail_length',12,30,'-Parameters.rail_length/2',f'{sgn}*Parameters.rail_spacing/2-6','Parameters.chassis_z'))
    objects.append(box(d,g,'UnderbodyEnvelope',290,170,55,-145,-85,'Parameters.chassis_z-40',note='Obscured chassis bulk; no ESC/motor/receiver identity inferred.'))
    for ax,sx in enumerate([-1,1]):
        objects.append(cylinder(d,g,'Axle'+str(ax),12,'Parameters.track_centres',f'{sx}*Parameters.wheelbase/2','Parameters.track_centres/2','Parameters.tyre_radius','chassis','y'))
        for side,sy in enumerate([-1,1]):
            wg=group(d,'Wheel'+str(ax)+str(side),('Front' if sx>0 else 'Rear')+' wheel / '+('enclosure side' if sy<0 else 'opposite side'))
            ex(wg,'Placement.Base.x',f'{sx}*Parameters.wheelbase/2');ex(wg,'Placement.Base.y',f'{sy}*Parameters.track_centres/2');ex(wg,'Placement.Base.z','Parameters.tyre_radius')
            pts=[('Parameters.tyre_radius*.57','-Parameters.tyre_width/2+5'),('Parameters.tyre_radius-7','-Parameters.tyre_width/2'),('Parameters.tyre_radius','-Parameters.tyre_width/2+9'),('Parameters.tyre_radius','Parameters.tyre_width/2-9'),('Parameters.tyre_radius-7','Parameters.tyre_width/2'),('Parameters.tyre_radius*.57','Parameters.tyre_width/2-5')]
            s=d.addObject('Sketcher::SketchObject','TyreProfile'+str(ax)+str(side));wg.addObject(s);tag(s,role='construction')
            for i,(x,y) in enumerate(pts):
                nx,ny=pts[(i+1)%len(pts)];s.addGeometry(Part.LineSegment(App.Vector(value(x),value(y),0),App.Vector(value(nx),value(ny),0)),False)
            for i,(x,y) in enumerate(pts):
                for typ,v in [('DistanceX',x),('DistanceY',y)]:
                    ci=s.addConstraint(Sketcher.Constraint(typ,i,1,value(v)));ex(s,'Constraints['+str(ci)+']',v)
                s.addConstraint(Sketcher.Constraint('Coincident',i,2,(i+1)%len(pts),1))
            tire=d.addObject('Part::Revolution','Tyre'+str(ax)+str(side));wg.addObject(tire);tire.Source=s;tire.Axis=App.Vector(0,1,0);tire.Angle=360;tire.Solid=True;tag(tire,'tyre');objects.append(tire)
            objects.append(cylinder(d,wg,'WheelRim'+str(ax)+str(side),'Parameters.tyre_radius*.57','Parameters.tyre_width-6',0,'Parameters.tyre_width/2-3',0,'wheel','y'))
            objects.append(cylinder(d,wg,'WheelHub'+str(ax)+str(side),17,'Parameters.tyre_width+2',0,'Parameters.tyre_width/2+1',0,'chassis','y'))
            lugs=[]
            for n in range(16):
                for half in [-1,1]:
                    sh=Part.makeBox(13,V['tyre_width']*.43,5,App.Vector(-6.5,(-.46 if half<0 else .03)*V['tyre_width'],V['tyre_radius']-5));sh.rotate(App.Vector(),App.Vector(0,1,0),n*22.5+(6 if half>0 else 0));lugs.append(sh)
            o=d.addObject('Part::Feature','Tread'+str(ax)+str(side));wg.addObject(o);o.Shape=Part.makeCompound(lugs);tag(o,'tread',note='Stylized tread, not OEM geometry. Regenerate after radius/width changes; placement follows parametric wheel.');objects.append(o)
    bg=group(d,'FrontBumper','Photo-informed front bumper / skid envelope','CAD-P02');ex(bg,'Placement.Base.x','Parameters.wheelbase/2+67')
    objects.append(loft(d,bg,'BumperBody',145,385,22,65,115,340,16,126,'chassis'))
    for i,y in enumerate([-128,73]):objects.append(box(d,bg,'BumperPad'+str(i),70,55,6,-30,y,127,'reference',note='Gray pad appearance; material and part identity unverified.'))
    objects.append(box(d,bg,'BumperRedDetail',26,38,20,20,-19,127,'red',note='Visible red feature; towing/lifting function not established.'))
    return objects
def build():
    for name,label,builder in [('v2_cart_mount','Cart supports',mount),('v2_battery_mount','Blue pack / adapter corner',dock),('v2_electronics_enclosure','External enclosure',enclosure),('v2_sensor_mounts','Front lighting / reserved sensor interface',lighting)]:
        d=newdoc(name,label);finish(d,builder(d))
    d=newdoc('v2_assembly','LitterBuggy V2 photo-informed assembly')
    finish(d,chassis(d)+mount(d)+tub(d)+enclosure(d,True)+dock(d,True)+accessories(d)+lighting(d,True))
    (OUT/'review-meshes.json').write_text(json.dumps(meshes,separators=(',',':')),encoding='utf-8')
    (OUT/'geometry-checks.json').write_text(json.dumps({'revision':'CAD-R2','FreeCAD_version':App.Version(),'checks':checks,'note':'Geometry/STEP checks only; dimensions, fit, hidden joints and load capacity unverified. Bucket omitted by owner. Raw photos excluded from Git.'},indent=2),encoding='utf-8')
    print('CAD-R2: five native/STEP documents saved and reopened;',len(checks),'component records')
if __name__=='__main__':build()
