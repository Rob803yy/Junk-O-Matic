# System architecture drafts

Open `.drawio` sources in diagrams.net. Matching SVG/PDF files are review exports.
They share the same scene data in `scripts/v2/draft_drawings.py`. Regeneration
replaces manual native edits, so update scene source or preserve native edits
separately before regenerating.

Green identifies the owner-confirmed Uno identity. Blue identifies historical
media observations (evidence basis, not a fifth verification status). Orange
marks unresolved configuration/interfaces; purple marks proposed software flow.
Dashed connections are untraced/proposed. Physical power/ground isolation is not
established by drawing separate domains. Pin-to-pin details belong in the QET
and WireViz drafts and must be reconciled before a build release.
