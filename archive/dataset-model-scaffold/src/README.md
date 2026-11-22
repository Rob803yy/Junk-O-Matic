# Python helper scaffold / historical dataset workspace

`junkomatic/config.py` loads YAML/JSON; `junkomatic/reporting.py` enumerates run
JSON and silently skips JSON decoding errors. `__init__.py` supplies only the
package marker. There is no build/installation metadata, deployed entry point,
model inference, sensor driver or vehicle-control API here.

The dashboard duplicates some of these loaders and does not import this package.
Treat any direct use as a repository helper, not a validated ingestion contract.
Schema/provenance validation, skipped-file diagnostics, path portability and API
consolidation remain optional implementation work. Source files are preserved
unchanged in this document pass; the current acquisition implementation is
[software/v2](../../../software/v2/raspberry_pi/README.md).
