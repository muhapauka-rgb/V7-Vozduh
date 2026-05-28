# Staged Canary Restore Runbook

Mode: future runbook only. Not executed in E9.3.2.

## Forbidden Without Separate Approval

- canary execution;
- `v7-user-switch`;
- `v7-routing-sync`;
- manual `v7-users-autoswitch --apply`;
- systemd stop/start/restart;
- policy/Direct/RU/Trusted RU/proxy/kill-switch mutation.

## Future Command Sequence

The following is a future sequence template. It must not be executed from this document.

### 1. Hold Planner and Apply

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Validation:

```bash
systemctl is-active v7-health.service
systemctl is-active v7-autoswitch-planner.timer || true
systemctl is-active v7-autoswitch-planner.service || true
systemctl is-active v7-users-autoswitch.timer || true
systemctl is-active v7-users-autoswitch.service || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' || true
```

### 2. Execute Approved One-User Canary

Only if separately approved:

```bash
v7-user-switch <candidate_user> <target_egress>
```

### 3. Rollback or Decision

If rollback is selected or required:

```bash
v7-user-switch <candidate_user> <rollback_egress>
```

### 4. Restore Planner Only

```bash
systemctl start v7-autoswitch-planner.timer
```

Do not restore `v7-users-autoswitch.timer` in this stage.

### 5. Observe Planner-Only

Collect at least two samples:

```bash
systemctl is-active v7-autoswitch-planner.timer
systemctl is-active v7-users-autoswitch.timer || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' || true
sha256sum /opt/v7/egress/state/users.registry /opt/v7/egress/state/egress.registry
tail -n 50 /opt/v7/egress/state/switch-history.jsonl 2>/dev/null || true
v7-reconcile-check
v7-user-route-check
v7-killswitch-check
v7-provisioning-reconcile-check
```

Planner selected moves should be captured from planner output/state when available.

### 6. Request Apply Restore Approval

Apply restore remains blocked unless operator approves:

```text
pending_moves=<none/list>
max_apply_movements=<n>
accepted_reason_classes=<list>
operator_approval=true
```

### 7. Restore Apply Only If Approved

```bash
systemctl start v7-users-autoswitch.timer
```

### 8. Post-Apply Settle

Collect:

- timer/service status;
- process guard;
- registry hash;
- switch-history delta;
- route/rule delta;
- four runtime checkers;
- movement classification.

## Abort Conditions

Abort and keep apply held if:

- planner predicts broad movement;
- selected move reason is unclear;
- any checker fails;
- `v7-routing-sync` appears;
- registry changes before apply restore;
- operator approval is missing.

## Runbook Verdict

```text
future_canary_restore_sequence_safe=false
reason=requires_future_approval_and_validation
```
# E9.3.3 Live Rehearsal Note

E9.3.3 validated the planner-first part of this runbook:

1. hold planner/apply;
2. collect quiet baseline;
3. restore planner timer only;
4. observe planner output;
5. keep apply timer held.

The rehearsal found pending failover recommendations after planner-only restore. Future runbook executions must treat this as a separate apply-restore approval stage, not as canary cleanup.

Current hard rule:

```text
do_not_start_v7-users-autoswitch.timer_without_separate_apply_restore_approval=true
```

## E9.3.4 Apply Restore Packet Update

E9.3.4 refreshed planner-only evidence and kept `v7-users-autoswitch.timer` held.

Fresh planner output showed:

```text
selected_moves=0
apply_requested=false
apply_result.applied=false
```

This is not a command to restore apply authority. It is a readiness signal for a separate future block.

Future apply-restore execution must follow this reduced sequence:

1. take a fresh authority snapshot;
2. collect one final planner-only sample;
3. confirm selected moves are zero, or explicitly list accepted moves;
4. set `max_apply_movements`;
5. only then restore `v7-users-autoswitch.timer`;
6. collect post-apply settle evidence;
7. classify any movement as autoswitch recovery, not canary movement.

Current status:

```text
apply_restore_status=HELD
approval_status=CONDITIONAL
execution_allowed_now=false
```

## E9.3.5 Runbook Update

Before apply restore, the runbook now requires a final immediate planner-only sample. If that sample differs from the approval packet, apply restore must abort.

E9.3.5 result:

```text
final_planner_selected_moves=3
final_planner_candidate_moves_total=15
approved_zero_move_assumption_invalidated=true
apply_restore_executed=false
apply_restore_status=HELD_ABORTED_BY_FINAL_PLANNER_SAMPLE
```

The next apply restore attempt must start from fresh planner-only evidence and either:

- show `selected_moves=0`; or
- include explicit operator approval for the exact selected movement list and maximum movement count.

## E9.4.4 Runbook Update

Add a delayed-settle block after apply timer restore:

1. Restore apply timer only after the approved final gate.
2. Collect immediate post-restore evidence.
3. Continue observing across at least two full apply timer intervals.
4. For each delayed-settle sample, collect:
   - `users.registry` hash;
   - switch-history/safety incoming entries;
   - latest planner/apply output;
   - `selected_moves`;
   - Telegram hard-block state for egress `1`;
   - route/rule drift summary;
   - `v7-reconcile-check`;
   - `v7-user-route-check`;
   - `v7-killswitch-check`;
   - `v7-provisioning-reconcile-check`.
5. If any movement occurs, classify it as autoswitch recovery before any canary planning continues.
6. Do not mark restore governance live-proven until delayed-settle passes.

Current status:

```text
restore_governance_live_proven=false
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.4.5 Runbook Update

Before any future apply restore stage, run the restore settle checker in pre-restore mode against the approved evidence set:

```bash
tools/v7-restore-settle-gate --pre-restore --pretty
tools/v7-restore-settle-gate --pre-restore --json
```

GO requires:

```text
gate_status=GO
sample_count>=3
apply_timer_intervals_covered>=2
selected_moves_by_sample=[0,0,0...]
telegram_hard_blocked_by_sample=[false,false,false...]
egress_1_eligible_by_sample=[true,true,true...]
checkers_ok=true
hidden_movers_observed=false
```

After any approved apply timer restore, run post-restore settle:

```bash
tools/v7-restore-settle-gate --post-restore --pretty
tools/v7-restore-settle-gate --post-restore --json
```

If post-restore reports movement, the movement is autoswitch recovery and not canary movement. The next canary remains NO-GO until that recovery is classified.

## E10 Fresh Approval Runbook Status

E10 instantiated this runbook as a future model only.

```text
candidate_user=10.7.0.11
selected_target=NONE
rollback_target=vless
restore_settle_gate_status=GO
second_canary_approval_status=NO-GO
execution_allowed_now=false
```

Because `selected_target=NONE`, no future command sequence is approved from E10. Any next live canary block must first produce a fresh target approval or an explicit target-specific waiver packet.

## E11.1 WireGuard Target Runbook Update

E11.1 keeps the staged canary restore lifecycle unchanged, but identifies the next target-specific governance path:

```text
target=wireguard-1779454504-c43409
target_status=CONDITIONAL_STALE_HANDSHAKE_ONLY
reservation_required=true
waiver_required=true
execution_allowed_now=false
```

Before any WireGuard canary execution packet, the project must complete:

1. WireGuard reservation approval or diagnose semantics approval.
2. Fresh target readiness after reservation/fix/waiver.
3. Fresh restore-settle gate.
4. Fresh one-user candidate selection.
5. Explicit forward/rollback preview.

If diagnose remains `SUSPECT`, the future canary packet must label the run as a stale-handshake waiver canary, not a strict clean-target canary.

## E11.2 WireGuard Reservation Gate

Before any future second canary using WireGuard:

1. Execute a separate bounded reservation metadata block for
   `wireguard-1779454504-c43409`.
2. Re-run restore-settle and runtime checkers.
3. Resolve stale-handshake diagnose semantics, or carry the explicit
   `wireguard_stale_handshake_reserved_target` waiver into a fresh canary
   approval packet.
4. Select the canary candidate fresh; old E9/E10 candidates are stale.
5. Use the full staged restore lifecycle after any canary movement.

E11.2 does not authorize canary execution.

## E11.4 Addendum - WireGuard Diagnose Gate Before Second Canary

Before any WireGuard-backed second canary block, the runbook now requires one of
two preconditions:

```text
preferred=diagnose_semantics_fixed_and_wireguard_readiness_GO
fallback=explicit_stale_handshake_waiver_packet_CONDITIONAL
```

The preferred path must prove that the diagnose producer is protocol-aware:

- WireGuard handshake freshness is read with `wg show <iface>`.
- AWG/AmneziaWG handshake freshness continues to use the AWG-specific command.
- `diagnose=SUSPECT` remains possible for true missing/down/stale WireGuard
  conditions.
- Strict target readiness selects the reserved WireGuard target only after
  fresh runtime gates pass.

The fallback waiver path must explicitly state that the canary is conditional,
one-user only, and dependent on fresh live handshake/route/quality evidence plus
restore-settle `GO`.

## E11.5 Addendum - Diagnose Deploy Before Canary Approval

E11.5 prepared the repo-side diagnose fix but did not deploy it to runtime.
Before any direct WireGuard second-canary approval:

1. Deploy only `v7-egress-diagnose` in a bounded runtime tooling block.
2. Create a timestamped backup and rollback command.
3. Run the fixed diagnose refresh/check.
4. Verify WireGuard diagnose is `OK`.
5. Verify AWG0/AWG3 diagnose did not regress.
6. Re-run strict target readiness and restore-settle evidence.
7. Only then prepare a fresh second-canary approval packet.

Until that deploy succeeds, WireGuard can only be considered through an explicit
conditional stale-handshake waiver path.

## E11.6 Addendum - Fresh Packet Required After Diagnose Deploy

E11.6 deployed the runtime diagnose fix and removed the WireGuard stale
handshake blocker:

```text
wireguard_diagnose_after=OK
selected_target_after=wireguard-1779454504-c43409
waiver_required_after=false
```

The next executable canary block is still not authorized by this deploy. Before
any live switch:

1. Create a fresh second-canary approval packet.
2. Use current candidate assignment; do not reuse old `current=vless`
   assumptions.
3. Confirm restore-settle remains `GO`.
4. Build new forward and rollback previews.
5. Use the staged lifecycle: hold planner/apply, one approved movement,
   observe, rollback/decision, restore planner, settle gate, restore apply only
   after gate, then post-restore settle monitoring.

## E11.7 Addendum - Do Not Execute While Reserved Target Is Occupied

E11.7 aborts fresh canary planning because the reserved WireGuard target has
production users.

Before any future live second-canary block:

1. Prove target zero-user by registry and load-state.
2. Prove `canary_reserved=true` is enforced by autoswitch or explicitly suspend
   production assignment to the target through a separately approved block.
3. Re-run target readiness.
4. Re-run restore-settle gate.
5. Generate fresh forward/rollback previews only after target readiness is
   `GO`.

## E11.8 Addendum - Reservation Enforcement Before Canary Planning

Before any canary approval packet can use a reserved target:

1. Verify runtime `v7-users-autoswitch` enforces `canary_reserved=true`.
2. Verify no production candidate can select the reserved target.
3. Verify existing users on a reserved target have either been drained by a
   separate bounded packet or are explicitly accepted as non-clean occupancy.
4. Require target readiness to report zero users from registry and load-state.

E11.8 enforces new assignment prevention, but WireGuard remains occupied until a
separate drain approval packet.

## E11.10 Closeout Addendum - Close Open Canary Before New Work

If a canary has been executed but lacks a keep/rollback decision, close that
canary before any new block.

E11.10 closeout validated this sequence:

1. Collect fresh live state.
2. If the candidate is still on the canary target, run a pre-decision settle
   check.
3. Reject keep if any sample has `selected_moves>0`.
4. Execute only the approved rollback user movement.
5. Restore planner first.
6. Run planner-only settle samples.
7. Restore apply only if the settle gate is `GO`.
8. Observe delayed effects across multiple samples.
9. Publish a final lifecycle report with mutation statements.

E11.10 result:

```text
candidate_user=10.7.0.3
rollback_executed=true
rollback_target=awg0
only_one_user_moved=true
restore_settle_gate_status=GO
apply_restore_after_gate_GO=true
delayed_movements_observed=false
new_canary_performed=false
```

## E11.11 Hardening Addendum - Post-Closeout Review Before Cohort

After a one-user lifecycle is closed, run a post-closeout governance review
before any cohort approval. The review must verify:

- current live state, not only historical fixture evidence;
- planner/apply timers and hidden mover scan;
- selected moves are zero;
- reservation enforcement still blocks production assignment to reserved targets;
- restore-settle gate defaults point at current evidence;
- target readiness defaults point at current state;
- runtime/repo lineage gaps are documented;
- mini-cohort capacity is bounded by target hard limit.

E11.11 result:

```text
governance_review_completed=true
lifecycle_stable=true
mini_cohort_readiness=CONDITIONAL
recommended_next_block=E11.12_TWO_USER_MINI_COHORT_APPROVAL_PACKET
execution_allowed_now=false
```

## E11.12 Addendum - Two-User Mini-Cohort Lifecycle

E11.12 defines, but does not execute, the first two-user mini-cohort lifecycle:

1. Fresh pre-checks: WireGuard users `0`, target readiness `GO`, restore-settle
   `GO`, selected moves `0`, checkers OK, hidden movers absent.
2. Hold planner/apply.
3. Move `10.7.0.11` to `wireguard-1779454504-c43409` and verify.
4. Wait at least one check interval.
5. Move `10.7.0.12` to `wireguard-1779454504-c43409` and verify.
6. Observe A/B/C.
7. Default rollback both users to `1` unless keep is explicitly safer.
8. Restore planner first.
9. Run restore-settle gate.
10. Restore apply only after gate `GO`.
11. Run delayed monitoring across multiple timer intervals.
12. Publish final verdict and mutation statements.

E11.12 verdict:

```text
approval_status=CONDITIONAL
blast_radius=2_users_max
three_user_cohort_allowed=false
execution_allowed_now=false
```

## E11.13 Addendum - Apply Restore Delayed Movement

E11.13 validated the two-user forward/rollback mechanics but exposed a restore
lifecycle blocker:

```text
restore_settle_gate_status=GO
apply_timer_restored_after_gate_GO=true
delayed_movements_observed=true
delayed_non_cohort_users=10.7.0.9,10.7.0.10,10.7.0.13
movement=1->awg0
apply_timer_reheld_for_containment=true
```

Runbook update: a pre-apply restore-settle GO is necessary but not sufficient.
After apply restore, delayed monitoring must be treated as a hard promotion
gate. If non-cohort movement occurs, hold apply again, do not manually move
unrelated users, and open a root-cause/hardening block before any larger cohort.
## E11.14 Apply-Restore Barrier Update

E11.14 proved that pre-restore settle GO is necessary but not sufficient for restoring the apply timer. A later apply-timer generation can recompute fresh service state and move non-cohort users after the sampled settle window.

New restore rule:

- Planner restore may proceed after rollback/keep verification.
- Restore-settle GO still requires stable hashes and `selected_moves=0`.
- Apply timer restore is not promotion-clean unless a restore barrier is active or a separate apply-restore approval block explicitly proves safe timer restoration.
- The restore barrier file is `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
- While active, `v7-users-autoswitch` suppresses failover selection during the post-restore window.
- Manual `v7-users-autoswitch --apply` remains forbidden in canary/cohort closeout blocks.

E11.14 status: apply timer remains held; next block must rehearse apply-restore barrier/generation governance before any larger cohort.

## E11.15 Apply-Restore Barrier Rehearsal Rule

E11.15 proves the restore barrier can suppress failover selection across a
bounded apply-timer restore rehearsal:

```text
apply_timer_restored=true
apply_requested_by_timer=true
restore_barrier_active=true
selected_moves=0
users_registry_hash_stable=true
switch_history_count_stable=true
apply_timer_final_state=held
```

Runbook update:

1. Apply restore under an active barrier is allowed only as an explicit bounded
   rehearsal or approved restore block.
2. A clean rehearsal requires multiple timer intervals with stable registry
   hash, stable switch-history count, selected moves `0`, and runtime checkers
   OK.
3. If barrier TTL expiry is not observed, the apply timer must be returned to
   hold at the end of the rehearsal.
4. A future post-TTL or generation-token block is required before unattended
   apply timer operation is considered promotion-clean.

## E11.16 Post-TTL Fail-Closed Rule

TTL expiry is no longer an implicit apply clearance. If a restore barrier exists
and expires without explicit clearance, failover remains quarantined.

Required clearance signals are explicit and auditable:

- `cleared=true`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`

Until one of those is present, apply timer must be treated as conditional even
if it is technically able to run. Any future clearance block must re-run fresh
target readiness, restore-settle, selected_moves, runtime checks, and hidden
mover scans.

## E11.17 Generation Clearance Budget Rule

Explicit clearance after barrier expiry is not sufficient by itself. If live
pressure exists, clearing the barrier can re-enable fresh apply recompute.

Future clearance must declare an approved movement budget:

```text
generation_clearance=true
clearance_max_selected_moves=<approved_count>
```

For rehearsal and no-movement restore validation, the approved count is `0`.
If recompute finds more selected moves than the budget, apply must remain a
no-op and report:

```text
clearance_budget_exceeded=true
clearance_guard_reason=restore_barrier_clearance_selected_moves_exceed_budget
selected_moves=0
```

The E11.17 live rehearsal proved this with
`clearance_selected_moves_before_guard=3` and final `selected_moves=0`.

## E11.18 Promotion-Clean Two-User Restore Lifecycle

The two-user mini-cohort restore lifecycle is promotion-clean only with all of
the following gates:

1. Exact approved users only.
2. Exact reserved WireGuard target only.
3. Sequential movement and route verification after each user.
4. Default rollback to target `1`.
5. Planner restore before apply restore.
6. Restore-settle GO.
7. Restore barrier present.
8. Post-TTL clearance explicit.
9. `clearance_max_selected_moves` set to the approved movement budget.
10. Delayed monitoring across timer intervals.
11. Final apply timer held unless a separate block approves otherwise.

For the E11.18 promotion-clean decision, the selected movement budget for
post-clearance restore validation is `0`. Larger cohorts require a separate
generation-token or nonzero-budget rehearsal.

## E12 Nonzero Budget Generation Rule

Any post-TTL restore clearance with `clearance_max_selected_moves > 0` must be
bound to immutable generation evidence:

```text
generation_token=<opaque approval token>
clearance_generation_id=<current planner_generation_id>
approved_selected_moves_hash=<hash of selected user/from/to/type list>
clearance_expected_selected_moves=<approved count>
clearance_max_selected_moves=<approved budget>
```

If token, generation, selected-move hash, count, expiry, or budget check fails,
apply must fail closed with `selected_moves=0`.

Budget zero remains valid for no-movement restore validation. Nonzero budget is
not cohort approval; it is only the replay-resistant envelope for a separately
approved movement plan.
