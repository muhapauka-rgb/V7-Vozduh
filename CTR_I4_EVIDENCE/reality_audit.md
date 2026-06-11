# CTR.I4 Reality Audit Evidence

Program: CTR.I4 CTR Shadow Comparison Window And Decision Quality Certification

## Verified reality

CTR simulation exists:

- `Candidate.ctr_score_simulation`
- `_attach_ctr_score_simulation(candidates)`
- candidate JSON field `ctr_score_simulation`

CTR simulation is not applied:

- `_score_parts` remains the production score owner.
- `candidate.score` remains `sum(candidate.score_parts.values())`.
- selected moves remain owned by `_select_moves`.
- routing remains unchanged.
- packets and restore barriers are not touched by CTR.I4.

## CTR.I4 extension

Added read-only plan field:

- `ctr_shadow_comparison`

This field compares:

- current production ranking
- CTR simulated ranking
- current winner
- simulated winner
- top 3 order
- best available pool order
- quality deltas
- service-aware deltas
- CTR state promotion/demotion statistics

## Stop condition check

No production CTR influence was found. The program did not stop early because CTR remained advisory/shadow only.

