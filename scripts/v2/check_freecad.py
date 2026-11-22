"""Check native CAD-R2 geometry, actual parameter behavior and STEP placement."""
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
        details['checks']=['wheel centre geometry','wheelbase edit moves tyres','tub centre/length and open interior','cart-length edit regenerates native loft/cut','case height edit in vertical orientation','limited draft clashes: case/tub, case/rim, case/pack','no bucket or historical ultrasonic in assembly']
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
summary={'revision':'CAD-R2','native_files':report,'step_readback_count':5,'measured_dimensions_entered':0,'held_pdf_count':len(held['held_pdfs']),'physical_fit_validation':'not performed','limits':['Photo-informed proportions; no scale reference','Clash checks cover named draft parts only, not real wiring/fasteners/moving travel','Tread shape and dock angles regenerate from source; other principal profiles/placements edit natively']}
(ROOT/'reports/v2/freecad-validation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('CAD-R2: five native/STEP readbacks, constrained profiles, parameter edits, named draft clashes and 13 held PDF hashes passed')
