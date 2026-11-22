Suggested title: Align legacy folders and evidence guidance with the current V2 review

Older folder entry points still present Nano/Pi4 wiring assumptions, legacy logger
outputs and example metrics beside the newer Uno/CAD/architecture sources. This
change routes current work to CFG-V2-R1 / ARCH-R2 / CAD-R3, preserves historical
material with explicit scope, and records 20 gaps in severity order with Six
Thinking Hats decisions and remaining evidence needs.

The legacy logger was shown offline to count a V2 frame as a row with blank
measurements. Original firmware/logger and example data remain unchanged and
clearly separated from current acquisition. Two bounded tool corrections add
dashboard provenance notices and an inventory scanner that reports only scanned
filename counts, keeps unparsed annotations/classes unknown and refuses accidental
output replacement. Issue templates, environment/data dictionaries and a physical
evidence plan now use configuration-specific records.

Validation: eight inventory behavior tests passed; revised/new local Markdown
links, register/citation structure, Python syntax, preserved source blobs and all
13 held PDF hashes passed. No firmware upload, Pi deployment, physical test,
dashboard browser run or native engineering requalification was performed.
Original engineering receipts and editable CAD/QET/WireViz/Office files are
unchanged. License content was excluded as requested. PDF generation remains held.

Prepared About text is included for the later repository-settings update; it has
not been applied remotely. Physical evidence gaps and deferred legacy runtime/CI
work remain explicitly open. Start review at [the alignment report](README.md).
