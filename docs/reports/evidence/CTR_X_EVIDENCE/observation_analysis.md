# CTR.X Observation Analysis Evidence

## Source search

Searched existing JSON evidence for:

- `ctr_shadow_comparison`
- dry-run planner output
- observation window output

Result:

- Existing production dry-run files exist.
- Existing production dry-run files do not contain `ctr_shadow_comparison`.
- `rg -l 'ctr_shadow_comparison' . --glob '*.json'` found no matching JSON plan files.

## Aggregated observation window

Generated:

- `docs/reports/evidence/CTR_I5_EVIDENCE/existing_production_dry_run_observation_window.json`

Result:

- usable_cycles=0
- shadow_cycles=0
- comparison_cycles=0
- positive_changes=0
- negative_changes=0
- neutral_changes=0
- ctr_usefulness_score=50.0
- ctr_confidence_score=0.0
- final_verdict=INSUFFICIENT_DATA

## Interpretation

CTR production value cannot be certified from historical dry-run evidence because the historical dry-runs were captured before CTR.I4 shadow comparison existed in planner output.

