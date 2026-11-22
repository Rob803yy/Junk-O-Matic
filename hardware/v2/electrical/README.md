# Three-sheet QElectroTech power draft / R1

v2_electrical.qet is self-contained with embedded symbols and terminal-linked
conductors. Sheets cover auxiliary source/distribution, converters/loads and RC
propulsion. QElectroTech 0.200.1 opened/re-saved the project and produced current
PNG previews in exports/. Native PNG previews were inspected.

U5A is the separate source-listed 5V 3A converter (S04 C33), shown OPEN; its input,
load and any connection to U5 are not inferred. U5 10A and U12 5A are source
specifications, not verified operating capabilities. The Pi model is conflicting.
KB624-03 is a battery-model designation, not an identified fuse/switch. All fuse
values, polarity, settings, actual protection order and returns remain unverified.

Every drawn net is a proposed/untraced review hypothesis labelled TBD. Terminal
functions are logical, not physical pin numbers. F1/S1 return paths depict bypass
roles, not fuse/switch contacts on return. No common ground or isolation is
asserted. Uno external supply and simultaneous USB power remain open. No motor
phases, RC channels or new motion-control connections are invented.

Generate with python scripts/v2/build_power.py, then open/re-save in QET. The
native commands used here are --resave INPUT OUTPUT and --export-png INPUT DIR.
The application's SVG export scaled symbol pictures by 0.75 while leaving wires
unscaled in this runtime; those defective SVG derivatives are excluded. Native
PNG and source are the current review materials. PDFs remain unchanged and stale
for R1 until owner review. Native compatibility is not circuit verification.
