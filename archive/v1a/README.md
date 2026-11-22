# V1A archive / historical instrumented-RC scaffold

Current draft: [Elegoo Uno R3 / V2 acquisition](../../software/v2/arduino/README.md)
and [Pi logger](../../software/v2/raspberry_pi/README.md).

| Reference | Scope |
| --- | --- |
| [Arduino stub](software/arduino/README.md) | Preserved source emits fixed example values, not physical measurements |
| [Pi logger](software/raspberry_pi/README.md) | Legacy permissive parser can count V2 frames with blank measurement columns; not compatible with the new contract |
| [Old scope](docs/project_scope_v1a.md) / [procedure](docs/test_procedure_v1a.md) / [exit targets](docs/v1_to_v2_exit_criteria.md) | Historical proposals, not current fitted hardware or passed gates |
| [Sample CSVs](validation/sample_data/README.md) | Legacy format examples with no accepted field-run provenance |
| [Former BOM entry](hardware/bom/README.md), [wiring entry](hardware/wiring_diagrams/README.md), [enclosure entry](hardware/enclosure_layout/README.md) | Preserved former navigation pages; current sources are linked from them |

Executable/config bytes and the four CSV examples are unchanged. New README links
only route historical references correctly. The legacy program's relative default
paths are preserved under this directory; it is not selected by root requirements
or the current quick start. No legacy program was uploaded or deployed by cleanup.
See [contract differences](../../docs/data_dictionary.md) before examining an old run.
