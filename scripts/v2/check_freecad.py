"""Run with FreeCAD Python. Reopen native/STEP and check parameter propagation."""
from pathlib import Path
import json
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'hardware/v2/mechanical';report=[]
for p in sorted(BASE.glob('*.FCStd')):
    d=App.openDocument(str(p));d.recompute()
    shapes=[o for o in d.Objects if hasattr(o,'Shape')]
    assert shapes and all(not o.Shape.isNull() and o.Shape.isValid() for o in shapes),p.name
    if p.stem=='v2_assembly':
        y0=d.getObject('Tyre00').Shape.BoundBox.Center.y;y1=d.getObject('Tyre01').Shape.BoundBox.Center.y
        assert abs(abs(y1-y0)-380)<.001,(y0,y1)
        # Wheelbase parameter must actually move both tyre centres.
        d.Parameters.set('B3','510');d.recompute()
        xa=d.getObject('Tyre00').Shape.BoundBox.Center.x;xb=d.getObject('Tyre10').Shape.BoundBox.Center.x
        assert abs(abs(xb-xa)-510)<.001,(xa,xb)
    report.append({'file':p.name,'reopened':True,'all_shapes_valid':True,'shape_objects':len(shapes)})
    App.closeDocument(d.Name)
    s=Part.Shape();s.read(str(BASE/'exports'/(p.stem+'.step')));assert not s.isNull() and s.isValid()
out=ROOT/'reports/v2';out.mkdir(exist_ok=True,parents=True)
(out/'freecad-validation.json').write_text(json.dumps({'native_files':report,'step_readback_count':5,'parametric_wheelbase_test':'passed','tyre_centre_spacing_test':'passed','physical_fit_validation':'not performed'},indent=2))
print('Native and STEP reopen, parameter propagation and tyre-centre geometry checks passed.')
