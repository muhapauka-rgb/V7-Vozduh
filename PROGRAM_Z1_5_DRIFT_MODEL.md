# Program Z1.5 Drift Model

Date: 2026-06-01

## Critical Drift

These must invalidate approval:

- approved user changes, unless approval explicitly names a candidate class
- budget changes
- route class changes
- target trust class changes
- target policy class changes
- target becomes ineligible
- safety status becomes critical
- registry hash changes for the approved user row
- policy hash changes
- selected move count exceeds budget
- rollback target changes
- target interface missing or disabled

## Non-Critical Drift For Policy Approval

These may be allowed only under explicit substitution rules:

- target egress ID changes within same route class
- target score ordering changes within same policy class
- capacity changes that remain within approved capacity band
- health score changes that remain above floor
- quality changes that do not change eligibility or trust class

## Non-Critical Drift For Target Approval

Almost none. Target approval is intentionally strict:

- exact user must match
- exact target must match
- exact rollback must match
- runtime hashes/fingerprints must match or be within explicit tolerance

## Verdict

drift_model_defined=true

