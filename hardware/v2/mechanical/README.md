# CAD-R3 / photo-informed V2 mechanical review

This revision addresses owner CAD feedback on PR #3 using seven supplied photograph references
(CAD-P01..07). Four new references expose the under-frame and low front. CAD-P07
appears to repeat the CAD-P03 scene and is not an independent test. The owner confirms **yellow-handle end = FRONT** and requests the
assembly **without the removable bucket**. +X is forward, +Z up, -Y is the enclosure
side. Standalone component documents use local frames; the assembly places them.

**Member ordering confirmed by owner:** the up/down members in CAD-P04 run fore/aft beneath the gray frame; left/right transverse member(s) sit above it. Numerical joint planes, section sizes and connections remain unmeasured.

## Review files

| Native FreeCAD source | Current interpretation | Exports |
| --- | --- | --- |
| [Assembly](v2_assembly.FCStd) | Flared rounded tub, thick rim, ribs, rear-biased placement, external vertical enclosure, blue corner pack/adapter, yellow front handle, red rim lights, two white front lights, treaded wheels and bumper | [Review sheet](exports/v2_assembly.png), [STEP](exports/v2_assembly.step), [SVG](exports/v2_assembly.svg) |
| [Cart support](v2_cart_mount.FCStd) | Gray rectangular frame, inner hollow members, purple end markings, tub brackets, fastener appearances, transverse member and light-colored spacer | [Sheet](exports/v2_cart_mount.png), [STEP](exports/v2_cart_mount.step) |
| [Battery mount](v2_battery_mount.FCStd) | Blue pack-like body, dark adapter, guide/rail and unidentified release-like feature | [Sheet](exports/v2_battery_mount.png), [STEP](exports/v2_battery_mount.step) |
| [Enclosure](v2_electronics_enclosure.FCStd) | Rounded orange case, translucent lid, rim and stylized latches; internal PCB placement removed | [Sheet](exports/v2_electronics_enclosure.png), [STEP](exports/v2_electronics_enclosure.step) |
| [Front lighting / reserved sensor interface](v2_sensor_mounts.FCStd) | Two observed white light points and a bracket proxy; historical HC-SR04 reference is hidden and excluded from assembly/STEP | [Sheet](exports/v2_sensor_mounts.png), [STEP](exports/v2_sensor_mounts.step) |

Additional assembly views: [front](exports/v2_assembly_front.png),
[opposite side](exports/v2_assembly_opposite.png),
[tub hidden](exports/v2_assembly_tub_hidden.png), [large oblique](exports/v2_assembly_iso.png).
[Top under-frame view](exports/v2_mounting_frame_top.png),
[low front under-frame view](exports/v2_mounting_frame_low_front.png), and
[illustrative tipped pose](exports/v2_assembly_tipped.png) address the new photos.
The owner confirms the same mounting hardware, normal rear hinge and gray frame
remaining on the chassis. These are not verified load-path or motion-clearance drawings. No new fabrication holes or bracket design is released.

## Evidence and dimensions

[photo-observations.json](photo-observations.json) records 24 bounded observations,
source hashes and seven owner decisions. Raw field photographs stay outside
Git. Capture dates and a dimensional scale reference are absent.

**No measured dimension was introduced.** [dimensions.json](dimensions.json) and
the native Parameters spreadsheets separate layout estimates, source specifications
and UNKNOWN measurements. mm apply to lengths; *_deg parameters are angles.
The nominal enclosure catalog tuple remains 11.5 × 7.5 × 5.1in. Its broad face is
now mapped to X/Z (292.1 × 190.5mm) with 129.54mm depth along Y, matching the observed
vertical orientation. The actual enclosure model, dimensions and fit remain unverified.

Rib/tread/strip counts and cosmetic latches are stylized. The CAD-R3 open-section outer frame and hollow inner members replace the earlier
vertical-strip/generic-support interpretation. Exact member sections/joints, spacer
material, battery identity/retention, light brackets and sensor
fitting remain open. A recognizable photo-informed envelope is not an OEM replica.
The bucket's omission follows the owner's display request; photographs do show it.

## Editing and regeneration

The five native files contain named component groups and evidence properties.
Rounded profiles are fully constrained sketches driving native lofts, cuts,
fillets and tire revolutions. Main dimensions and placements edit through the
Parameters sheet without an installed custom Python proxy. Cosmetic tread/spring geometry and
compound dock angle construction require regeneration after those specific edits.
Spring display meshes are coarsened for efficient previews; native/STEP solids
retain the full swept geometry. The tub_tip_angle_deg parameter edits the native
pose directly; 0 is normal. The shown 55-degree service pose is illustrative,
not a measured limit. Hinge numerical position/orientation, latch details, minor
bracket moving membership and full travel/clearance remain unresolved. Front
light attachment is unverified and stays at its rest position in this pose.

Run build_models.FCMacro with FreeCAD Python (implementation: model_components.py).
Regeneration replaces manual native edits; preserve them or update the source first.
Run python scripts/v2/render_mechanical.py with NumPy/Pillow for PNG/SVG review
sheets. SVG annotations are editable text; its geometry previews are raster views
of the native mesh. STEP contains the selected visible solids with global placement;
construction and historical sensor reference geometry are excluded.

For native colors, visibility, lid translucency and a saved camera, run
scripts/v2/save_cad_presentation.FCMacro in FreeCAD. The checked files include this
GUI state. Run scripts/v2/check_freecad.py with FreeCAD Python for native/STEP
readbacks, fully constrained sketches, real parameter edits and limited named
draft clash checks. Successful checks do not verify real-world moving clearance,
fit, payload, material properties or structural capacity.

PDF generation remains held for owner review. Existing R0 PDFs are unchanged and
stale. R1 reconciliation Word/workbooks remain the earlier review baseline;
CAD-R3 supersedes their prior mechanical pictures/proxy descriptions only.

## Most useful next CAD feedback

1. Outer-frame member section/gauge and dimensions.
2. Inner rectangular member dimensions, spacing and end cap/plug state.
3. Spacer material/attachment and actual chassis interfaces.
4. Hinge-axis measurements, latch details and which minor brackets move.

Use CAD-001..024 observation IDs or component names when returning corrections.
