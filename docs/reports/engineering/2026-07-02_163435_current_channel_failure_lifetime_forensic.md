# Current Channel Failure Lifetime And Propagation Forensic

Created: 2026-07-02 16:34:35 Asia/Bangkok
Mode: READ_ONLY_FORENSIC
Production impact: NONE
Deploy performed: NO
Users moved: 0

## Mission

Trace why the production fact:

```text
openvpn-1779388847-d2ad7c is failed/degraded and still has affected users
```

does not appear in the latest blocked execution, which instead reports:

```text
current_channel_failure.confirmed = false
current_channel_failure.severity = OK
current_channel_failure.diagnose_reason = OK
current_failures = []
l3_wake_decision = REJECT_WAKE
blockers = confirmed_l3_wake_required, required_service_failure_required
```

No code, runtime, planner, authority, restore barrier, wake, service matrix, production state, or user routing was modified.

## Compared Executions

### Success Execution

Artifact:

```text
/opt/v7/egress/state/execution-events.jsonl:8625
/opt/v7/egress/state/l3-runtime-state.json
```

Identity:

```text
created_at = 2026-07-02T03:25:16.066855+00:00
operation_id = runtime_autoswitch_1367b9f8947a3359ad4ce4e4
l3_incident_key = 73eb29a94ce3010d80c9a73a
user = 10.7.0.3
source = openvpn-1779388847-d2ad7c
target = awg0
selected_move_hash = 77c81719cf94321b5d368ad79529909d633123d6e161040865746b297a9d5fb4
terminal_state = APPLIED
terminal_reason = selected_moves_applied
outcome_status = success
verify_rc = 0
service_verify_rc = 0
```

Incident record:

```text
incident_key = 73eb29a94ce3010d80c9a73a
failed_sources = ["openvpn-1779388847-d2ad7c"]
failed_required_services = ["google", "google_auth", "instagram", "telegram", "youtube"]
status = CLOSED
terminal_state = APPLIED
terminal_reason = selected_moves_applied
attempt_count = 1
```

Reason for comparison:

```text
This is a real automatic governed L3 execution that moved one user from the failed OpenVPN source.
```

### Latest Blocked Execution

Artifacts:

```text
/opt/v7/egress/state/operator-execution-lease.json
/opt/v7/egress/state/execution-events.jsonl:11991
/opt/v7/egress/state/l3-runtime-state.json
```

Identity:

```text
terminal operation_id = runtime_autoswitch_5cf1792f5557d5810ecfb9b6
source_preview operation_id = runtime_autoswitch_f16337da689d38f97276fd24
planner_generation_id = 01a0068ee0706821dfd3d958b706a2661e7725fbf1274cb4d96dc72f515ec968
l3_incident_key = 46ffebc776d1eb9fd256bf2a
user = 10.7.0.5
source = awg0
target = vless
approved selected_move_hash = f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff
post-gate selected_move_hash = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
terminal_state = DENIED
terminal_reason = approved_plan_lock_selected_moves_missing
```

Incident record:

```text
incident_key = 46ffebc776d1eb9fd256bf2a
failed_sources = []
failed_required_services = []
status = SUSPENDED
terminal_state = DENIED
terminal_reason = approved_plan_lock_selected_moves_missing
attempt_count = 15
```

Reason for comparison:

```text
This is the latest blocked execution where current_channel_failure was false/OK and Wake rejected.
```

### Current Production Observation

Artifacts:

```text
/opt/v7/egress/state/egress.registry
/opt/v7/egress/state/users.registry
/opt/v7/egress/state/egress-diagnose.state
/opt/v7/egress/state/egress-status.state
/opt/v7/egress/state/v7-state.json
/opt/v7/egress/state/service-matrix.json
/opt/v7/egress/state/telegram-sentinel.json
/opt/v7/egress/state/service-matrix-refresh-summary.json
```

Reason for comparison:

```text
This establishes whether the failed OpenVPN source recovered or whether the fact still exists.
```

## Part 1 - Production Reality Baseline

Collection time:

```text
server_time_utc = 2026-07-02T09:28:09Z
```

Source registry:

```text
id = openvpn-1779388847-d2ad7c
protocol = openvpn
type = interface
interface = v7edb0c189291
enabled = 1
role = GLOBAL_FAST
service_tags = google,telegram,instagram,global
```

Current assigned users:

```text
enabled affected users = 10
users = [
  10.7.0.2,
  10.7.0.4,
  10.7.0.6,
  10.7.0.8,
  10.7.0.9,
  10.7.0.10,
  10.7.0.11,
  10.7.0.12,
  10.7.0.13,
  10.7.0.15
]
```

Current diagnosis:

```text
egress-diagnose.updated = 2026-07-02T09:27:49Z
diagnose_severity = FAIL
diagnose_reason = interface_down_or_missing
diagnose_detail = protocol=openvpn
```

`v7-state.json` row:

```text
diagnose_severity = FAIL
diagnose_reason = interface_down_or_missing
diagnose_detail = protocol=openvpn
code = 000
avg_mbps = 0
min_mbps = 0
stability = 0
load_status = HARD_FULL
users = 10
```

`egress-status.state`:

```text
fail_count = 7768
last_code = 000
last_fail = 1782984289
last_ok = 1780405620
quarantine_until = 1782984589
```

Telegram Sentinel:

```text
updated = 2026-07-02T09:28:08.668344+00:00
blocked_egress includes openvpn-1779388847-d2ad7c
status = DOWN
bad_now = true
bad_for_seconds = 2578700.5
matrix_ok = false
matrix_status = TELEGRAM_DOWN_14S
reason = api.telegram.org:443=timeout; 149.154.167.50:443=timeout; 149.154.175.50:443=timeout; 91.108.56.177:443=timeout; 194.221.250.50:443=timeout
```

Service matrix:

```text
updated = 2026-07-02T09:28:08.656389+00:00
status = FAIL
ok_count = 0
route_class_fitness.GLOBAL_FAST.status = FAIL
route_class_fitness.GLOBAL_FAST.reason = telegram is mandatory and unavailable
route_class_fitness.VIDEO_OPTIMIZED.status = FAIL
route_class_fitness.VIDEO_OPTIMIZED.reason = required services failed
telegram.status = TELEGRAM_DOWN_14S
telegram.severity = FAIL
google.status = FAIL
youtube.status = FAIL
instagram.status = FAIL
chatgpt.status = FAIL
```

Admin API:

```text
127.0.0.1:7080 is listening for v7-admin-api.
Read-only requests to /api/egress and /api/users with admin/admin returned HTTP 401.
No API data was used as evidence.
```

Baseline verdict:

```text
openvpn-1779388847-d2ad7c is still a failed production source.
The failed-source fact is present and fresh in persisted production artifacts.
10 enabled users remain assigned to the failed source.
```

## Part 2 - Fact Lifetime Map

| Owner / Function | Input Failed Source | Output Failed Source | Decision | Blockers | Artifact |
| --- | --- | --- | --- | --- | --- |
| Telegram Sentinel | `openvpn-1779388847-d2ad7c`, interface `v7edb0c189291` | `status=DOWN`, `blocked=true`, `matrix_ok=false` | failed Telegram evidence preserved | none | `telegram-sentinel.json` |
| service-matrix writer | Telegram + HTTP probes for OpenVPN interface | `status=FAIL`, service failures for Telegram/Google/YouTube/etc. | failed service matrix preserved | none | `service-matrix.json` |
| egress state producer | diagnose/status files | `diagnose_severity=FAIL`, `diagnose_reason=interface_down_or_missing` | failed egress row preserved | none | `v7-state.json` |
| v7-state loader | `v7-state.json` | `self.state["egress"][source]` | source row loadable | none | `tools/v7-users-autoswitch` |
| `_load_egress()` | `state.egress[openvpn]` | `Egress.severity=FAIL`, `diagnose_reason=interface_down_or_missing`, `users=10` | failed source preserved | none | `tools/v7-users-autoswitch:3503-3544` |
| `_candidate()` | user + OpenVPN Egress | candidate gets severity classification from Egress | source fact preserved for OpenVPN candidates | later gates may block candidate | `tools/v7-users-autoswitch:7157-7175` |
| `_gate_basic()` | candidate severity FAIL | `candidate.eligible=false` | blocks current/source candidate | `severity_FAIL` | `tools/v7-users-autoswitch:7181-7200` |
| `_decision_for_user()` | user.current determines current source | decision source is the user's current assignment | source is per user, not incident-scoped | none directly | `tools/v7-users-autoswitch:6867-6982` |
| `_select_moves()` | all switch/failover decisions unless CLI source filter exists | selected move can be any failover-ranked user/source | not incident-scoped | none directly | `tools/v7-users-autoswitch:7686-7706` |
| `_approved_plan_lock_validation()` | approved lock selected move | validates locked user/source/target | preserves approved move identity | none in blocked case | `tools/v7-users-autoswitch:5794-5922` |
| `_merge_locked_moves_with_live_decisions()` | locked move + live decisions | merges semantic fields only if user/source/target match | preserves locked source | none directly | `tools/v7-users-autoswitch:5664-5701` |
| `_emergency_failover_move_evidence()` | selected move | evaluates `move.current_egress` only | evaluates `awg0`, not OpenVPN, in latest blocked run | `required_service_failure_required` | `tools/v7-users-autoswitch:1208-1286` |
| `_l3_wake_decision()` | move evidence | no failed_sources, no observed events | `REJECT_WAKE` | `confirmed_l3_wake_required` | `tools/v7-users-autoswitch:1364-1475` |
| `_l3_incident_context()` | gate.move_evidence | derives incident failed_sources from selected move evidence | incident has `failed_sources=[]` | stop-safe context | `tools/v7-users-autoswitch:1860-1933` |
| `_emergency_failover_authority_gate()` | selected move + restore barrier | returns empty selected moves when gate not ok | filters selected move | `confirmed_l3_wake_required`, `required_service_failure_required` | `tools/v7-users-autoswitch:955-1109` |
| Restore barrier gates | already-empty selected list in latest blocked run | did not remove OpenVPN fact | pass/empty | none | `tools/v7-users-autoswitch:5414-5462` |
| `_l3_execution_eligibility()` | plan selected moves | not reached with selected move; would evaluate selected move source | fail-closed if source recovered or wake rejected | `l3_wake_not_accepted`, etc. | `tools/v7-users-autoswitch:6251-6335` |

Field-level conclusion:

```text
The OpenVPN failed-source fact is preserved through production observation.
It is not overwritten to OK.
It is not stale.
It is not unavailable.
It disappears from the blocked execution because the blocked selected move is not sourced from OpenVPN.
```

## Part 3 - Source Scoping Audit

Mandatory questions:

1. Was the blocked execution actually about `openvpn-1779388847-d2ad7c`?

```text
NO.
```

Persisted selected move:

```text
user = 10.7.0.5
current_egress = awg0
recommended_egress = vless
move_type = failover
reason = current_egress_not_eligible, projected_load_target_adjusted
```

2. Or was it about `awg0 -> vless`?

```text
YES.
```

3. If source became `awg0`, why?

```text
Because the selected/approved move for the blocked execution was user 10.7.0.5 with current_egress=awg0.
Planner selection is driven by live user.current decisions and optional CLI source filter.
No persisted incident_source constraint was applied to keep the continuation on openvpn-1779388847-d2ad7c.
```

4. Did Planner select a user whose current source was no longer the failed OpenVPN channel?

```text
YES.
10.7.0.5 current=awg0 in users.registry.
```

5. Did approved plan lock preserve an old user/source/target after user state changed?

```text
NO for the latest blocked execution.
The lock preserved 10.7.0.5 / awg0 / vless, and the user was still on awg0.
```

6. Did `current_channel_failure` correctly return OK because `awg0` was OK?

```text
YES.
For selected_move.current_egress=awg0, current_channel_failure.severity=OK and confirmed=false are factually correct.
```

7. Was the diagnosis attached to selected move source rather than original incident source?

```text
YES.
_emergency_failover_move_evidence() derives current_channel_failure from the selected move's current candidate.
```

8. Is this a bug or correct behavior?

```text
For a standalone awg0 -> vless move, it is correct.
For continuation of the OpenVPN L3 incident with remaining affected users, it is a source-continuity defect.
```

## Part 4 - Incident Source vs Selected Move Source

1. Does the system preserve `incident_source` independently from `selected_move.current_egress`?

```text
NO in the observed execution path.
```

Evidence:

```text
_l3_incident_context() derives failed_sources only from gate.move_evidence.
gate.move_evidence is produced from selected moves.
Latest blocked incident 46ffebc776d1eb9fd256bf2a has failed_sources=[].
```

2. If selected move is `source=awg0`, can it legally belong to an incident whose failed source is `openvpn-1779388847-d2ad7c`?

```text
Not proven legal.
The canonical L3 entry condition is current assigned channel failed for the affected user/service context.
If the selected user's current assigned channel is awg0 and awg0 is OK, this selected move cannot prove the OpenVPN failed-channel wake.
```

3. Should L3 wake evidence be evaluated against `incident_source` or `selected_move.current_egress`?

```text
For a continuation of an existing failed-source incident, it must preserve the failed incident source and choose affected users still assigned to that source.
For a single selected move, code currently evaluates selected_move.current_egress.
```

4. Where is this rule defined?

Canonical L3 document:

```text
docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md:71-84
L3 may start only when current channel failed, users affected, required services failed, safe target exists, and freshness/authority/restore/rollback are ready.

docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md:303-320
Incident must expose failed channel, affected users/scope, failed required services, selected target or no-target blocker, and next action.
```

5. Does current code use the correct source?

```text
Current code uses selected_move.current_egress.
It does not independently carry incident_source through the selected move lifecycle.
```

6. Did `confirmed_current_channel_failure` disappear because selected move source was not failed incident source?

```text
YES.
In latest blocked execution selected_move.current_egress=awg0.
awg0 severity=OK, service failures=[], so confirmed_current_channel_failure was not produced.
```

## Part 5 - Comparative Success vs Failure Trace

| Field | Success | Latest Blocked |
| --- | --- | --- |
| operation_id | `runtime_autoswitch_1367b9f8947a3359ad4ce4e4` | `runtime_autoswitch_5cf1792f5557d5810ecfb9b6` |
| timestamp | `2026-07-02T03:25:16.066855+00:00` | `2026-07-02T09:02:56.574376+00:00` |
| incident_key | `73eb29a94ce3010d80c9a73a` | `46ffebc776d1eb9fd256bf2a` |
| user | `10.7.0.3` | `10.7.0.5` |
| source | `openvpn-1779388847-d2ad7c` | `awg0` |
| target | `awg0` | `vless` |
| selected_move_hash | `77c81719cf94321b5d368ad79529909d633123d6e161040865746b297a9d5fb4` | approved: `f9d49842548212334433eb9957674d9e3d08f2a13241e4e0f8413c87f1ddb8ff`; post-gate empty hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| incident.failed_sources | `["openvpn-1779388847-d2ad7c"]` | `[]` |
| incident.failed_required_services | `["google","google_auth","instagram","telegram","youtube"]` | `[]` |
| current_channel_failure.confirmed | proven by incident failed source and successful L3 apply | `false` |
| diagnose_severity evaluated | OpenVPN `FAIL` | awg0 `OK` |
| diagnose_reason evaluated | `interface_down_or_missing` | `OK` |
| wake accepted sources | execution succeeded | `[]` |
| observed events | OpenVPN failed-source incident existed | `[]` |
| selected_moves_before_gate | one selected move | `1` |
| selected_moves_after_gate | executed | `0` |
| blockers | none terminal | `confirmed_l3_wake_required`, `required_service_failure_required`, `restore_barrier_required_for_emergency_failover` |

First field difference explaining wake outcome:

```text
selected_move.current_egress

success = openvpn-1779388847-d2ad7c
latest blocked = awg0
```

Downstream consequence:

```text
_emergency_failover_move_evidence() evaluated awg0, not OpenVPN.
Therefore current_channel_failure.confirmed=false and current_failures=[] were correct for the selected move, but wrong for continuing the OpenVPN incident.
```

## Part 6 - Event Lifetime / TTL / Freshness

1. Is `confirmed_current_channel_failure` persisted?

```text
The bridge event itself is not persisted as an independent durable incident-source object in the observed path.
It is recomputed from selected move evidence.
```

2. If recomputed, from which artifact?

```text
v7-state.json:egress[].diagnose_severity/diagnose_reason
users.registry assignment
selected move candidate fields
```

3. Can it disappear if a later candidate uses a different source?

```text
YES. This is what happened.
```

4. Can it disappear if service matrix changes?

```text
YES, if required service failures no longer exist for the evaluated selected source.
In this case the selected source was awg0 with healthy required services.
```

5. Can it disappear if diagnose_severity is overwritten to OK?

```text
YES for the evaluated selected source.
OpenVPN was not overwritten to OK; awg0 was OK.
```

6. Can it disappear if affected user count changes?

```text
YES if affected_users_on_channel becomes zero for the evaluated source.
In this case awg0 had affected_users_on_channel=3 but severity OK, so confirmed=false.
```

7. Can it disappear after one successful user movement?

```text
YES in current implementation if the next selected move is not scoped to the same failed source.
```

8. Is there incident memory that keeps failed source active until recovered?

```text
l3-runtime-state keeps incident records, but the observed planning/wake path does not use a preserved incident_source to constrain the next selected move.
```

9. Is there a recovery condition that closes the incident?

```text
Observed successful incident 73eb29a94ce3010d80c9a73a closed after one APPLIED attempt.
No evidence in that closure shows source recovery or zero remaining affected users.
```

10. Was such recovery condition met?

```text
NO evidence found.
Current production still has 10 enabled users on failed OpenVPN.
```

11. If not, why did Wake reject?

```text
Because Wake evaluated the selected move source awg0, not the still-failed OpenVPN source.
```

## Part 7 - Recovery / Incident Closure Audit

1. Did any owner mark `openvpn-1779388847-d2ad7c` recovered?

```text
NO evidence found.
Current persisted state marks it FAIL.
```

2. Did Telegram Sentinel classify it healthy?

```text
NO. It classified it DOWN and blocked.
```

3. Did service matrix classify Telegram OK for it?

```text
NO. Telegram is TELEGRAM_DOWN_14S / FAIL.
```

4. Did v7-state classify severity OK for it?

```text
NO. v7-state classifies OpenVPN as FAIL / interface_down_or_missing.
```

5. Did admin overview classify route/service OK for it?

```text
UNKNOWN from admin API because local API returned HTTP 401.
Persisted admin-facing state artifacts classify OpenVPN as FAIL.
```

6. Did user movement reduce affected users but leave remaining users?

```text
YES. At least one success moved 10.7.0.3 off OpenVPN.
Current production still has 10 enabled users on OpenVPN.
```

7. Was the incident closed after first success despite remaining users?

```text
YES for incident 73eb29a94ce3010d80c9a73a.
status = CLOSED after one APPLIED attempt.
```

8. Is incident closure based on one-user success instead of source recovery?

```text
For the observed incident, yes.
```

9. Is that canonical?

```text
Not proven canonical.
Canonical L3 requires incident exposure of failed channel and affected users/scope.
No canonical rule found that one-user success proves source recovery or no remaining affected users.
```

## Part 8 - Multi-User Continuation Audit

1. After one user moved, how should the system continue?

```text
It should continue bounded governed execution from the same failed source while affected users remain, or prove canonical impossibility.
```

2. Does it keep the same incident open?

```text
Not in observed success incident. The incident was CLOSED after one applied move.
```

3. Does it create a new incident generation?

```text
It created later incident keys, but later blocked key 46ffebc776d1eb9fd256bf2a had failed_sources=[].
```

4. Does it require new `confirmed_current_channel_failure` each cycle?

```text
Current implementation recomputes wake from selected move evidence each cycle.
```

5. Does approved plan lock bind to the right next affected user?

```text
Not in the latest blocked execution.
It bound to 10.7.0.5 / awg0 / vless, not a remaining OpenVPN user.
```

6. Does the ladder allow another max-users=1 cycle?

```text
The artifacts show repeated one-user bounded attempts, but not a preserved OpenVPN incident-source continuation.
```

7. Does retry budget block correctly?

```text
Not the first divergence in this execution.
Latest blocked execution had wake/source evidence failure before executable selected move.
```

8. Does source scoping block incorrectly?

```text
YES. Source scoping did not constrain the next L3 candidate to remaining users on the failed OpenVPN source.
```

9. Does the next candidate come from remaining affected users?

```text
NO for latest blocked execution.
It came from 10.7.0.5 on awg0.
```

10. If not, why?

```text
Planner selection uses live decisions and optional CLI source filter.
No independent incident_source was preserved and consumed by selection/wake to force continuation on openvpn-1779388847-d2ad7c.
```

## First Divergence

The first factual divergence is:

```text
selected_move.current_egress changed from the failed incident source to a healthy non-incident source.
```

Exact transition:

```text
Successful OpenVPN incident:
  incident_key = 73eb29a94ce3010d80c9a73a
  failed_sources = ["openvpn-1779388847-d2ad7c"]
  selected_move.current_egress = openvpn-1779388847-d2ad7c
  status = CLOSED after one APPLIED move

Latest blocked execution:
  incident_key = 46ffebc776d1eb9fd256bf2a
  failed_sources = []
  selected_move.current_egress = awg0
  current_channel_failure.severity = OK
```

First code owner where this becomes executable state:

```text
tools/v7-users-autoswitch::plan()
tools/v7-users-autoswitch::_select_moves()
```

First code owner where the failed-source fact becomes false/OK:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
```

Why:

```text
_emergency_failover_move_evidence() evaluates selected_move.current_egress.
For latest blocked execution selected_move.current_egress = awg0.
awg0 diagnose_severity = OK.
Therefore current_channel_failure.confirmed = false is correct for awg0, but the execution is no longer scoped to the OpenVPN incident.
```

## Primary Classification

```text
INCIDENT_SOURCE_NOT_PRESERVED
```

Secondary observed effects:

```text
SELECTED_MOVE_SOURCE_MISMATCH
WAKE_EVALUATES_WRONG_SOURCE
INCIDENT_CLOSED_TOO_EARLY
```

These are secondary because the durable OpenVPN failure fact exists in production; the failure is the loss of source continuity from incident to next selected move/wake evaluation.

## Safe Fix Direction

Do not bypass Wake, Authority, Restore Barrier, Runtime, or Planner.
Do not enable broad automation.
Do not move more than one user per bounded cycle.
Do not create a new owner.

Minimal safe correction direction:

```text
Owner: tools/v7-users-autoswitch, with existing governed owner input from tools/v7-governed-canary-dry-run-cycle.

Preserve incident_source independently from selected_move.current_egress for L3 continuation.

When an L3 incident source remains failed and has enabled affected users:
  - constrain Planner selection to remaining users whose current assignment equals incident_source;
  - require approved plan lock selected move source to match incident_source;
  - evaluate confirmed_current_channel_failure against incident_source / selected affected user on that source;
  - keep one-user bounded Restore Barrier and Authority behavior unchanged;
  - close or suspend the failed-source incident only when source recovery, zero affected users, rollback/containment terminal rule, or canonical impossibility is proven.
```

Patch required:

```text
PATCH_REQUIRED
```

## Final Verdict

```text
primary classification = INCIDENT_SOURCE_NOT_PRESERVED
first divergence = selected_move.current_egress became awg0 while failed incident source remained openvpn-1779388847-d2ad7c in production reality
exact owner/function = tools/v7-users-autoswitch::plan() / _select_moves(); first false OK evidence produced by _emergency_failover_move_evidence()
failed source current status = FAIL, interface_down_or_missing, service matrix FAIL, Telegram DOWN
remaining affected users = 10
safe fix direction = preserve incident_source and constrain bounded L3 continuation to remaining users on failed source through existing Planner/Wake/Authority/Restore Barrier/Runtime owners
PATCH_REQUIRED
```
