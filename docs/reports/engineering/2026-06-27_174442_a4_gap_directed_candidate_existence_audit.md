# Engineering Report: A4 gap-directed candidate existence audit

## Summary

Read-only audit found current A4 gap-reducing candidates in the eligible candidate universe, but the governed A4 planner-selected candidate is non-missing.

## Action Performed

Compared:

- current A4 missing candidate keys;
- autoswitch read-only candidate universe;
- current governed planner-selected candidate.

No apply, no restore barrier, no runtime mutation, no user movement.

## Objective Observations

- A4 missing candidate keys: `62`.
- Autoswitch read-only summary: `25` candidate moves, `0` selected moves.
- Autoswitch terminal reason: `dry_run_intelligence_snapshot_stop_required`.
- Eligible candidate rows checked: `40`.
- Gap-reducing eligible candidate rows: `18`.
- Governed planner-selected candidate: `10.7.0.5 -> vless`.
- Planner-selected candidate is missing A4 evidence: `NO`.
- Latest governed stop reason: `candidate_not_missing_a4_evidence`.

## Engineering Conclusions

There are gap-reducing candidates available in the candidate universe, but current governed A4 selection is not gap-directed. This is an existing-owner A4 selection/read-model integration gap, not a new architecture problem.

## Impact

A4 cannot reliably finish by repeatedly running the current governed selection loop, because the loop may keep selecting non-missing candidates while missing candidates exist elsewhere.

## Capability Progress

A4 remains `94 / 156 = 60.3%`; missing `62`.

## Backlog Progress

A4 remains `IN_PROGRESS`.

## Production Maturity

Production Maturity remains `24.0%`.

## Canonical Knowledge

No new owner, backlog item, runtime path, policy, or architecture required. Existing A4/gap evidence owners cover the finding.

## Evidence

- `current_a4_missing_candidate_keys`: `62`.
- `eligible_candidate_count`: `40`.
- `gap_reducing_eligible_count`: `18`.
- `planner_selected_missing`: `false`.
- `users_moved`: `0`.
- `runtime_automation_enabled`: `false`.
- `authority_expanded`: `false`.

## Next Step

Extend existing A4 governed selection owner to choose a safe gap-reducing candidate when one exists, before attempting bounded transaction execution.

## Re-audit Rule

Re-audit after the A4 selection owner is extended, or if production candidate/read-model structure changes materially.
