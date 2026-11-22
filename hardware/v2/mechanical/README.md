# V2 mechanical draft R0

Five native, parametric FreeCAD documents and matching STEP exports are provided:
assembly, cart mounting structure, battery dock/mount envelope, enclosure layout,
and sensor mount. The assembly includes chassis rails, axles, four tyres,
coilover envelopes, raised metal support, hollow cart tub, enclosure and boards,
blue dock and ultrasonic bracket. These are simplified envelopes, not reverse
engineered OEM parts.

**Every numeric dimension is illustrative.** `dimensions.json` deliberately
separates `layout_mm` from `measured_mm: null`. No dimension was recovered from
photographs without a scale. A valid solid is not an accurate fit or rated part.
No hole coordinates or dock recess function are invented. No drilling/cutting
should be based on these draft exports.

Historical photos 1963-1971 informed the raised tub, metal support members,
four-wheel chassis and coilover representation. Photos 3718-3721 informed the
blue dock/guide-rail envelope. Sampled video frames support retaining lighting
in the overall system scope, but don't establish locations or dimensions.
Enclosure/dock/sensor placement in CAD is a proposed layout. The symmetric
suspension geometry is an envelope, not a correction of the observed right lean.

Open the FCStd files and edit the **Parameters** spreadsheet. Named dimensional
expressions drive the main envelopes. Individual primitive dimensions/placements
are also editable. Rebuild all documents and STEP exports by running
`build_models.FCMacro` using the FreeCAD Python runtime (set macro `__file__`
when invoking by exec from a console), then run
`python scripts/v2/render_mechanical.py` with Pillow and ReportLab installed.

`exports/geometry-checks.json` records native reopen and solid validity checks;
the generator also reads back every STEP export. Review PDFs/PNGs use the same
generated geometry. The assembly PDF contains illustrative layout dimensions.
The drawings remain reference sheets until measured dimensions are entered.

First review: orientation/datum, cart/frame interface, enclosure and battery
location, mount hole patterns, extraction/latch access, wire routing, full
steering/suspension clearance, mass distribution and payload position.
