# Wiring review entry / current V2

This page routes to the current review sources. The former instructions are
[preserved as historical V1A notes](../archive/reference-pages/v1a-wiring-notes.md); they are not a
current connection or grounding plan.

Read [ARCH-R2 power domains](../hardware/v2/architecture/v2_power_domains.drawio),
the [three-sheet QET source](../hardware/v2/electrical/README.md),
[WireViz harnesses/registers](../hardware/v2/wiring/README.md) and
[normalized BOM](v2/bom.json) together. All drawn electrical paths remain
proposed/untraced. Functional terminal labels are not physical connector pins.

- Uno R3 identity is confirmed; external supply entry and simultaneous USB power
  remain open. No buck-to-Uno feed is selected by the documentation.
- Pi 3B/Pi 4 remains conflicting. Read its actual label/OS and power connector.
- 3S propulsion and Kobalt 24V-family auxiliary power are project scope; exact
  packs, cutoff, ratings, polarity and protection need physical evidence.
- U5 5V/10A and separate U5A 5V/3A are source-listed ratings, not measured capacity.
  U5A routing/load remains OPEN; no parallel or backup function is established.
- U12-to-lights is a proposal; actual lighting voltage/fitting is unknown.
- F1/S1/FB1 functions do not select physical order, fuse values or wire sizes.
- No shared RC/auxiliary ground or galvanic isolation is asserted. Historical
  single-point grounding language is a design proposal, not an observed net.
- Sensor identity, supply/logic compatibility, pull-ups and pins remain open.
  A02YYUW UART is not an HC-SR04 trigger/echo replacement in this code.
- Source code issues no vehicle commands; this does not prove every existing
  physical control interface has been inspected.

Use [the evidence plan](v2/verification-plan.md) to capture labels, contact views,
continuity and measured source/load details. Retain unknowns until evidence closes
the specific item; diagram arrows or lead colors are not polarity proof.
