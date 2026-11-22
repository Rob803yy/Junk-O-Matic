"""Check native CAD-R3 geometry, frame/tipping parameters and STEP placement."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'hardware/v2/mechanical';OUT=BASE/'exports'
cfg=json.loads((BASE/'dimensions.json').read_text());meshes=json.loads((OUT/'review-meshes.json').read_text());report=[]
rows={k:'B'+str(i) for i,k in enumerate(cfg['parameters'],3)}
def world(o):s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def close(a,b,tol=.001):assert abs(a-b)<tol,(a,b)
def edit(d,k,delta):
    old=cfg['parameters'][k]['layout_mm'];d.Parameters.set(rows[k],str(old+delta));d.recompute();return old
files=sorted(BASE.glob('*.FCStd'));assert len(files)==5
for p in files:
    d=App.openDocument(str(p));d.recompute()
    shapes=[o for o in d.Objects if hasattr(o,'Shape')]
    assert shapes and all(not o.Shape.isNull() and o.Shape.isValid() for o in shapes),p.name
    sketches=[o for o in d.Objects if o.TypeId=='Sketcher::SketchObject']
    assert all(o.FullyConstrained for o in sketches),[(o.Name,o.FullyConstrained) for o in sketches]
    details={'file':p.name,'reopened':True,'all_shapes_valid':True,'constrained_sketches':len(sketches),'checks':[]}
    if p.stem=='v2_assembly':
        a=world(d.Tyre10).BoundBox.Center;b=world(d.Tyre00).BoundBox.Center;c=world(d.Tyre11).BoundBox.Center
        close(abs(a.x-b.x),cfg['parameters']['wheelbase']['layout_mm']);close(abs(a.y-c.y),cfg['parameters']['track_centres']['layout_mm'])
        old=edit(d,'wheelbase',20);close(abs(world(d.Tyre10).BoundBox.Center.x-world(d.Tyre00).BoundBox.Center.x),old+20);d.Parameters.set(rows['wheelbase'],str(old));d.recompute()
        tub=world(d.CartTub);v=cfg['parameters'];z=v['mount_z']['layout_mm'];x=v['cart_offset_x']['layout_mm'];h=v['cart_height']['layout_mm']
        close(tub.BoundBox.Center.x,x);close(tub.BoundBox.XLength,v['cart_length']['layout_mm'])
        assert tub.isInside(App.Vector(x,0,z+2),1e-5,True)
        assert not tub.isInside(App.Vector(x,0,z+h-30),1e-5,True)
        old=edit(d,'cart_length',20);close(world(d.CartTub).BoundBox.XLength,old+20);assert d.CartTub.Shape.isValid();d.Parameters.set(rows['cart_length'],str(old));d.recompute()
        case=world(d.EnclosureShell);rim=world(d.RolledRim);pack=world(d.BluePack)
        assert case.common(world(d.CartTub)).Volume<.001,'Enclosure intersects tub'
        assert case.common(rim).Volume<.001,'Enclosure intersects rim'
        assert case.common(pack).Volume<.001,'Enclosure intersects blue pack'
        old=edit(d,'enclosure_height',10);close(world(d.EnclosureShell).BoundBox.ZLength,old+10);d.Parameters.set(rows['enclosure_height'],str(old));d.recompute()
        assert d.getObject('UnselectedSensorReference') is None
        assert all('Bucket' not in o.Name and 'HistoricalTransducer' not in o.Name for o in d.Objects)
        assert d.getObject('VisibleSideStrip0') is None and d.getObject('BumperRedDetail') is None
        rail=world(d.InnerRail0);cy=-v['inner_spacing']['layout_mm']/2;cz=v['inner_z']['layout_mm']+v['inner_section']['layout_mm']/2
        assert not rail.isInside(App.Vector(0,cy,cz),1e-5,True),'Inner rail incorrectly filled'
        assert rail.isInside(App.Vector(0,cy+v['inner_section']['layout_mm']/2-1,cz),1e-5,True),'Inner rail missing wall'
        for inner in [d.InnerRail0,d.InnerRail1]:
            for outer in [d.FrameEndWeb0,d.FrameEndWeb1]:assert world(inner).common(world(outer)).Volume<.001,'Inner member penetrates gray frame'
        assert world(d.InnerRail0).BoundBox.ZMax<=world(d.FrameEndWeb0).BoundBox.ZMin+.001
        assert world(d.FrameCrosspiece).BoundBox.ZMin>=world(d.FrameSideWeb0).BoundBox.ZMax-.001
        width=v['frame_width']['layout_mm'];old=edit(d,'frame_width',20)
        close(world(d.FrameSideWeb1).BoundBox.YMax-world(d.FrameSideWeb0).BoundBox.YMin,width+20);d.Parameters.set(rows['frame_width'],str(old));d.recompute()
        frame_before=world(d.FrameSideWeb0).BoundBox;cart_before=world(d.CartTub).BoundBox
        tipcell=rows['tub_tip_angle_deg'];d.Parameters.set(tipcell,str(v['service_pose_angle_deg']['layout_deg']));d.recompute()
        frame_after=world(d.FrameSideWeb0).BoundBox
        for name in ['XMin','YMin','ZMin','XMax','YMax','ZMax']:close(getattr(frame_before,name),getattr(frame_after,name))
        assert world(d.CartTub).BoundBox.ZMax>cart_before.ZMax+100,'Tub failed to tip upward'
        assert d.TubTipPivot.Placement.Base.x<0 and d.TubTipPivot.Placement.Rotation.Axis.y<0
        assert all(world(d.getObject(o['name'])).isValid() for o in meshes[p.stem])
        d.Parameters.set(tipcell,'0');d.recompute();close(world(d.CartTub).BoundBox.ZMax,cart_before.ZMax)
        close(world(d.FrontAxleRedHousing).BoundBox.ZMax,v['tyre_radius']['layout_mm'])
        details['checks']=['wheel centre geometry','wheelbase edit moves tyres','tub centre/length and open interior','cart-length edit regenerates native loft/cut','case height edit in vertical orientation','limited draft clashes: case/tub, case/rim, case/pack','no bucket or historical ultrasonic in assembly']
        details['checks']+=['inner rail hollow profile','owner-confirmed longitudinal-below/transverse-above ordering, without rail/end-web penetration','frame-width edit propagates','rear-axis tub tipping with stationary outer frame','normal pose restored and shape validity at illustrative tip angle','red housing below axle centre; old bumper-top/vertical-strip interpretations removed']
    leaves=[world(d.getObject(o['name'])) for o in meshes[p.stem]]
    native=Part.makeCompound(leaves);step=Part.Shape();step.read(str(OUT/(p.stem+'.step')))
    assert step.isValid() and step.Volume>0
    for name in ['XMin','XMax','YMin','YMax','ZMin','ZMax']:close(getattr(native.BoundBox,name),getattr(step.BoundBox,name))
    details['step_readback_global_bounds_match']=True
    with zipfile.ZipFile(p) as zf:
        details['native_gui_state_saved']='GuiDocument.xml' in zf.namelist()
        if details['native_gui_state_saved']:
            gui=ET.fromstring(zf.read('GuiDocument.xml'));views={v.get('name'):v for v in gui.iter('ViewProvider')}
            if 'ClearLid' in views:
                assert views['ClearLid'].find(".//Property[@name='Transparency']/Integer").get('value')=='72'
                details['native_lid_transparency_verified']=True
            if 'UnselectedSensorReference' in views:
                for name in ['UnselectedSensorReference','HistoricalSensorBoard','HistoricalTransducer0','HistoricalTransducer1']:
                    assert views[name].find(".//Property[@name='Visibility']/Bool").get('value')=='false'
                details['historical_reference_hidden_verified']=True
    App.closeDocument(d.Name);report.append(details)
assert all(v.get('measured_mm',v.get('measured_deg')) is None for v in cfg['parameters'].values())
held=json.loads((ROOT/'docs/reconciliation/export-status.json').read_text())
for p in held['held_pdfs']:assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256']
summary={'revision':'CAD-R3','native_files':report,'step_readback_count':5,'measured_dimensions_entered':0,'held_pdf_count':len(held['held_pdfs']),'physical_fit_validation':'not performed','limits':['Photo-informed proportions; no scale reference','Rear hinge/fixed frame confirmed; numeric axis/travel, latch and minor bracket moving membership unverified','Clash checks cover named draft parts only, not real wiring/fasteners/full moving travel','Tread/spring shape and dock angles regenerate from source; other principal profiles/placements and tub-tip angle edit natively']}
(ROOT/'reports/v2/freecad-validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('CAD-R3: five native/STEP readbacks, frame edits, hollow members, fixed-frame tub tipping and 13 held PDF hashes passed')
