# P3.E Observability Certification

Project: V7 Vozduh
Block: P3.E Dry-Run Certification

## Observability Surfaces

P3.C/P3.D are visible through existing `/admin-v2` trust/runtime/operator surfaces.

No new top-level admin section is required.

## Operator Visibility

Operators can inspect:

- dry-run decision
- reason
- confidence
- input refs
- input hashes
- freshness
- evidence
- verification plan
- rollback simulation
- verification comparison
- verification confidence
- safety flags

## Observability Limits

The UI must not expose execute/apply/route/move/autoswitch controls for the P3 dry-run result.

The UI must preserve the distinction between planning confidence and runtime authority.

## Verdict

`observability_certified=true`

