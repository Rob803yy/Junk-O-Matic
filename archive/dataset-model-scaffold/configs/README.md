# Dataset/taxonomy configuration scaffold / reviewed REPO-R1

The two original YAML files are preserved unchanged.

| File | Actual meaning | Not established |
| --- | --- | --- |
| `classes.yaml` | Seven configured project labels | Observed classes, dataset-label mapping, annotation coverage or trained detector |
| `datasets.yaml` | Candidate TACO detection / TrashNet classification entries and local roots | Acquired files, selected subsets/splits, verified mapping or current network availability |

`enabled: true` selects a root for preparation/scanning; it does not download or
parse a dataset. `bootstrap_datasets.py` is a directory-creation stub. Source URLs
are retained; live availability and acquisition were not tested in this review.

The revised inventory scanner reports existing image files only. Missing roots
stay distinct from empty roots, disabled roots are not scanned, and annotations
and observed classes remain null until a parser exists. Configured labels are
reported separately. Raw dataset files belong in ignored `data/external/`; scans
write new ignored `reports/local/` output and refuse accidental overwrite.
Keep public source config separate from private/local device configuration.

No interface from these configs to Uno/Pi acquisition or vehicle control is
implemented. See [script commands](../../../scripts/README.md) and
[current engineering sources](../../../docs/v2/README.md).
