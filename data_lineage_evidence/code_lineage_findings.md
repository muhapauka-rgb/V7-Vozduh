# Code Lineage Findings

## Key Files

- `admin_core/intelligence_platform.py`
- `admin_core/intelligence_workers.py`
- `admin_core/intelligence_snapshots.py`
- `tools/v7-intelligence-snapshot-refresh`

## RI6 Model Inputs Exist

`admin_core/intelligence_platform.py` defines:

- `decision_outcome_framework(records)`
- `prediction_accuracy_model(forecasts, actuals)`
- `suitability_trust_model(candidate_rows, outcomes)`
- `rollback_intelligence_model(records)`
- `trust_evolution_summary(...)`

The platform is structurally able to consume outcomes.

## Worker Consumption Break

`admin_core/intelligence_workers.py` builds trust evolution from:

- bounded decision records from audit/switch/rollback;
- prediction forecast rows from `prediction-summaries`;
- service rows from service and channel service snapshots;
- candidate rows from `candidate-suitability-summary`.

But it passes:

- `prediction_actuals=[]`
- `service_actuals=[]`
- `candidate_outcomes=[]`

This directly explains zero live outcome calibration for prediction and suitability trust.

## Snapshot Builder Coverage

`build_all_snapshots(...)` builds 11 snapshot families:

- service scores
- channel service scores
- trust summaries
- risk summaries
- blast radius summaries
- user service scores
- candidate suitability summary
- best available pool
- prediction summaries
- trust evolution summaries
- overview summary

Production dry-run confirms all 11 are buildable.

## Runtime Read Contract

`admin_core/intelligence_snapshots.py` allows the planner to read all snapshot families, but requires validation of schema, freshness, expiry, confidence, source hashes, and item counts.

The planner must not read raw history logs directly. Therefore fixes should enrich snapshots using existing workers, not bypass the fast path.

## Safe Classification

| Component | Classification |
| --- | --- |
| RI6 model functions | REUSE |
| `intelligence_workers` snapshot builders | EXTEND |
| `v7-intelligence-snapshot-refresh` | REUSE |
| existing audit/switch/history stores | REUSE |
| closure/execution empty stores | EXTEND after ownership decision |
| runtime planner fast path | DO_NOT_TOUCH in this audit |
| governance/execution/rollback ownership | DO_NOT_TOUCH |
