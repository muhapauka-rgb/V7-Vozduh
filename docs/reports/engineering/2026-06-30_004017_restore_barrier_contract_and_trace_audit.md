# Restore Barrier Contract + Runtime Trace Audit

Date: 2026-06-30
Workspace: `/Users/ponch/Documents/New project`
Scope: read-only audit. No runtime mutation, no user movement, no automation enablement, no patch applied.

## Summary

The canonical contract is **Contract A: proposal-visible, execution-blocked**.

The restore barrier is intended to protect the irreversible execution/apply boundary, not to hide the planner proposal or why-card. Current implementation follows an older safety branch that suppresses failover proposal creation when `restore_barrier.failover_quarantine=true`.

Primary classification: `CONTRACT_VIOLATION_BUG`.

Secondary confirmed issues:

- `BUG_RESTORE_BARRIER_SUPPRESSES_PROPOSAL`
- `BUG_ADMIN_API_PLAN_JSON_NOT_MATERIALIZED`
- `BUG_TARGET_FILTER_USED_AS_SOURCE_EVACUATION_QUERY`
- `EXPECTED_EXECUTION_BLOCKED_BUT_UI_EXPLAINABILITY_GAP`

Canonical knowledge changes: `NONE`. Existing canonical owners already define the intended separation.

## Part 1 - Canonical Contract Discovery

### Canonical References Supporting Contract A

| Source | Classification | Evidence | Contract |
| --- | --- | --- | --- |
| `docs/reference/V7_DECISION_MODEL.md:184-190` | canonical | Law 1 states Decision != Execution. V7 keeps decisions read-only until explicit execution authority exists. Restore barrier is listed as part of that separation. | A |
| `docs/reference/V7_DECISION_MODEL.md:442-450` | canonical | Prepared Plan is advisory candidate/action artifact produced before live execution; Runtime Eligibility and Execution Eligibility are separate concepts. | A |
| `docs/reference/V7_DECISION_MODEL.md:452-474` | canonical | Flow is Current State -> Desired Safe State -> Delta -> Prepared Plan -> Runtime Eligibility -> Execution Eligibility -> Execution. Prepared Plan is advisory until live gates pass. | A |
| `docs/reference/V7_DECISION_MODEL.md:317-324` | canonical | Safety must remain visible in every decision output. | A |
| `docs/reference/V7_RUNTIME_MODEL.md:49` | canonical | Runtime model repeats Decision != Execution. | A |
| `docs/reference/V7_RUNTIME_MODEL.md:203` | canonical | Rollback readiness gate can stop on restore-barrier failure, but this is modeled as a gate before action. | A |
| `docs/reference/V7_RUNTIME_MODEL.md:353` | canonical | Execution Plane performs the shortest safe execute-or-stop action. | A |
| `docs/reference/V7_RUNTIME_MODEL.md:519` | canonical | `runtime_eligibility_arbitration` may report read-only advisory state and must not enable apply or bypass gates. | A |
| `docs/reference/SYSTEM_MAP.md:56` | canonical | Execution Plane owns lease-bound, fail-closed execute-or-stop path. | A |
| `docs/reference/SYSTEM_MAP.md:118` | canonical | Event-driven chain is regression -> planner -> packet -> restore barrier -> bounded apply. Planner is before restore barrier. | A |
| `docs/programs/V7_IMPLEMENTATION_BACKLOG.md:124-134` | program | A6 owns runtime eligibility arbitration and live gate ordering; no new owner/path. | A |
| `docs/programs/V7_IMPLEMENTATION_BACKLOG.md:155-158` | program | A3 owns restore barrier/governed execution; A6 consumes A1-A5 gates and returns read-only execute-or-stop rows. | A |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md:4820` | program | RT2-S4 maps prepared plan, packet, lease, restore barrier, verification and rollback; every live action still revalidates gates and requires authority. | A |
| `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md:21-33` | ADR | Chain places planner before packet/restore barrier/apply. | A |
| `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md:85-94` | ADR | Required phase runs planner in preview, builds packet, validates restore barrier/rollback, then proves bounded apply eligibility. | A |
| `docs/decisions/ADR-AUTONOMY-RISK-TIERED-FLOORS.md:22-29` | ADR | Candidate must exist; packet/restore barrier/operator approval/apply are later gates. | A |

### Evidence Supporting Contract B

No canonical document found supporting Contract B as the current intended product/runtime contract.

Contract B exists as implementation behavior in:

- `tools/v7-users-autoswitch:5285-5289`

That branch suppresses failover proposal creation while restore barrier quarantine is active. This is code-level behavior, not canonical product/runtime intent.

## Part 2 - Git / History Discovery

| Commit | Date | Message | Relevant files | Intent inferred | Contract |
| --- | --- | --- | --- | --- | --- |
| `736f0354` | 2026-05-28 15:23:47 +0300 | `Update V7 governance and operator execution state` | `tools/v7-users-autoswitch`, `admin_core/operator_execution.py`, many governance reports | Introduced `restore_barrier_failover_suppressed`, `failover_quarantine`, and selected-move clearance fields. Intent was safety-first governance during restore/apply hardening. | B as legacy implementation behavior |
| `eced6689` | 2026-06-06 20:04:48 +0300 | `Lock governed apply to approved selected moves` | `tools/v7-users-autoswitch` | Hardened apply identity around approved selected moves. This protects execution identity, not proposal visibility. | A |
| `6f4ef071` | 2026-06-06 10:06:28 +0300 | `Fix autoswitch source stability lease` | `tools/v7-users-autoswitch` | Lease/source stability hardening. | A |
| `7e3a61ef` | 2026-06-05 14:31:00 +0300 | `PROGRAM Atomic execution envelope binding` | `tools/v7-users-autoswitch` | Atomic envelope binds selected moves for apply safety. | A |
| `3b894b86` | 2026-05-18 15:45:29 +0300 | `Complete autoswitch quality safety UI` | `admin/v7-admin-api` | Introduced read-only `/api/autoswitch-plan` surface with parsed `plan` plus raw `output`. | A |
| `fb1e8fc6` | 2026-06-11 21:28:31 +0300 | `Close SNAP.1 admin planner refresh path` | `tools/v7-users-autoswitch`, `admin/v7-admin-api` | Added/extended `--target-egress` planner refresh path. Semantics are target filter, not source evacuation. | Ambiguous for evacuation UI |
| `a8f2d432` | 2026-05-19 01:14:40 +0300 | `Update V7 admin profile provisioning` | `tools/v7-users-autoswitch`, `admin/v7-admin-api` | Earlier target-egress/planner work. | Ambiguous for evacuation UI |

Relevant diff evidence from `736f0354:tools/v7-users-autoswitch`:

- `failover_quarantine = enabled and (active or post_ttl_blocking)`
- if current is ineligible and `failover_quarantine` is true, append `restore_barrier_failover_suppressed`
- otherwise compute `failover_candidates`

This shows the proposal-suppression branch was introduced as a safety mechanism, but later canonical decision/execution documents require proposal visibility and execution blocking instead.

## Part 3 - Runtime Trace With Real Values

Evidence directory:

- `docs/reports/engineering/live_openvpn_trace_2026-06-30/`

Affected user used for fixture trace: `10.7.0.11`.

### Active Restore Barrier Trace

Source file: `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_user_no_target.json`

| Step | File:line | Variable/value | Branch | Result |
| --- | --- | --- | --- | --- |
| 1 | `tools/v7-users-autoswitch:5255-5261` | `current_egress=openvpn-1779388847-d2ad7c`; services include `youtube`, `instagram`, `telegram`, `google`, `google_auth`; route class `VIDEO_OPTIMIZED` | build candidates and current candidate | current evaluated before decision |
| 2 | `tools/v7-users-autoswitch:5261` | current candidate score `0.0`; current service blocks include `telegram_required_telegram_down_14s`; load state includes `HARD_FULL` in fixture evidence | current candidate | `current.eligible=false` |
| 3 | `tools/v7-users-autoswitch:5262` | eligible targets exist: `vless`, `awg3`, `awg0`, `wireguard-1779454504-c43409` | target candidates exist | safe target candidates are present before suppression |
| 4 | `tools/v7-users-autoswitch:5278` | `not current or not current.eligible = true` | current-not-eligible branch entered | failover path considered |
| 5 | `tools/v7-users-autoswitch:5285` | `restore_barrier.failover_quarantine=true` | restore barrier branch wins | failover candidate evaluation skipped |
| 6 | `tools/v7-users-autoswitch:5289` | reason appended: `restore_barrier_failover_suppressed` | suppression | proposal hidden |
| 7 | `tools/v7-users-autoswitch:5293-5304` | failover candidate block not executed | skipped | no `current_egress_not_eligible` proposal |
| 8 | plan result | `action=keep`; `move_type=none`; `recommended_egress=openvpn-1779388847-d2ad7c` | final decision | user remains on failed channel in plan |
| 9 | operation | `selected_move_count=0`; `terminal_reason=dry_run_restore_barrier_active` | read-only dry-run | no execution, but no visible evacuation proposal either |

Restore barrier values from fixture safety block:

- `enabled=true`
- `active=true`
- `expired=false`
- `cleared=true`
- `post_ttl_blocking=false`
- `failover_quarantine=true`
- `clearance_max_selected_moves=0`
- `clearance_generation_id=fixture-generation`
- `generation_token=fixture`

## Part 4 - Counterfactual Verification

### Fixture A - Restore Barrier Active

File: `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_user_no_target.json`

Result:

- `current_egress=openvpn-1779388847-d2ad7c`
- `recommended_egress=openvpn-1779388847-d2ad7c`
- `action=keep`
- `move_type=none`
- `reason=["restore_barrier_failover_suppressed"]`
- `selected_move_count=0`
- `terminal_reason=dry_run_restore_barrier_active`
- eligible targets exist but are not exposed as failover proposal

All affected users summary:

File: `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target_affected_summary.json`

- affected users: `14`
- affected actions: `keep=14`
- affected move types: `none=14`
- affected recommendation: `openvpn-1779388847-d2ad7c=14`
- affected reason: `restore_barrier_failover_suppressed=14`

### Fixture B - Restore Barrier Disabled Only In Fixture

File: `docs/reports/engineering/live_openvpn_trace_2026-06-30/counterfactual_user_no_target.json`

Result:

- `current_egress=openvpn-1779388847-d2ad7c`
- `recommended_egress=vless`
- `action=switch`
- `move_type=failover`
- `reason=["current_egress_not_eligible"]`
- `selected_move_count=1`
- `terminal_reason=dry_run_selected_moves_available`

All affected users summary:

File: `docs/reports/engineering/live_openvpn_trace_2026-06-30/counterfactual_all_no_target_affected_summary.json`

- affected users: `14`
- affected actions: `switch=14`
- affected move types: `failover=14`
- affected recommendation: `vless=14`
- selected move count remains bounded to `1`

Conclusion: identical input except restore barrier state changes proposal visibility. The restore barrier is suppressing proposal generation, not only execution.

## Part 5 - API Materialization Deep Check

API owner:

- `admin/v7-admin-api:15953-15979` (`run_json_command`)
- `admin/v7-admin-api:15982-16005` (`autoswitch_read_only_plan_command`, `autoswitch_plan_state`)

Behavior:

- command runs `v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --pretty`
- stdout is captured and truncated to the last `max_output=5_000_000` bytes for parsing
- API response returns only `output[-12000:]`
- if `json.loads(output)` fails, `plan=None`
- parse exception is not returned to the caller

Production API evidence:

- `docs/reports/engineering/live_openvpn_trace_2026-06-30/browser_api/autoswitch_plan_all_after_timeout.json`
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/browser_api/autoswitch_plan_best_target_after_timeout.json`
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/browser_api/autoswitch_plan_bad_target_after_timeout.json`

Observed:

| API call | rc | plan | output length | output starts | direct parse of returned output |
| --- | --- | --- | --- | --- | --- |
| `/api/autoswitch-plan` | `0` | `null` | `12000` | starts at `"hard_limit": 20` inside JSON | `JSONDecodeError: Extra data` |
| `/api/autoswitch-plan?egress=amneziawg...` | `0` | `null` | `12000` | starts at `imit": 20` inside JSON | `JSONDecodeError: Expecting value` |
| `/api/autoswitch-plan?egress=openvpn...` | `0` | `null` | `12000` | starts at `"hard_limit": 20` inside JSON | `JSONDecodeError: Extra data` |

Direct local fixture CLI emits valid JSON and was saved successfully under:

- `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_user_no_target.json`
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/counterfactual_user_no_target.json`

Classification: `output truncation / command contract materialization bug`.

The API does not prove planner absence. It proves the admin API fails to materialize the plan JSON for production-sized output.

## Part 6 - Source Evacuation Semantics

CLI semantics:

- `tools/v7-users-autoswitch:4046-4052`
- `tools/v7-users-autoswitch:6543`

`--target-egress` means: limit selected autoswitch moves to users recommended **to** this egress.

Admin API / UI:

- `admin/v7-admin-api:15982-16005` maps query `egress` to `--target-egress`
- `admin/v7-admin-api:37649-37653` exposes `/api/autoswitch-plan?egress=...`
- `admin/v7-admin-api:29601-29606` channel drawer calls `/api/autoswitch-plan?egress=<channel>`
- `admin/v7-admin-api:29578-29590` channel autoswitch table filters `recommended_egress === id`

Therefore a channel drawer for `openvpn-1779388847-d2ad7c` asks:

> "Who should move TO openvpn?"

It does not ask:

> "Who is currently ON openvpn and should evacuate FROM it?"

There is partial UI logic elsewhere that can inspect `current_egress` in assignment surfaces (`admin/v7-admin-api:27995-28002`), but `/api/autoswitch-plan` has no source/current-channel evacuation query.

Current answer: no existing correct API query was found for "show evacuation proposal for users currently on this channel."

Minimal needed semantics, not implemented:

- add a source/current-egress filter to the existing plan surface, e.g. `source_egress` or `current_egress`;
- preserve `--target-egress` as target filter;
- channel drawer evacuation view should use source semantics for "users currently on this channel";
- selected/apply behavior must remain unchanged and fail-closed.

## Part 7 - Decision Classification

Primary classification: `CONTRACT_VIOLATION_BUG`.

Why:

1. Canonical Decision Model and Runtime Model separate proposal/decision visibility from execution/apply.
2. Restore barrier belongs at execution eligibility / apply safety boundary.
3. Current code uses restore barrier during proposal construction and prevents failover candidates from being evaluated.
4. This makes the operator/UI see no evacuation proposal for users on a failed channel, even though safe targets exist.

Historical note:

- `restore_barrier_failover_suppressed` appears to be legacy safety behavior from `736f0354`.
- That behavior was reasonable during early governed execution hardening, but it now conflicts with the canonical proposal-visible decision model.

Secondary issues:

- `BUG_TARGET_FILTER_USED_AS_SOURCE_EVACUATION_QUERY`
- `BUG_ADMIN_API_PLAN_JSON_NOT_MATERIALIZED`
- `EXPECTED_EXECUTION_BLOCKED_BUT_UI_EXPLAINABILITY_GAP`

## Part 8 - Minimal Patch Plan, Not Applied

### 1. Restore Barrier Proposal / Execution Semantics

File: `tools/v7-users-autoswitch`

Function: `_decision_for_user`

Current branch:

- `tools/v7-users-autoswitch:5278-5304`

Intended behavior:

- if current is ineligible, compute failover candidates even when restore barrier quarantine is active;
- expose `action=switch`, `move_type=failover`, `recommended_egress=<best target>`, and `reason=current_egress_not_eligible`;
- add an execution-only blocker such as `restore_barrier_execution_blocked` or equivalent existing field;
- selected moves/apply must remain blocked while restore barrier is active.

Safety invariant:

- no restore barrier bypass;
- no increased authority;
- no automatic movement;
- restore barrier still blocks selected execution/apply.

Test needed:

- current ineligible + safe target + restore barrier active -> proposal visible, selected/apply blocked;
- current ineligible + safe target + restore barrier inactive -> proposal visible, selected bounded by authority;
- no eligible target -> no proposal.

Rollback plan:

- revert only this branch; restore previous suppression behavior.

### 2. API Plan Materialization

File: `admin/v7-admin-api`

Function: `run_json_command`

Current lines:

- `admin/v7-admin-api:15953-15979`

Intended behavior:

- parse complete stdout before truncating display output;
- return parse errors in diagnostics;
- keep raw/tail output for UI display only;
- if CLI emits non-JSON logs, extract the JSON object through a strict command contract or compact JSON mode.

Safety invariant:

- read-only endpoint remains read-only;
- no apply, no restore write, no user movement.

Test needed:

- large valid JSON stdout parses into `plan`;
- truncated display output does not affect `plan`;
- invalid stdout returns `plan=null` plus parse diagnostic.

Rollback plan:

- revert API parser change.

### 3. Source / Current-Channel Evacuation Query

Files:

- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`

Functions:

- `plan`
- `autoswitch_read_only_plan_command`
- `autoswitch_plan_state`
- channel drawer caller around `admin/v7-admin-api:29601-29606`

Intended behavior:

- add read-only source/current-egress query semantics for evacuation view;
- do not overload `--target-egress`;
- source filter shows users currently on the channel and their proposed evacuation or blocker reason.

Safety invariant:

- source filter cannot widen apply authority;
- guarded apply must still require exact bounded execution authority.

Test needed:

- `source_egress=openvpn...` returns users currently on openvpn;
- `target_egress=vless` remains users recommended to vless;
- source view does not imply apply.

Rollback plan:

- remove source query path and return to global plan only.

### 4. UI / Operator Wording

File: `admin/v7-admin-api`

Functions:

- `channelAutoswitchPlanHtml`
- channel drawer loading functions

Intended behavior:

- channel drawer should distinguish:
  - "users to move TO this channel";
  - "users currently ON this channel needing evacuation";
  - "proposal visible, execution blocked by restore barrier."

Safety invariant:

- display-only change;
- no runtime mutation.

Test needed:

- failed source channel with restore barrier active displays evacuation proposal plus execution blocker.

Rollback plan:

- revert UI wording.

## Final Answers

1. Restore barrier intended to suppress proposal or only execution?

Only execution/apply. Proposal and why-card should remain visible.

2. Bug or historical contract/product gap?

Current behavior is a `CONTRACT_VIOLATION_BUG` against current canonical model, with historical origin in an older safety branch.

3. Exact code path causing users to remain on failed channel.

`tools/v7-users-autoswitch:5278-5304`, specifically `5285-5289`: when current is ineligible and `restore_barrier.failover_quarantine=true`, the planner appends `restore_barrier_failover_suppressed` and skips failover candidate evaluation. Final decision remains `keep`.

4. Exact code path causing UI/API `plan=null`.

`admin/v7-admin-api:15953-15979`: `run_json_command` parses stdout after capture; production output returned to UI is a truncated tail beginning mid-JSON, so the exposed `plan` is `null`. Endpoint path is `admin/v7-admin-api:15995-16005` and route is `37649-37653`.

5. Smallest safe next implementation step.

Patch only the existing autoswitch owner so restore barrier blocks execution/selected apply, not proposal visibility. Then patch admin API plan materialization. Then add source/current-egress evacuation query semantics for the channel drawer. No new owner, no new runtime path, no authority expansion.

