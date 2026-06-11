# CTR.I3 Reality Audit Evidence

Program: CTR.I3 Pool Soft Score Application Dry-Run Parity

## Current state before CTR.I3

CTR already existed as advisory data:

- `tools/v7-users-autoswitch::_snapshot_channel_trust_recovery_map`
- `tools/v7-users-autoswitch::_ctr_soft_adjustment_for_state`
- `tools/v7-users-autoswitch::_ctr_advisory_for_egress`
- candidate JSON field: `ctr_advisory`
- routing brain summary field: `routing_brain.ctr_advisory`

CTR did not exist in the production score path:

- `_score_parts` did not include a `ctr` score part.
- `candidate.score` was still `sum(candidate.score_parts.values())`.
- candidate sorting still used `(candidate.eligible, candidate.score)`.
- selected move selection still used existing decisions and candidate scores.

## CTR.I3 extension point

Existing owner:

- Planner owner: `tools/v7-users-autoswitch`
- Production score owner: `_score_parts`
- Candidate selection owner: `_decision_for_user`
- Selected move owner: `_select_moves`

Extension point:

- `Candidate.ctr_score_simulation`
- `_attach_ctr_score_simulation(candidates)`

Merge point:

- Candidate JSON output only.
- Routing brain advisory summary only.

## No duplicate ownership

CTR.I3 did not create:

- a second planner
- a second selected move writer
- a second runtime authority
- a second score path for production decisions
- a second pool owner

