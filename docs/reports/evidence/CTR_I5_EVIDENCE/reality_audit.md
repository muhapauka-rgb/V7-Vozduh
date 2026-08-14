# CTR.I5 Reality Audit Evidence

Program: CTR.I5 Production Dry-Run Observation Window And CTR Value Certification

## Existing observation ownership

Found existing CTR.I4 single-plan shadow comparison:

- `tools/v7-users-autoswitch::ctr_shadow_comparison`
- candidate ranking comparison
- winner comparison
- service/trust/recovery/capacity quality delta
- no-bypass flags

Missing before CTR.I5:

- passive observation window aggregator across multiple dry-run planner outputs
- CTR usefulness score across cycles
- CTR confidence score across cycles
- state-level winner/top3 counts across cycles

## CTR.I5 implementation

Added:

- `tools/v7-ctr-observation-window`

This tool:

- reads existing autoswitch dry-run JSON plans
- extracts `ctr_shadow_comparison`
- aggregates cycles
- calculates positive/negative/neutral changes
- calculates CTR usefulness score
- calculates CTR confidence score
- produces readiness review

It does not:

- run the planner
- change planner ranking
- change selected moves
- write runtime state
- mutate routing
- create packets
- write restore barriers

## Production data availability

Existing production dry-run evidence was inspected from:

- `docs/reports/evidence/canary_expansion_small_batch_evidence/`
- `docs/reports/evidence/medium_batch_readiness_evidence/`
- `docs/reports/evidence/large_batch_stability_pool_readiness_evidence/`
- `docs/reports/evidence/pool_stability_post_pool_evidence/`

Result:

- Existing JSON plans do not contain `ctr_shadow_comparison`.
- They were produced before CTR.I4 shadow comparison existed in planner output.
- Therefore CTR usefulness cannot be certified from those historical files.

Current production observation verdict:

- `INSUFFICIENT_DATA`

