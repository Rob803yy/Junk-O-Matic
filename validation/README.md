# Validation evidence / current V2 versus historical examples

Start with [the V2 evidence plan](../docs/v2/verification-plan.md),
[revision-scoped check receipts](../docs/v2/validation.md) and
[verification register](../docs/v2_verification/README.md). The actual physical
configuration, method and raw evidence must be identified before recording a
result. Confirmed/source-only code behavior is not a passed physical test.

| Material | Disposition |
| --- | --- |
| Archived V1A sample CSVs | Legacy format examples with no accepted run provenance; [labels/limits](../archive/v1a/validation/sample_data/README.md) |
| [Scorecard guidance](scorecard/README.md) | Manual evidence interpretation; no automatic V2 summary mapping implemented |
| [V1A procedure](../archive/v1a/docs/test_procedure_v1a.md) | Historical only; output names, field meanings and capabilities differ |
| [V1A exit targets](../archive/v1a/docs/v1_to_v2_exit_criteria.md) | Historical proposed thresholds; not adopted or passed for current V2 |
| Software replay/compile/native-file checks | Scoped to source/artifact behavior; no upload, field run or fabricated physical result |

For every planned/result record include configuration ID, source revision,
replay/bench/field mode, exact method, units/denominator, acceptance rule status,
reviewer/date and evidence reference/hash. Keep proposed requirements distinct
from observed results. Missing score, evidence or denominator stays pending/null,
not zero, pass or automatic fail. Distinguish observed failure from a critical
classification supported by the actual evidence.

The V2 logger has no operator route-keyboard markers, voltage logging, E-stop
measurement or automatic legacy scorecard summary. CPU temperature is not enclosure
ambient; a sequence anomaly is not proof of a physical reset. Valid null frames
are not physical samples. See [the dictionary](../docs/data_dictionary.md).

Keep raw video/serial and full field archives outside Git. A bounded public record
may reference a private archive identifier/hash without exposing private paths or
personal data. No physical test or operating approval was added in REPO-R1. Historical files now live under archive/; see the
[relocation record](../archive/relocation-manifest.json).
