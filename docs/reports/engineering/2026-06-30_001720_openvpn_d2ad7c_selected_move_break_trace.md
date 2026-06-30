# OpenVPN d2ad7c Selected Move Break Trace

Дата: 2026-06-30
Режим: read-only audit + local fixture reproduction
Канал: `openvpn-1779388847-d2ad7c`
Фокусный пользователь: `10.7.0.11`

Evidence:

- Previous live evidence: `docs/reports/engineering/live_openvpn_audit_2026-06-29/`
- Current browser/API evidence: `docs/reports/engineering/live_openvpn_trace_2026-06-30/browser_api/`
- Local fixture evidence: `docs/reports/engineering/live_openvpn_trace_2026-06-30/`

## Summary

Точная точка поломки найдена.

`SWITCH_AVAILABLE` ломается не в service recommendation layer и не в current eligibility.

Planner correctly detects that `openvpn-1779388847-d2ad7c` is not eligible for the affected users. Safe targets exist. If restore barrier is disabled in a local fixture, the same user gets a visible failover proposal:

- `action=switch`
- `move_type=failover`
- `reason=current_egress_not_eligible`
- `recommended_egress=vless`
- `selected_move_count=1`

With restore barrier active, the same user remains:

- `action=keep`
- `move_type=none`
- `reason=restore_barrier_failover_suppressed`
- `selected_move_count=0`

Therefore the first real break point is:

`tools/v7-users-autoswitch:5285-5289`

The restore barrier suppresses failover proposal generation itself, instead of allowing a proposal to remain visible and blocking only execution/apply.

There is a second confirmed issue:

`/api/autoswitch-plan` returns `plan=null`, so the operator surface cannot reliably display planner why-cards. The API wrapper runs the correct CLI owner, but the materialized JSON plan is lost in `admin/v7-admin-api:15953-15979`.

## Live State Confirmed

Production state remains consistent with the previous live audit:

- 14 users assigned to `openvpn-1779388847-d2ad7c`.
- Route installation is OK.
- Service matrix status is `FAIL`.
- `ok_count=0`, `total=14`.
- User-relevant services fail through this channel.
- Service recommendation layer reports `SWITCH_AVAILABLE` / `manual_switch_available`.
- Safe alternate targets exist.

## One-User Full Decision Trace

User: `10.7.0.11`

### 1. Current Assignment

Input:

- user `10.7.0.11`
- current channel `openvpn-1779388847-d2ad7c`

Owner:

- `tools/v7-users-autoswitch:2258-2276`

Result:

- user is active and assigned to `openvpn-1779388847-d2ad7c`.

Move status:

- not dropped.

### 2. Required Services

Input:

- default user priority services
- route class derived as `VIDEO_OPTIMIZED`

Owner:

- `tools/v7-users-autoswitch:399-405`
- `tools/v7-users-autoswitch:5254-5256`

Result:

- `youtube`, `instagram`, `telegram`, `google`, `google_auth`

Move status:

- not dropped.

### 3. Current Candidate Construction

Input:

- current egress `openvpn-1779388847-d2ad7c`
- purpose `current`
- required services above

Owner:

- `tools/v7-users-autoswitch:5261`
- `tools/v7-users-autoswitch:5544-5561`

Branch:

- `_candidate(... purpose="current")`

Result:

- current candidate is constructed.

Move status:

- not dropped.

### 4. Current Service Suitability

Owner:

- `tools/v7-users-autoswitch:5734-5795`

Important result:

- `_gate_service` is called for `purpose="current"`.
- Service failure does affect the current candidate.

Local fixture result for `openvpn-1779388847-d2ad7c`:

- `eligible=false`
- blocked includes `telegram_required_telegram_down_14s`
- load status for current is `HARD_FULL`
- current score `0.0`

Verdict:

- Hypothesis A is false.
- Planner does not incorrectly keep current eligible.

Move status:

- failover should begin after this point.

### 5. Failover Condition

Owner:

- `tools/v7-users-autoswitch:5278-5304`

Expected branch:

- `elif not current or not current.eligible`

Actual branch:

- branch is entered.
- then `restore_barrier_failover_suppressed` is emitted before failover candidates are evaluated.

Exact condition:

`tools/v7-users-autoswitch:5285-5289`

```text
if current and restore_barrier.failover_quarantine:
    reason.append("restore_barrier_failover_suppressed")
```

Result:

- action remains `keep`.
- recommended egress remains current.
- no failover proposal is created.

Move status:

- never created because failover proposal generation is suppressed.

### 6. Candidate Target List

Even when proposal is suppressed, candidate construction shows safe targets exist.

Local fixture target candidates:

- `vless`: eligible, service OK
- `awg3`: eligible, service OK
- `awg0`: eligible, service OK
- `wireguard-1779454504-c43409`: eligible, service OK

Blocked target example:

- `amneziawg-exec-20260528-10-8-1-14` is service-good but blocked by manual/reserve/canary flags in the local fixture path.

Move status:

- safe targets exist; target suitability is not the root cause.

### 7. Ranking And Best Target

Counterfactual fixture with restore barrier disabled:

- best target for `10.7.0.11`: `vless`
- score: `2170.34`
- action: `switch`
- move type: `failover`
- reason: `current_egress_not_eligible`

Evidence:

- `docs/reports/engineering/live_openvpn_trace_2026-06-30/counterfactual_user_no_target.json`

Move status:

- created successfully when restore barrier does not suppress proposal generation.

### 8. Selected Move Creation

Counterfactual:

- `selected_move_count=1`
- selected user `10.7.0.11`
- selected target `vless`

Restore-barrier-active fixture:

- `selected_move_count=0`
- reason `restore_barrier_failover_suppressed`

Failure point:

- proposal is prevented before selected move can exist.

### 9. Target-Egress Filtering

Owner:

- `tools/v7-users-autoswitch:4046-4052`
- CLI help: `tools/v7-users-autoswitch:6543`

Confirmed semantics:

- `--target-egress` means "Limit selected autoswitch moves to users recommended for this egress."
- It is a movements-to-target filter.
- It is not an evacuation-from-source/current-channel filter.

Therefore:

- `/api/autoswitch-plan?egress=openvpn-1779388847-d2ad7c` is not the correct query for evacuating users currently on that channel.

Verdict:

- Hypothesis C is true.

### 10. Restore-Barrier Check

Owners:

- failover suppression: `tools/v7-users-autoswitch:5285-5289`
- selected move clearance: `tools/v7-users-autoswitch:4086-4155`
- selected move diagnostics: `tools/v7-users-autoswitch:4237-4250`

Observed production API terminal reasons:

- no-target plan: `dry_run_restore_barrier_clearance_selected_moves_exceed_budget`
- best-target plan: `dry_run_restore_barrier_clearance_generation_expired`
- bad-target plan: `dry_run_restore_barrier_clearance_generation_expired`

Local fixture root behavior:

- failover proposal is suppressed by `restore_barrier_failover_suppressed`.

Verdict:

- Hypothesis D is true.
- Restore barrier currently suppresses proposal generation for current-channel failover, not only execution/apply.

### 11. API Wrapper Materialization

Owner:

- `admin/v7-admin-api:15953-15979`
- `admin/v7-admin-api:15982-16005`

Observed:

- `/api/autoswitch-plan` returns `plan=null`.
- response includes only an output tail.
- output starts mid-JSON/object, so operator surface loses structured decisions.

Local fixture:

- direct CLI stdout is valid JSON.

Verdict:

- Hypothesis E is true.
- The API wrapper does not reliably materialize the planner JSON when output is too large/truncated or otherwise not parseable.

## All-Users Consistency Check

Affected users: 14.

With restore barrier active in the fixture:

- affected users: 14
- action: `keep` for all 14
- reason: `restore_barrier_failover_suppressed` for all 14
- current score: `0.0` for all 14

With restore barrier disabled in the counterfactual fixture:

- affected users: 14
- action: `switch` for all 14
- move_type: `failover` for all 14
- recommendation: `vless` for all 14
- reason: `current_egress_not_eligible`
- selected move count remains bounded by existing policy/authority selection.

Evidence:

- `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target_affected_summary.json`
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/counterfactual_all_no_target_affected_summary.json`

## Hypotheses Tested

### A. Current channel remains eligible despite service FAIL

Verdict: FALSE.

`_gate_service` is called for current candidate. In the fixture, current is ineligible and score is `0.0`.

### B. Recommendation and planner use different truth sources

Verdict: PARTIAL, not the root cause.

Both layers see service failure and safe alternatives. Service recommendation directly exposes `SWITCH_AVAILABLE`; planner also marks current ineligible in the fixture. The break happens after current ineligibility, not before it.

### C. Target-only semantics breaks evacuation-from-current

Verdict: TRUE.

`egress=` in `/api/autoswitch-plan?egress=...` maps to `--target-egress`, which filters by recommended target. It does not mean "evacuate current/source egress."

### D. Restore barrier suppresses proposal

Verdict: TRUE.

`restore_barrier_failover_suppressed` prevents failover proposal generation before selected move creation.

### E. Admin API loses JSON plan

Verdict: TRUE.

`plan=null` is observed in production API. Direct CLI in fixture emits valid JSON. API materialization is failing for the production-sized plan.

### F. Capacity overload blocks evacuation

Verdict: FALSE as root cause.

Current channel is overloaded (`14` users vs registry hard limit `2`, fixture dynamic hard limit `14`), but target capacity exists. Current overload is additional evidence for evacuation, not the reason no proposal appears.

### G. Authority disabled explains no execution but not no proposal

Verdict: TRUE.

Authority may block execution/apply. It should not hide a governed evacuation proposal or why-card.

## Exact Failure Point

Primary failure:

`tools/v7-users-autoswitch:5285-5289`

The restore barrier suppresses failover proposal generation:

```text
restore_barrier_failover_suppressed
```

This converts:

```text
current ineligible + safe target exists
```

into:

```text
keep current, no selected evacuation move
```

Secondary failure:

`admin/v7-admin-api:15953-15979`

The API plan wrapper returns `plan=null`, so the UI/operator read-model cannot consume full structured planner decisions.

Tertiary workflow issue:

`tools/v7-users-autoswitch:4046-4052`

`target_egress` is movements-to-target, not evacuate-from-source. The UI/API needs explicit source/current-channel evacuation semantics or must not label target-filter output as current-channel evacuation readiness.

## Code Owners and Line Ranges

- `tools/v7-users-autoswitch:5254-5369`: per-user decision.
- `tools/v7-users-autoswitch:5261`: current candidate construction.
- `tools/v7-users-autoswitch:5278-5304`: current-not-eligible failover branch.
- `tools/v7-users-autoswitch:5285-5289`: restore-barrier failover suppression.
- `tools/v7-users-autoswitch:5544-5561`: candidate gates.
- `tools/v7-users-autoswitch:5734-5795`: service suitability gate.
- `tools/v7-users-autoswitch:4046-4052`: target-egress filtering.
- `tools/v7-users-autoswitch:4086-4155`: restore-barrier selected move clearance.
- `tools/v7-users-autoswitch:4237-4250`: selected move diagnostics.
- `tools/v7-users-autoswitch:6543`: target-egress CLI semantics.
- `admin/v7-admin-api:15953-15979`: command output capture and JSON parse.
- `admin/v7-admin-api:15982-16005`: autoswitch plan API command.

## Is This Expected?

Execution block: expected.

Proposal suppression: not expected.

Correct behavior should be:

```text
proposal_available = true
execution_blocked = true
execution_blocker = restore_barrier / authority / live gate
```

Current behavior is closer to:

```text
proposal hidden or never created
selected_move_count = 0
operator surface plan = null
```

## Is This Bug?

Yes.

Confirmed bug classes:

- `BUG_TARGET_FILTER_USED_AS_SOURCE_EVACUATION_QUERY`
- `BUG_RESTORE_BARRIER_SUPPRESSES_PROPOSAL`
- `BUG_ADMIN_API_PLAN_JSON_NOT_MATERIALIZED`
- `EXPECTED_EXECUTION_BLOCKED_BUT_UI_EXPLAINABILITY_GAP`

Not confirmed:

- `BUG_CURRENT_ELIGIBILITY_SERVICE_FAILURE_NOT_PROPAGATED`

Current eligibility works.

## Minimal Patch Proposal, NOT APPLIED

No patch was applied during this audit.

### Patch 1: Preserve Proposal When Restore Barrier Blocks Execution

File:

- `tools/v7-users-autoswitch`

Function:

- `_decision_for_user`

Change:

- Do not convert current ineligible failover into `keep` solely because restore barrier is active.
- Instead produce the failover proposal with a diagnostic:
  - `proposal_available=true`
  - `execution_blocked=true`
  - `execution_blocker=restore_barrier_failover_suppressed`

Safety:

- Do not allow apply.
- Do not bypass restore barrier.
- Do not increase selected executable moves.

### Patch 2: Separate Proposal Count From Executable Selected Moves

File:

- `tools/v7-users-autoswitch`

Functions:

- `plan`
- selected move diagnostics area

Change:

- Add separate fields:
  - `proposal_moves`
  - `proposal_move_count`
  - `execution_selected_moves`
  - `execution_selected_move_count`
  - `execution_blocked_reason`

Safety:

- Runtime execution continues to consume only execution-selected moves.
- Operator/UI can still see why evacuation is needed.

### Patch 3: Add Source/Current-Channel Evacuation Query

Files:

- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`

Change:

- Keep existing `--target-egress` unchanged.
- Add explicit source/current filter, for example:
  - `--source-egress`
  - `/api/autoswitch-plan?source_egress=...`

Safety:

- Read-only plan by default.
- No apply.

### Patch 4: Fix API Plan Materialization

File:

- `admin/v7-admin-api`

Function:

- `run_json_command`

Change:

- Ensure structured plan is not lost when stdout is large.
- Options:
  - stream command JSON to a temp file and parse the full file;
  - request compact JSON from CLI for API calls;
  - return a summarized structured plan instead of tail-only output.

Safety:

- No runtime behavior change.
- UI/operator observability improves.

## Tests Needed

1. Current channel service FAIL + safe target exists -> current candidate ineligible.
2. Restore barrier active -> proposal visible, execution blocked.
3. Restore barrier inactive -> failover selected normally.
4. `--target-egress` filters by recommended target only.
5. New source/current-channel filter returns users currently on that channel.
6. API `/api/autoswitch-plan` returns non-null structured plan for large planner output.
7. UI shows:
   - proposal available;
   - execution blocked;
   - exact blocker.

## Production Risk

Current risk:

- Operators cannot see a governed evacuation proposal for users on a service-failed channel.
- A true service failure may appear as "no selected moves" or `plan=null`.
- This can strand users on a bad channel while the system already knows alternatives exist.

Patch risk:

- Low if proposal and execution are kept separate.
- Do not change apply path.
- Do not bypass restore barrier.
- Do not enable automation.

## Canonical Knowledge Changes

NONE.

This is implementation/workflow materialization under existing owners:

- Movement Protection
- Runtime Eligibility
- Operator Explainability
- Governed Transaction
- Autoswitch Planner
- Admin Operator Surface

## Final Verdict

Confirmed:

- `BUG_TARGET_FILTER_USED_AS_SOURCE_EVACUATION_QUERY`
- `BUG_RESTORE_BARRIER_SUPPRESSES_PROPOSAL`
- `BUG_ADMIN_API_PLAN_JSON_NOT_MATERIALIZED`
- `EXPECTED_EXECUTION_BLOCKED_BUT_UI_EXPLAINABILITY_GAP`

Rejected:

- `BUG_CURRENT_ELIGIBILITY_SERVICE_FAILURE_NOT_PROPAGATED`

Need New Owner: FALSE
Need New Backlog Item: FALSE
Need New Architecture: FALSE
Runtime Changed: NO
Users Moved: NO
Patch Applied: NO
