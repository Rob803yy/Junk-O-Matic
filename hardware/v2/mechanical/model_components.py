"""CAD-R3: photo-informed frame, native profiles and editable tub tipping pose.

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
COL={'cart':(.13,.15,.16),'rim':(.20,.22,.23),'chassis':(.13,.16,.18),'tyre':(.075,.085,.09),'tread':(.11,.12,.13),'wheel':(.19,.20,.21),'metal':(.68,.70,.70),'orange':(.95,.31,.055),'lid':(.66,.72,.75),'blue':(.025,.22,.80),'yellow':(.98,.78,.035),'red':(.95,.04,.07),'white':(.89,.96,1.),'reference':(.50,.55,.57),'frame':(.36,.39,.40),'purple':(.46,.23,.61),'fastener':(.66,.49,.22),'spring':(.28,.30,.31)}
meshes={};checks=[];poses={}
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
    d=App.newDocument(name);d.Label=label+' | CAD-R3 / unmeasured';s=d.addObject('Spreadsheet::Sheet','Parameters')
    s.set('A1','CAD-R3 PHOTO-INFORMED LAYOUT - NO MEASURED DIMENSIONS')
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
def meshitem(o):
    if o.Name.startswith('FrontSpring'):
        # Display LOD only: avoid a very dense OCC NURBS mesh for the cosmetic
        # sweep. The full native/STEP pipe solid remains the geometry authority.
        vs=[];ts=[];steps=108;sides=8;h=V['front_shock_height'];length=math.sqrt((10*12*math.pi)**2+h*h)
        placement=o.getGlobalPlacement()
        for i in range(steps+1):
            t=i/steps;a=12*math.pi*t;ca,sa=math.cos(a),math.sin(a)
            for j in range(sides):
                u=2*math.pi*j/sides;c,sn=math.cos(u),math.sin(u)
                p=App.Vector(10*ca+1.5*(ca*c-h*sa/length*sn),10*sa+1.5*(sa*c+h*ca/length*sn),h*t-1.5*10*12*math.pi/length*sn)
                vs.append(placement.multVec(p))
        for i in range(steps):
            for j in range(sides):
                a=i*sides+j;b=i*sides+(j+1)%sides;c=(i+1)*sides+j;e=(i+1)*sides+(j+1)%sides;ts.extend([(a,c,b),(b,c,e)])
    else:s=worldshape(o);vs,ts=s.tessellate(2)
    parent=o.getParentGeoFeatureGroup()
    return {'name':o.Name,'label':o.Label,'assembly_group':parent.Name if parent else '', 'color':COL[o.DraftColor],'opacity':o.ReviewOpacity,'vertices':[[v.x,v.y,v.z] for v in vs],'triangles':ts}
def finish(d,objects):
    d.recompute();items=[]
    for o in objects:
        s=worldshape(o);assert not s.isNull() and s.isValid() and s.Volume>0,(d.Name,o.Name,o.State)
        checks.append({'document':d.Name,'object':o.Name,'valid':True,'solid_count':len(s.Solids),'volume_mm3':s.Volume,'dimension_status':'unmeasured layout'})
        items.append(meshitem(o))
    for o in d.Objects:
        if App.GuiUp and o.ViewObject and hasattr(o,'ReviewRole'):o.ViewObject.Visibility=o.ReviewRole=='render'
    if App.GuiUp:App.Gui.activeDocument().activeView().viewAxonometric();App.Gui.activeDocument().activeView().fitAll()
    name=d.Name;d.saveAs(str(BASE/(name+'.FCStd')))
    if name=='v2_assembly':
        cell='B'+str(list(CFG['parameters']).index('tub_tip_angle_deg')+3)
        original={o.Name:o.getGlobalPlacement() for o in objects}
        d.Parameters.set(cell,str(V['service_pose_angle_deg']));d.recompute()
        transforms={}
        for o in objects:
            matrix=(o.getGlobalPlacement()*original[o.Name].inverse()).toMatrix()
            if any(abs(a-b)>1e-7 for a,b in zip(matrix.A,App.Matrix().A)):transforms[o.Name]=matrix.A
        poses['v2_assembly_tipped']={'angle_deg':V['service_pose_angle_deg'],'qualification':'Illustrative pose. Rear hinge/fixed frame confirmed by owner; pivot location, travel, latch, bracket membership and clearance unverified.','transforms':transforms}
        d.Parameters.set(cell,str(V['tub_tip_angle_deg']));d.recompute()
    temp=App.newDocument('Export_'+name);leaves=[]
    for o in objects:
        leaf=temp.addObject('Part::Feature',o.Name);leaf.Label=o.Label;leaf.Shape=worldshape(o);leaves.append(leaf)
    temp.recompute();stepfile=OUT/(name+'.step');Part.export(leaves,str(stepfile));App.closeDocument(temp.Name)
    stepfile.write_text('\n'.join(line.rstrip() for line in stepfile.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    meshes[name]=items;App.closeDocument(name);r=App.openDocument(str(BASE/(name+'.FCStd')));assert r.Objects;App.closeDocument(r.Name)
    s=Part.Shape();s.read(str(OUT/(name+'.step')));assert s.isValid() and s.Volume>0,name
def square_tube(d,g,name,L,W,H,x,y,z,wall,c='metal'):
    a=box(d,g,name+'Outer',L,W,H,x,y,z,c,'construction')
    b=box(d,g,name+'Void',f'({L})+2',f'({W})-2*({wall})',f'({H})-2*({wall})',f'({x})-1',f'({y})+({wall})',f'({z})+({wall})',c,'construction')
    o=d.addObject('Part::Cut',name);g.addObject(o);o.Base=a;o.Tool=b
    return tag(o,c,evidence='CAD-P04;CAD-P06',note='Rectangular member / visible end. Numeric wall and section are illustrative, not fabrication dimensions.')
def mount(d):
    g=group(d,'FixedCartFrame','Gray rectangular frame / remains on chassis','CAD-P04;CAD-P06;CAD-U06;CAD-U07');objects=[]
    prop(g,'MemberOrdering','CAD-U07: fore/aft members below gray frame; transverse crossmember above. Numeric joint planes/sections/attachments unmeasured.')
    for i,s in enumerate([-1,1]):
        y=f'{s}*Parameters.frame_width/2'+('-Parameters.frame_wall' if s>0 else '')
        yf='Parameters.frame_width/2-Parameters.frame_flange_width' if s>0 else '-Parameters.frame_width/2'
        objects.append(box(d,g,'FrameSideWeb'+str(i),'Parameters.frame_length','Parameters.frame_wall','Parameters.frame_web_height','Parameters.frame_offset_x-Parameters.frame_length/2',y,'Parameters.frame_top_z-Parameters.frame_web_height','frame',note='Gray formed member observed. Open-section web/flange is a simplified profile; exact section unknown.'))
        objects.append(box(d,g,'FrameSideFlange'+str(i),'Parameters.frame_length','Parameters.frame_flange_width','Parameters.frame_wall','Parameters.frame_offset_x-Parameters.frame_length/2',yf,'Parameters.frame_top_z-Parameters.frame_wall','frame'))
        x=f'Parameters.frame_offset_x+{s}*Parameters.frame_length/2'+('-Parameters.frame_wall' if s>0 else '')
        xf='Parameters.frame_offset_x+Parameters.frame_length/2-Parameters.frame_flange_width' if s>0 else 'Parameters.frame_offset_x-Parameters.frame_length/2'
        objects.append(box(d,g,'FrameEndWeb'+str(i),'Parameters.frame_wall','Parameters.frame_width','Parameters.frame_web_height',x,'-Parameters.frame_width/2','Parameters.frame_top_z-Parameters.frame_web_height','frame'))
        objects.append(box(d,g,'FrameEndFlange'+str(i),'Parameters.frame_flange_width','Parameters.frame_width','Parameters.frame_wall',xf,'-Parameters.frame_width/2','Parameters.frame_top_z-Parameters.frame_wall','frame'))
    objects.append(box(d,g,'FrameCrosspiece',45,'Parameters.frame_width-2*Parameters.frame_wall',25,-150,'-Parameters.frame_width/2+Parameters.frame_wall','Parameters.frame_top_z','frame',note='Transverse crosspiece seen in CAD-P04. Section, exact location and connections unmeasured.'))
    for i,s in enumerate([-1,1]):
        y=f'{s}*Parameters.inner_spacing/2-Parameters.inner_section/2'
        objects.append(square_tube(d,g,'InnerRail'+str(i),'Parameters.inner_length','Parameters.inner_section','Parameters.inner_section','Parameters.inner_offset_x-Parameters.inner_length/2',y,'Parameters.inner_z','Parameters.inner_wall'))
        objects.append(square_tube(d,g,'PurpleEnd'+str(i),.8,'Parameters.inner_section','Parameters.inner_section','Parameters.inner_offset_x+Parameters.inner_length/2',y,'Parameters.inner_z','Parameters.inner_wall','purple'))
        o=cylinder(d,g,'FrameFastenerFace'+str(i),7,3,'Parameters.frame_offset_x+Parameters.frame_length/2',f'{s}*Parameters.inner_spacing/2','Parameters.frame_top_z-13','fastener','x')
        prop(o,'ReviewNote','Visible gold-colored fastener appearance only; no diameter, thread, grade or material identification.')
    objects.append(box(d,g,'LightSpacerEnvelope',100,185,'Parameters.inner_z-Parameters.chassis_z-30',135,-92.5,'Parameters.chassis_z+30','white',note='Light-colored interface seen in CAD-P06; material, fasteners and load transfer unverified.'))
    rod=cylinder(d,g,'SlenderTransverseMember',2.2,'Parameters.frame_width-40','Parameters.frame_offset_x+Parameters.frame_length/2-20','Parameters.frame_width/2-20','Parameters.frame_top_z+12','metal','y');prop(rod,'ReviewNote','Thin transverse member observed. Section and mechanical role unknown.');objects.append(rod)
    brackets=group(d,'TubBrackets','Observed tub brackets / pose membership approximate','CAD-P06')
    for i,s in enumerate([-1,1]):
        y=f'{s}*(Parameters.frame_width/2-32)'
        objects.append(box(d,brackets,'TubBracketWeb'+str(i),4,45,'Parameters.bracket_height','Parameters.frame_offset_x+Parameters.frame_length/2-4',f'({y})-22.5','Parameters.mount_z-Parameters.bracket_height','frame',note='Upturned bracket appearance. Exact release/hinge interfaces and moving membership not resolved.'))
        objects.append(box(d,brackets,'TubBracketFlange'+str(i),45,45,3,'Parameters.frame_offset_x+Parameters.frame_length/2-30',f'({y})-22.5','Parameters.mount_z-3','frame'))
        objects.append(cylinder(d,brackets,'TubWasher'+str(i),10,2,'Parameters.frame_offset_x+Parameters.frame_length/2-15',y,'Parameters.mount_z-5','fastener'))
        h=d.addObject('Part::Prism','TubFastener'+str(i));brackets.addObject(h);h.Polygon=6;h.Circumradius=7;h.Height=6
        ex(h,'Placement.Base.x','Parameters.frame_offset_x+Parameters.frame_length/2-15');ex(h,'Placement.Base.y',y);ex(h,'Placement.Base.z','Parameters.mount_z-11')
        tag(h,'fastener',evidence='CAD-P06',note='Visible head/nut proxy only. No thread, grade, material, torque or drilling specification.');objects.append(h)
    for o in objects:prop(o,'AppearanceEvidence','CAD-P04;CAD-P06;CAD-U03;CAD-U06')
    return objects
def tipping(d):
    pivot=group(d,'TubTipPivot','Rear tub hinge / editable visual pose','CAD-U04;CAD-U05;CAD-U06')
    ex(pivot,'Placement.Base.x','Parameters.hinge_x');ex(pivot,'Placement.Base.z','Parameters.hinge_z')
    pivot.Placement.Rotation=App.Rotation(App.Vector(0,-1,0),1);ex(pivot,'Placement.Rotation.Angle','Parameters.tub_tip_angle_deg*1 deg')
    prop(pivot,'KinematicQualification','Rear hinge and fixed gray frame owner-confirmed. Numeric axis location, angle/travel, latch and minor bracket membership unmeasured; no clearance certification.')
    rest=group(d,'TubRestOffset','Rest-position compensation');pivot.addObject(rest)
    ex(rest,'Placement.Base.x','-Parameters.hinge_x');ex(rest,'Placement.Base.z','-Parameters.hinge_z')
    for name in ['Cart','ElectronicsCase','BatteryCorner','TubAccessories','TubBrackets']:rest.addObject(d.getObject(name))
    axis=d.addObject('Part::Feature','RearHingeAxisReference');axis.Shape=Part.makeLine(App.Vector(0,-180,0),App.Vector(0,180,0))
    ex(axis,'Placement.Base.x','Parameters.hinge_x');ex(axis,'Placement.Base.z','Parameters.hinge_z');tag(axis,'reference','reference','CAD-U05','Rear transverse axis reference only; position unmeasured, actual hinge construction omitted.')
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
    objects.append(softbox(d,g,'FrontAxleRedHousing',58,68,52,'Parameters.wheelbase/2-29',-34,'Parameters.tyre_radius-52','red',r=5,note='Red front axle-center appearance from CAD-P06. Exact part identity/section unverified; not a bumper-top feature.'))
    suspension=group(d,'FrontSuspension','Observed front coilovers / angled guard proxies','CAD-P06')
    for i,s in enumerate([-1,1]):
        objects.append(cylinder(d,suspension,'FrontDamperBody'+str(i),7,'Parameters.front_shock_height-15','Parameters.wheelbase/2-25',f'{s}*110','Parameters.front_shock_z+7','chassis'))
        objects.append(cylinder(d,suspension,'FrontDamperRod'+str(i),3,'Parameters.front_shock_height+15','Parameters.wheelbase/2-25',f'{s}*110','Parameters.front_shock_z-10','metal'))
        helix=Part.makeHelix(V['front_shock_height']/6,V['front_shock_height'],10)
        section=Part.Wire([Part.makeCircle(1.5,App.Vector(10,0,0),App.Vector(0,10*2*math.pi/(V['front_shock_height']/6),1))])
        o=d.addObject('Part::Feature','FrontSpring'+str(i));suspension.addObject(o);o.Shape=helix.makePipeShell([section],True,True)
        ex(o,'Placement.Base.x','Parameters.wheelbase/2-25');ex(o,'Placement.Base.y',f'{s}*110');ex(o,'Placement.Base.z','Parameters.front_shock_z')
        tag(o,'spring',evidence='CAD-P06',note='Cosmetic spring envelope. Pitch, wire, rate, travel and mount details unmeasured; regenerate after spring-height edits.');objects.append(o)
        f=box(d,suspension,'FrontGuard'+str(i),120,60,4,'Parameters.wheelbase/2-85',f'{s}*145-30',190,'chassis',note='Angled guard appearance from CAD-P06; attachment/profile unmeasured.')
        f.Placement.Rotation=App.Rotation(App.Vector(0,1,0),-25);objects.append(f)
    for o in objects:
        if o.Name.startswith(('FrontAxleRedHousing','FrontDamper','FrontSpring','FrontGuard')):prop(o,'AppearanceEvidence','CAD-P06')
    return objects
def build():
    for name,label,builder in [('v2_cart_mount','Cart supports',mount),('v2_battery_mount','Blue pack / adapter corner',dock),('v2_electronics_enclosure','External enclosure',enclosure),('v2_sensor_mounts','Front lighting / reserved sensor interface',lighting)]:
        d=newdoc(name,label);finish(d,builder(d))
    d=newdoc('v2_assembly','LitterBuggy V2 photo-informed assembly')
    objects=chassis(d)+mount(d)+tub(d)+enclosure(d,True)+dock(d,True)+accessories(d)+lighting(d,True);tipping(d);finish(d,objects)
    (OUT/'review-meshes.json').write_text(json.dumps(meshes,separators=(',',':')),encoding='utf-8')
    (OUT/'review-poses.json').write_text(json.dumps(poses,separators=(',',':')),encoding='utf-8')
    (OUT/'geometry-checks.json').write_text(json.dumps({'revision':'CAD-R3','FreeCAD_version':App.Version(),'checks':checks,'note':'Geometry/STEP checks only; dimensions, fit, joints, travel and load capacity unverified. Bucket omitted by owner. Gray frame fixed and normal rear hinge owner-confirmed. Raw photos excluded from Git.'},indent=2),encoding='utf-8')
    print('CAD-R3: five native/STEP documents saved and reopened;',len(checks),'component records')
if __name__=='__main__':build()
