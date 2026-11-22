# Decisions and build sequence

| Decision | Current disposition | Evidence/change needed |
| --- | --- | --- |
| V3 mission / motion authority | Owner-confirmed assisted mission and manual RC requirement | Demonstrate software/physical interfaces honor it; no fitted-control claim follows from the scope answer |
| Uno and serial version | Proposed reuse of existing acquisition and protocol 2 | Match actual sensor build and retain strict regression behavior |
| Camera part and USB/CSI interface | Unknown | Identify/select one camera and its field of view, power, connector, format and supported capture path |
| Pi / accelerator | Existing Pi model conflicting; upgrade unselected | Read actual board/OS and benchmark concurrent recording/inference/archive before choosing any replacement |
| Camera mount | Proposed; no location/dimensions chosen | Compare fixed-frame versus moving-tub positions, sightlines, cable motion and access using measured interfaces |
| Alert channel | Proposed operator visual display first | Select viewer/location/link and stale/acknowledgment behavior; no mandatory new buzzer or MCU command path |
| Runtime/data storage | Proposed reuse of telemetry core plus additive sidecars | Define schemas/IDs/failure states, orchestration and bounded resource handling |
| Model / labels | Unknown model; seven old labels are candidate names | Define rubric, representative data/splits, preprocessing and baseline/evaluation artifacts |
| Numerical performance gates | Unknown / unselected | Set latency, freshness, coverage, false-alert/detection and thermal/storage limits after baseline measurements |
| Private storage / transfer | Destination unselected; manual verified transfer first | Select archive location and verify finalized source/destination hashes before optional unattended uploading |
| PDFs / historical evidence | Existing 13 PDFs held unchanged; old results remain scoped | Regenerate/proof changed current derivatives only after owner content review; never copy old passes into V3 |

## Work order

1. **System overview first:** derive three V3 architecture diagrams plus digital
   connectivity, using the confirmed mission and explicit unknown interfaces.
2. **Power schematic:** select camera/compute interface and establish actual load,
   source/return/USB behavior and protection requirements before detailed net edits.
3. **Wiring:** update the two harnesses/registers and proper complete camera cable
   after physical connector/part selection. No guessed USB contacts or GPIO pins.
4. **Mechanical assembly:** develop camera mounting and affected enclosure/cable
   interfaces; retain the five-model structure and measured-versus-layout status.
5. **Firmware/Pi software:** retain Uno/serial where unchanged; implement V3 frame,
   perception, alert, context, review and transfer modules with explicit schemas.
6. **Offline/bench evidence:** validate synthetic error/empty/stale/drop contracts,
   then real camera/compute/power/timing and operator behavior on known hardware.
7. **Controlled field/data/model loop:** labeled original runs, independent model
   evaluation and advisory-only observation trials with measured performance.
8. **Technical review/release:** reconcile all affected BOM/drawing/code/test/Office
   references, then generate/proof PDFs under a new export record after content review.

The next native engineering file is the V3 system overview. The present package
prepares its inputs and the complete file impact plan; it does not pretend that
the later native files, runtime or bench results already exist.
