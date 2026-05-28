# One-User Canary Governance

This document defines future governance for a one-user canary. It does not authorize or execute the canary.

## Approval

A future one-user canary requires explicit operator approval naming:

- user IP;
- current egress;
- target egress;
- rollback egress;
- canary window;
- autoswitch hold plan;
- stop conditions;
- rollback authority.

Approval is valid only for the named user and target. It does not approve routing-sync, autoswitch apply, policy apply, Direct/RU mutation, proxy apply, or broader migration.

## Execution Authority

Only an operator with control-plane responsibility may execute the future canary. The execution must be manual, observed, and bounded. Automation must not choose or expand the candidate during the canary window.

## Required Pre-Canary Packet

```text
candidate user
from egress
to egress
route table
target interface
forward preview JSON
rollback preview JSON
kill switch status
user route check status
provisioning reconcile status
reconcile status or approved explanation
autoswitch hold confirmation
target egress readiness
operator approval
```

## Blast Radius Control

- one user only;
- no `v7-routing-sync` as first mutation;
- no autoswitch apply during observation;
- no policy/Direct/RU/proxy mutation;
- no kill switch rebuild unless separately approved;
- no automatic escalation to multi-user movement.

## Rollback Readiness

Rollback must be known before the canary. For the current E8.8 conditional packet:

```text
v7-user-switch 10.7.0.15 vless
```

Rollback is mutation and requires the same observation discipline as the forward switch.

## Block E8.8 Approval Packet

```text
candidate_user=10.7.0.15
current_egress=vless
target_egress=1
rollback_target=vless
route_table=1013
target_interface=v7e356a192b79
approval_status=CONDITIONAL
execution_allowed_now=False
```

Forward command for a separately approved future canary:

```text
v7-user-switch 10.7.0.15 1
```

Rollback command:

```text
v7-user-switch 10.7.0.15 vless
```

This packet supersedes the stale `10.7.0.13 -> awg3` candidate. `awg3` is not the first-canary target because current evidence still shows weak quality/stability.

## Block E9 Execution Result

```text
canary_executed=true
candidate_user=10.7.0.15
forward=vless -> 1
rollback=1 -> vless
forward_success=true
rollback_success=true
quiet_window_preserved=true
only_one_user_moved=true
blast_radius_respected=true
execution_allowed_now=False
```

Governance conclusions:

- the one-user `v7-user-switch` canary path is live-proven for `10.7.0.15`;
- rollback via `v7-user-switch 10.7.0.15 vless` is live-proven for the same user;
- `v7-routing-sync` was not required and remains forbidden as a broad first mutation;
- the quiet hold model must be repeated for any future canary;
- the E9 result does not grant standing permission for more users.

## Block E9.1 Monitoring Result

```text
post_canary_monitoring_executed=true
delayed_side_effects_observed=false
candidate_10.7.0.15_still_vless=true
table_1013_back_to_tun0=true
second_canary_readiness=CONDITIONAL
execution_allowed_now=False
```

Governance conclusion:

- post-canary monitoring supports the E9 success verdict;
- no delayed movement or routing drift was observed;
- second canary discussion may proceed only as a new approval packet, not as automatic execution.

## Autoswitch Non-Interference

Before execution, the operator must prove autoswitch cannot concurrently move users. A canary is invalid if autoswitch can run `--apply` during the window.

## Automatic Failure Conditions

The canary fails if any occur:

- user route table does not point to target interface;
- registry/assignment mismatch appears;
- kill switch check warns or fails;
- route check warns or fails;
- target egress health falls below accepted threshold;
- autoswitch moves any user during the window;
- unexpected policy/Direct/RU/proxy state changes appear;
- rollback command cannot be executed promptly when needed.

## Result Recording

The operator must record:

- exact commands run;
- timestamps;
- pre/post check outputs;
- forward and rollback preview hashes;
- whether rollback was needed;
- observed user impact;
- final assignment and route state;
- whether autoswitch authority was restored.

## Verdict

The governance model exists. E9 proved one bounded live canary and rollback; E9.1 showed no delayed side effects. Future execution still requires a separate bounded live approval and immediate pre-canary checks.

## Block E9.2 Second Canary Packet

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
rollback_target=vless
approval_status=CONDITIONAL
execution_allowed_now=False
```

E9.2 changes the user variable while keeping the target variable stable:

- first live proof: `10.7.0.15: vless -> 1 -> vless`;
- proposed second proof: `10.7.0.14: vless -> 1 -> vless`;
- route table changes from `1013` to `1012`;
- target interface remains `v7e356a192b79`;
- `v7-routing-sync` remains forbidden.

The second canary strategy should be proof with immediate rollback, not a long hold and not a temporary migration, unless the operator separately approves a longer observation window. The reason is simple: E9.2 found target `1` health good but load-state noisy (`SOFT_FULL` / `1_users=1`) despite registry evidence showing no live user assigned to `1`.

Execution remains forbidden until a separate E9.3 live approval packet names the exact user, target, hold sequence, rollback, and accepted target-load condition.

## Block E9.2.1 Target Truth Update

E9.2.1 found that target `1` is no longer a clean same-target canary target:

```text
10.7.0.5 current=1 table=1003 enabled=1
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_ready_for_E9_3=false
candidate_10.7.0.14_still_valid=true
```

Governance impact:

- `10.7.0.14` remains a valid candidate variable;
- target `1` is currently occupied by another real user;
- a second canary to target `1` would no longer isolate pure route/user-switch mechanics;
- E9.3 should not execute against target `1` without a new explicit waiver and refreshed blast-radius statement.

Preferred path: perform a read-only target selection refresh and choose a healthy zero-user target, or wait until target `1` returns to zero users and refresh the packet.

## Block E9.2.2 Target Selection Result

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
```

Governance impact:

- the user variable remains acceptable;
- no target is currently acceptable for a clean zero-user second canary;
- no forward command is approved or recommended;
- rollback preview is non-actionable because no forward target exists.

Future E9.3 can only be discussed after a clean target appears or a separate waiver changes the experiment definition.

## Block E9.2.3 Target Watcher Governance

E9.2.3 created a manual read-only watcher:

```text
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
```

Governance rules:

- the watcher may be run manually for target-selection evidence;
- the watcher is not a daemon and must not be installed as a timer/service in this block;
- `GO` from the watcher only permits a new approval packet discussion;
- `GO` from the watcher does not execute canary and does not replace human approval;
- E9.3 must still name exactly one candidate, one target, one rollback target, and one bounded quiet-window model.

Current watcher verdict:

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
second_canary_readiness=NO-GO
should_E9_3_execute_now=false
```

## Block E9.2.4 Zero-User Diagnostics Governance

E9.2.4 changes the discussion but not the execution state:

- there is still no `CLEAN_READY` target;
- OpenVPN/WireGuard look like idle/stale-handshake targets, not proven dead targets;
- AWG0/AWG3 are real quality-floor failures;
- target `1` is operationally strong but occupied.

Governance implication:

```text
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

Any future E9.3 packet must state which experiment is being approved:

1. clean isolation: wait for strict watcher `GO`;
2. target diversity: use OpenVPN/WireGuard only with idle-SUSPECT waiver;
3. production-load realism: use target `1` only with occupied-target waiver.

## Block E9.2.5 OpenVPN Waiver Packet

E9.2.5 selects the target-diversity path:

```text
candidate_user=10.7.0.14
target_egress=openvpn-1779388847-d2ad7c
rollback_target=vless
waiver_name=openvpn_idle_suspect_mechanics_canary
approval_status=CONDITIONAL
execution_allowed_now=false
```

Governance meaning:

- this is not clean target readiness;
- the only waived condition is idle/stale-handshake `SUSPECT`;
- one-user blast radius still applies only if future execution uses exactly one approved `v7-user-switch`;
- rollback must be immediate or explicitly governed by the E9.3 live packet;
- fresh pre-canary checks are mandatory.

## E9.3 Governance Finding

The E9.3 OpenVPN waiver canary proved one-user mechanics for `10.7.0.14`:

- planner/apply authority was held;
- exactly one approved user was switched during the quiet window;
- table `1012` moved to `v7edb0c189291`;
- observation samples stayed stable;
- rollback restored table `1012` to `tun0`;
- runtime checks stayed OK.

The restore step exposed a separate governance gap:

```text
restored v7-users-autoswitch.timer immediately ran v7-users-autoswitch --apply
10.7.0.5 moved from 1 to vless after canary rollback
```

Future canary governance must separate:

| Window | Status |
|---|---|
| held canary window | one-user blast radius preserved |
| rollback window | one-user blast radius preserved |
| post-restore window | extra autoswitch movement occurred |

New rule:

```text
No further canary may be executed until autoswitch restore behavior is staged, bounded, or separately approved.
```

## E9.3.1 Restore Governance Update

E9.3.1 classified the side effect:

```text
restore_side_effect_classification=EXPECTED_BUT_UNSAFE_RESTORE_SEQUENCE
autoswitch_root_cause=timer_restore_immediate_apply_failover
restore_sequence_governance_gap=true
second_canary_readiness=NO-GO
```

Governance impact:

- the held canary window can still be one-user bounded;
- the restore window is a separate operational stage;
- restoring `v7-users-autoswitch.timer` can immediately resume apply authority and move non-candidate users;
- future canary approvals must restore `v7-autoswitch-planner.timer` first, observe planner-only state, and restore `v7-users-autoswitch.timer` only after separate explicit approval.

No further canary execution is acceptable under the old model that restores planner and apply timers together.

## E9.3.2 Staged Restore Governance

E9.3.2 creates the future restore contract:

```text
recommended_restore_model=planner_first_apply_by_separate_approval
apply_restore_requires_separate_approval=true
future_canary_restore_sequence_safe=false
execution_allowed_now=false
```

Future canary approval must include these distinct approvals:

1. approval for canary quiet hold;
2. approval for one named user switch;
3. approval for rollback/decision;
4. approval for planner-only restore;
5. separate approval for apply restore after pending moves are inspected.

The last approval is not optional. Restoring apply authority can move non-candidate users and must be treated as autoswitch recovery.
# E9.3.3 Restore Governance Addendum

Future one-user canaries must split the canary window from the autoswitch restore window.

Required sequence:

1. hold planner and apply;
2. execute only the approved one-user canary and rollback/decision;
3. restore planner only;
4. observe pending moves;
5. request separate apply restore approval;
6. restore apply only if approved.

E9.3.3 validated steps 1, 3, and 4 in a no-canary rehearsal. It did not validate apply restore.

Current status:

```text
planner_only_stage_safe=true
apply_restore_requires_separate_approval=true
execution_allowed_now=false
```

## E9.3.5 Restore Governance Update

E9.3.5 was not a canary, but it affects future canary governance. Apply authority restore is now a hard separate stage after canary rollback.

The final E9.3.5 planner-only gate showed:

```text
selected_moves=3
candidate_moves_total=15
apply_restore_aborted=true
```

Future canary reports must separate:

- canary window blast radius;
- rollback blast radius;
- planner-only restore evidence;
- apply-restore approval evidence;
- post-apply autoswitch recovery movements.

No future canary may treat `v7-users-autoswitch.timer` restore as cleanup. It requires its own fresh sample and explicit approval.
