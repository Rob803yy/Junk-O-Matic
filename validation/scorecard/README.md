# Scorecard Import Guidance

The Raspberry Pi logger exports `exports/summary_for_scorecard.csv` inside each run folder.

Import that CSV into the validation scorecard to track V1.0A gates:

- Pi boot and logger start reliability
- Camera video usability
- Arduino telemetry completeness
- Pi reset or thermal issues
- 5V and 12V rail stability
- Manifest creation
- Summary export creation
- Field session duration
- Event marker use
- Evidence folder traceability

The scorecard should link to the local or OneDrive evidence folder rather than storing raw media in GitHub.
