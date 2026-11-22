# Six Thinking Hats / decision record

REPO-R1, 2026-11-22. Baseline identification and severity ranking were recorded
before correction. The [gap register](gap-register.json) contains the six-lens
record for every finding; this page summarizes the selected decisions. Lenses
organize evidence and options; they do not produce physical verification.

## Evidence validity and physical scope / REV-001–004, REV-019

- **White / facts:** owner confirms Uno and mounting relationships; old pages name
  Nano/Pi4 and give untraced wiring instructions. The old sketch emits constants.
  Fake-port reproduction proves the legacy logger counts a V2 frame with blank
  measurements. Current physical traces, measurements and passed gates are absent.
- **Red / anticipated concern:** familiar-looking voltage rows and a clean run
  summary can feel more settled than their evidence supports.
- **Black / failure consequence:** selecting the wrong power/serial path or using
  example/null data can invalidate technical decisions and physical test conclusions.
- **Yellow / retained value:** old source and format examples remain useful for
  identifying history and recovering the actual installed program.
- **Green / options:** overwrite history; attempt speculative hardware reconstruction;
  or preserve history, select the current strict contract and collect missing evidence.
- **Blue / decision:** choose explicit current routing, historical containment,
  contract mapping and prioritized evidence collection. Unknown hardware values
  stay unknown; no field gate or operating permission is invented.

## Dataset/model provenance / REV-005, REV-006, REV-012

- **White:** the committed run identifies `baseline-placeholder`; inventory code
  copied configured labels into observed classes and emitted zero annotations
  without parsing. Dataset bootstrap only creates directories.
- **Red:** plausible metrics and `enabled: true` can look like completed work.
- **Black:** documentation or funding/build decisions could cite nonexistent
  evaluation, dataset coverage or integrated perception capability.
- **Yellow:** keep the lightweight dashboard, taxonomy and report examples as a
  useful starting workspace rather than delete them.
- **Green:** build a full perception stack now; leave unsupported claims; or add
  provenance notices and report only what the scanner actually observes.
- **Blue:** choose notices plus a bounded scanner correction. Missing/disabled
  roots and unparsed annotations/classes remain explicit; preserve fixture JSON.
  Real ingestion, mappings, training and evaluation remain separate work.

## Finding the right source / REV-008–011, REV-015, REV-017, REV-020

- **White:** parent folders and issue templates still name legacy outputs while
  QET/WireViz/CAD/current code already exist. The owner's screenshot sidebar
  describes autonomy/sorting beyond current reconstruction evidence.
- **Red:** contradictory entry points can make a reviewer unsure which file to edit.
- **Black:** parallel BOMs, schemas or issue records can attach results to the
  wrong vehicle configuration and lose traceability.
- **Yellow:** stable old paths and full historical snapshots preserve useful links
  while a short current index makes the project approachable.
- **Green:** move/delete every legacy folder; duplicate current files into each;
  or keep locations and route them to one authoritative source per subject.
- **Blue:** choose routing tables, compatibility/setup guidance, configuration-aware
  templates and a dated per-file review record. Prepare About wording for posting;
  remote metadata remains unchanged in this local preparation pass.

## Scope, regeneration and maintenance / REV-007, REV-013, REV-014, REV-016, REV-018

- **White:** old logger limits are visible in source; validation counts belong to
  specific revisions. Some generators overwrite native files; the held book still
  assembles R0 PDFs. Helper duplication and lack of CI are present.
- **Red:** a successful rebuild or new timestamp can create unjustified confidence.
- **Black:** rerunning everything can erase manual edits, replace original receipts
  or package stale drawings without resolving a physical claim.
- **Yellow:** retain trustworthy scoped receipts and useful native tools while
  avoiding a broad code/dependency rewrite during document alignment.
- **Green:** refactor all legacy code/install CI now; ignore limitations; or record
  them and add a narrow offline review check with protected-source comparisons.
- **Blue:** choose scoped documentation/tool checks and explicit overwrite boundaries.
  Do not rerun unrelated firmware/CAD suites or generate PDFs. Legacy runtime
  repair, helper consolidation, dependency locking and CI remain clearly deferred.
