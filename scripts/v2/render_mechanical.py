"""Generate current CAD-R3 SVG/PNG previews. PDF generation remains held."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().with_name('cad_preview.py')),run_name='__main__')
