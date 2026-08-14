# OBSERVABILITY_CERTIFICATION

Status: PASS

Existing reused implementation:

- `observability_model`
- snapshot confidence/freshness contracts

RI6 observability:

- New advisory family: `trust-evolution-summaries`
- Missing outcomes are explicit warnings:
  - `prediction_actual_outcomes_missing`
  - `candidate_outcomes_missing`
  - `decision_outcomes_missing`

Runtime behavior:

- Advisory-only.
- Stale: IGNORE.
- Low confidence: IGNORE.

