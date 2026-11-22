# Five mechanical review models / R1

The assembly, cart mount, battery dock/mount envelope, electronics enclosure and
sensor mount are native parametric FreeCAD documents with STEP and SVG reference
drawings. PNG previews accompany them. Parameters sheets contain provenance and
UNKNOWN measured values. Editable models are simplified review proxies.

dimensions.json separates layout_mm, optional source_spec_mm and measured_mm.
**Every measured_mm remains null.** Enclosure envelope 292.1 × 190.5 × 129.54mm
is an unverified source catalog claim (S04 V1.0 C16: 11.5 × 7.5 × 5.1 inches),
not a measurement of the actual orange box. Other numeric values are illustrative
layout choices. No photograph was scaled into an as-built dimension. Stock
overall width is not a tyre-centre track measurement.

The raised tub/support relationship follows historical media. RevB rail pods,
four-post/five-truss cradle, closed ring, detachable Case4 module and trailer in
S11 are future/source proposals. No fit, strength, suspension clearance or payload
rating is established. The HC-SR04 geometry is a historical profile reported lost
in S06; final sensor/mount selection is open. Pi3B/Pi4 identity is unresolved.

Run build_models.FCMacro with FreeCAD Python to regenerate native/STEP/mesh files.
Run python scripts/v2/render_mechanical.py for current SVG/PNG source sheets; it
does not generate PDFs by default. Existing R0 PDFs remain stale and held until
owner review. Do not fabricate or drill from these proxies. STEP carries geometry;
retain the native file and parameter JSON for provenance and editable expressions.

FreeCAD reopened every native file and STEP, checked solid validity and tested
wheelbase parameter propagation and tyre-centre geometry. These are software
geometry checks only. Physical measurement, datum, hole patterns, latch/slide
access, steering/suspension travel and mass distribution need technical review.
