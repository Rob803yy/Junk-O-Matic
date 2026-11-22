# QElectroTech power draft R0

`v2_electrical.qet` is self-contained: module symbols are embedded in the project,
and wires reference actual QET terminals. It has three sheets: auxiliary source,
converter/load branches and propulsion. The checked PDF was exported by the native
QElectroTech 0.200.1 Qt6 runtime after opening/re-saving the generated project.

Every drawn net is proposed/untraced and labelled TBD. Module terminal names are
logical functions, not connector pin numbers. F1/S1 boxes include functional
return bypasses; this does not assert fuse/switch contacts on the return conductor.
No internal converter isolation or shared ground is assumed. Source ratings,
fuse values, protection placement and voltage settings are unresolved.

Uno power entry, ESC/motor phases, receiver/BEC/servo channels and optional
sensor/camera power entries remain open instead of guessed. The blue adapter's
wire colours are visible; polarity and cutoff are not established by appearance.
Treat this as a module-level electrical draft, not a released wiring instruction.

Generate with `python scripts/v2/build_power.py`. For application normalization:

```text
QElectroTech --resave v2_electrical.qet normalized.qet
```

After checking the normalized file, replace the generated file with it and export
using the same application version:

```text
QElectroTech --export-pdf v2_electrical.qet v2_electrical.pdf
```

Older releases may not expose the headless switches; use their graphical open,
save and PDF export instead. Native export validates compatibility and layout,
not circuit correctness or the physical system.
