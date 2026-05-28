# E11.16 Generation Governance Analysis

## Current Ownership Model

planner_timer=v7-autoswitch-planner.timer
planner_command=/usr/local/bin/v7-users-autoswitch
apply_timer=v7-users-autoswitch.timer
apply_command=/usr/local/bin/v7-users-autoswitch --apply

The planner/apply split is timer-authority separation, not a persisted generation
handoff. The apply timer computes a fresh plan in process and applies the
selected moves from that same in-memory plan.

## State Ownership

| State | Owner | Mutation Pattern | Governance Risk |
|---|---|---|---|
| `users.registry` | `v7-user-switch` | only during user movement | protected if apply selects no moves |
| `switch-history.jsonl` | `v7-user-switch` | append on movement | drift detector for unexpected apply |
| `autoswitch-restore-barrier.json` | governance block | explicit barrier TTL/clearance metadata | previously expired open; now fail-closed |
| `egress-load-summary.json` | planner/apply dry-run | refreshed during planning | not user movement, but can alter future scoring context |
| `client-reconnect-state.json` | planner/apply | reconnect observation | possible future rotation input |
| `autoswitch-safety.json` | apply after movement | anti-flap/freeze state | no write without applied movement |

## E11.16 Evidence

Live pre-TTL state:

- barrier_expired=false
- barrier_ttl_remaining_seconds=81917
- apply timer held
- selected_moves=0 under active barrier
- WireGuard users=0
- runtime checks OK

Counterfactual expired-barrier dry-run on copied live state before fix:

- `restore_barrier.active=false`
- `candidate_moves_total=4`
- `selected_moves=3`
- selected users: `10.7.0.11`, `10.7.0.12`, `10.7.0.14`
- fourth switch decision: `10.7.0.15`
- runtime hashes unchanged

This proves that barrier expiry would re-enable fresh apply recompute under the
current service/quality pressure. It was not stale selected_moves replay; it was
new eligibility computation once barrier suppression was removed.

## Verdict

generation_governance_required=true
barrier_alone_sufficient=false
selected_moves_cache_root_cause=false
fresh_apply_recompute_root_cause=true

The missing ownership concept is not a stale planner file. It is explicit
restore lifecycle clearance: apply needs to know whether a post-restore barrier
has been intentionally cleared by a governed generation, rather than treating
TTL expiry as production authorization.

