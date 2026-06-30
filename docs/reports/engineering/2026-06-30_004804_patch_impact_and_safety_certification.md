# Patch Impact & Safety Certification

Date: 2026-06-30
Workspace: `/Users/ponch/Documents/New project`
Scope: read-only impact audit. No patch, no runtime mutation, no user movement, no automation enablement.

## Summary

Root cause investigation is complete enough to begin implementation, but only under a strict patch boundary.

The safe implementation is **not** "remove `restore_barrier_failover_suppressed` and let the current flow continue."

The safe implementation is:

1. keep failover proposal visible in `decisions`;
2. add/strengthen an execution-only restore-barrier gate after proposal/selection and before packet/apply identity;
3. ensure active restore barrier forces `selected_moves=[]` unless a valid approved clearance/plan lock explicitly authorizes execution;
4. keep apply fail-closed if selected moves are missing or identity/generation checks fail.

Final verdict: `IMPLEMENTATION_SAFE_WITH_MINOR_RISKS`.

Minor risks:

- two existing unit tests encode the legacy suppression contract and must be rewritten;
- if Step 1 is implemented without Step 2, selected executable moves can appear while restore barrier is active;
- API parser changes must preserve `run_json_command` callers for dry-run, planner refresh, and guarded apply.

Canonical Knowledge Changes: `NONE`.

## Dependency Graph

| Area | Owner | Consumes | Produces | Mutates | Execution critical | Proposal only | Read model only |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Restore barrier status | `tools/v7-users-autoswitch::_restore_barrier_status` (`1296-1393`) | restore barrier file, clearance metadata, approved plan lock metadata | `restore_barrier` dict with `active`, `expired`, `failover_quarantine`, clearance fields | No | Yes | No | Yes |
| Current-not-eligible branch | `tools/v7-users-autoswitch::_decision_for_user` (`5254-5304`) | current candidate, service gates, restore barrier | per-user decision, reason, proposal target | No | Indirect | Yes | Yes |
| Proposal generation | `tools/v7-users-autoswitch::_decision_for_user` (`5254-5426`) | candidate list, current state, service/load/policy gates | `decisions[]` rows | No | Indirect | Yes | Yes |
| Selected moves | `tools/v7-users-autoswitch::plan` + `_select_moves` (`4042-4058`, `6073-6093`) | decisions, autoswitch policy | `selected_moves` | No, until apply | Yes | No | Yes |
| Selected move budget | `_select_moves`, `_authority_budget_gate`, request cap (`4059-4065`, `3142-3205`) | selected moves, policy, authority budget, CLI cap | capped selected moves, budget diagnostics | No | Yes | No | Yes |
| Blast radius | `plan` dynamic blast radius (`4067-4085`, `4210-4224`) | affected moves, selected moves, authority budget | `safety.dynamic_blast_radius` | No | Yes | No | Yes |
| Approved plan lock | `_approved_plan_lock_validation` (`4296-4378`) | restore barrier lock, selected moves, users/current source/targets | validation result, selected moves from approved lock | No | Yes | No | Yes |
| Restore generation/hash | `_restore_clearance_generation_check` (`4961-5125`) | selected hash/count, generation, envelope IDs, source hashes | clearance OK/blocked reason | No | Yes | No | Yes |
| Selected move hash | `_selected_moves_hash` (`4731-4741`) | selected moves | deterministic hash | No | Yes | No | Yes |
| Operation ID | `_operation_context` (`4275-4287`) | selected hash/count, generation | `operation_id` | No | Yes | No | Yes |
| Execution envelope | `_atomic_execution_envelope` (`4501-4558`) | selected hash/count, source/snapshot hashes | envelope ID/hash/state | No | Yes | No | Yes |
| Execution envelope validation | `_validate_atomic_execution_envelope` (`4560+`) | plan operation/envelope, current source hashes | apply validation OK/STOP reason | No | Yes | No | No |
| Apply | `apply` (`6177-6252`) | plan, selected moves, mode, apply flag, envelope validation | route mutation only when `--apply` and selected moves valid | Yes, only with `--apply` | Yes | No | No |
| Verification / rollback | `apply`, `_rollback_verdict`, rollback packet methods (`6238-6249`, `6315-6328`, `4743-4818`) | apply result, route verification, rollback target | verification result, rollback result, rollback packet | Yes, only after apply/rollback | Yes | No | No |
| Terminal audit | `finalize_operation`, `_terminal_verdict`, `_terminal_audit_reference` (`6254-6368`) | apply result, rollback verdict, restore status | terminal state/reason/audit reference | Audit only when apply | Yes | No | Yes |
| Autoswitch plan API | `admin/v7-admin-api::autoswitch_plan_state` (`15995-16005`) | CLI stdout via `run_json_command` | API plan/output/cmd | No | No | Yes | Yes |
| JSON command runner | `admin/v7-admin-api::run_json_command` (`15953-15979`) | command stdout/stderr | parsed `json`, redacted `output` | No | Used by guarded apply wrapper | No | Yes |
| Channel drawer | `admin/v7-admin-api` UI (`29578-29606`) | `/api/autoswitch-plan?egress=` | target-channel recommendation table | No | No | Yes | Yes |
| Global autoswitch UI | `admin/v7-admin-api` UI (`35984-36029`) | `/api/autoswitch-plan`, dry-run/apply actions | global plan table, guarded action buttons | Apply button calls action endpoint | Yes for apply button | Yes | Yes |

## Downstream Impact

Assumed Patch A: failover proposal remains visible while restore barrier blocks execution.

| Consumer | Impact | Classification | Reason |
| --- | --- | --- | --- |
| Per-user decisions | `action=switch`, `move_type=failover`, `recommended_egress=<target>` may appear where legacy behavior returned keep | `REQUIRES CHANGE` | This is intended product correction. |
| `summary.candidate_moves_total` | increases for visible blocked proposals | `REQUIRES TEST` | This changes read-model meaning from executable-only to proposal-visible unless selected is separately blocked. |
| `selected_moves` | must remain `0` while restore barrier is active without clearance | `REQUIRES CHANGE` | Existing code would otherwise select visible failover proposals. |
| `operation.selected_move_count` | must remain `0` under active restore barrier without valid clearance | `REQUIRES TEST` | Operation identity must represent executable selected moves, not visible proposals. |
| `selected_move_hash` | should hash executable selected moves only | `SAFE` if selected remains `[]` | Proposal-only visibility must not change execution identity. |
| Authority budget | continues to cap selected moves | `SAFE` | `_authority_budget_gate` already caps after selection, but restore barrier must still zero execution selection when active. |
| Blast radius | should distinguish proposal count from executable selected count | `REQUIRES TEST` | Existing `effective_blast_radius` uses selected/affected counts; ensure execution radius remains 0 when blocked. |
| Approved plan lock | should remain unchanged | `SAFE` | Valid lock can still override selected moves for approved execution; invalid lock blocks apply. |
| Execution envelope | should remain unchanged for blocked proposals | `SAFE` if selected is zeroed | Envelope over zero selected moves is non-executable. |
| Execution packet / approval packet | no automatic packet creation from advisory proposals | `SAFE` | Existing packet owners remain separate from planner read model. |
| Apply | must remain blocked without selected moves or valid approved lock | `REQUIRES TEST` | `apply` blocks `no_selected_moves` / lock failures. |
| Verification / rollback | no impact before apply | `SAFE` | They run only after mutation. |
| Runtime eligibility | visibility can feed advisory rows; execution still STOP_SAFE | `SAFE` | Runtime Model already separates advisory preview from execution. |
| Operator UI | should show evacuation proposal plus execution blocker | `REQUIRES CHANGE` | Current channel drawer asks target-egress question, not source evacuation. |
| API `plan=null` | separate parser/materialization fix needed | `REQUIRES CHANGE` | Plan visibility is useless if API cannot parse full output. |
| Tests | legacy suppression tests must be rewritten; new safety tests required | `REQUIRES CHANGE` | Current tests assert `restore_barrier_failover_suppressed`. |

No downstream consumer is classified as `BROKEN` if Patch A includes an execution-only restore-barrier gate.

If Patch A only removes the suppression branch, execution safety is `NOT SAFE`.

## Execution Safety

### Can execution happen accidentally?

Yes, if the patch only makes `action=switch` visible and does not add a selected-move execution gate.

Proof:

- `plan()` calls `_select_moves(selection_source)` at `tools/v7-users-autoswitch:4057`.
- `_select_moves()` selects decisions where `action=="switch"` and `move_type=="failover"` at `6073-6089`.
- `apply()` mutates for every `plan["selected_moves"]` at `6220-6225` if `--apply`, mode, policy, and envelope validation pass.
- There is no direct `restore_barrier.active` rejection in `apply()` before mutation.

Therefore safe implementation must ensure active restore barrier converts visible proposal into **non-executable selected state** before apply.

### Can selected executable moves increase?

They can increase unless the restore-barrier execution gate is moved from proposal suppression into selected-move suppression.

Required invariant:

- `decisions[]` may show proposal.
- `selected_moves[]` must be empty when restore barrier is active and no valid clearance/approved plan lock exists.

### Can authority be bypassed?

No, if the gate is implemented before operation/envelope/apply:

- `_authority_budget_gate` caps selected moves at `3142-3205`.
- approved plan lock validation rejects mismatched count/users/source/targets at `4296-4378`.
- guarded apply is still explicit through `--apply` and API confirm path.

### Can restore barrier be bypassed?

It can be bypassed by a bad patch that leaves visible proposals in `selected_moves`. It is not bypassed if selected moves are zeroed by restore barrier active/post-TTL state unless clearance is valid.

### Can packet identity change?

No, if selected executable moves remain zero while blocked. Packet/operation/envelope identity should continue to be derived from selected executable moves, not from visible proposals:

- selected move hash: `4731-4741`
- operation ID: `4275-4287`
- atomic envelope: `4501-4558`

### Can rollback guarantees weaken?

No direct impact before apply. Rollback packet generation requires applied source operation and selected hash at `4743-4818`. If no apply happens, rollback is not required.

### Can execution packet become inconsistent?

No, if approved plan lock and envelope validation stay unchanged. Existing checks reject:

- source mismatch (`4358-4359`)
- target missing/disabled (`4360-4365`)
- replacement authority (`4366-4371`)
- generation/hash/count mismatch (`4961-5125`)
- atomic envelope mismatch (`4560+`)

## Execution Pipeline

| Stage | File/function/line | Inputs | Outputs | Restore barrier role |
| --- | --- | --- | --- | --- |
| Observation | service matrix / quality / state inputs read in planner init | service, route, load, registry files | current production evidence | none |
| Candidate generation | `tools/v7-users-autoswitch::_decision_for_user` (`5254-5262`) | user, current channel, candidate channels, services | candidate list/current candidate | should not suppress proposal |
| Proposal | `_decision_for_user` (`5278-5304`) | current eligibility, failover candidates | advisory decision row | should expose proposal and blocker |
| Selection | `plan` + `_select_moves` (`4057`, `6073-6093`) | decision rows | selected executable moves | must block/zero selected moves if active barrier lacks clearance |
| Authority budget | `_authority_budget_gate` (`3142-3205`) | selected moves, authority policy | capped selected moves | independent gate before barrier/apply |
| Restore barrier status | `_restore_barrier_status` (`1296-1393`) | restore barrier file | barrier state/clearance metadata | source of active/clearance state |
| Approved lock | `_approved_plan_lock_validation` (`4296-4378`) | barrier lock, current user/source/target | valid/invalid selected move lock | may authorize exact selected moves only if valid |
| Restore generation | `_restore_clearance_generation_check` (`4961-5125`) | selected hash/count/generation/envelope | clearance OK/fail | apply/readiness guard |
| Envelope | `_atomic_execution_envelope` (`4501-4558`) | selected hash/count/source hashes | envelope ID/hash/state | execution identity |
| Runtime eligibility | Runtime/A6 read model | gate outputs | advisory EXECUTE/STOP rows | consumes restore state |
| Execution eligibility | `apply` (`6177-6218`) | mode, apply flag, selected moves, envelope | fail-closed or proceed | must not proceed on barrier-blocked selected moves |
| Apply | `apply` (`6220-6252`) | selected moves | switch command result | mutation point |
| Verification | `apply` (`6238-6241`) | route state | verify result | after mutation |
| Rollback | `apply` (`6242-6249`) | failed verification, current target | rollback result | after failed verification |
| Terminal outcome | `finalize_operation` (`6254-6368`) | apply/rollback state | terminal state/audit | records restore status |

## Planner Invariants

| Invariant | Current owner | Would safe Patch A violate? | Explanation |
| --- | --- | --- | --- |
| Proposal is advisory until execution gates pass | Decision/Runtime Model; planner read model | `NO` | Patch aligns implementation with this invariant. |
| Selected moves are executable candidates, not all proposals | `tools/v7-users-autoswitch::plan` | `UNKNOWN` until patched | Must preserve by adding execution blocker before `selected_moves` finalization. |
| Selected move hash is deterministic over executable selected moves | `_selected_moves_hash` | `NO` if blocked selected remains `[]` | Hash must not include advisory proposals. |
| Operation ID derives from selected hash/count/generation | `_operation_context` | `NO` if selected remains `[]` when blocked | Operation identity remains stable. |
| Authority caps selected moves | `_authority_budget_gate` | `NO` | Existing cap remains. |
| Restore barrier blocks unapproved execution | restore barrier + plan/apply gates | `NO` only if selected is zeroed while active | This is required by patch. |
| Approved plan lock can override fresh planning only when valid | `_approved_plan_lock_validation` | `NO` | Must remain unchanged. |
| Apply requires explicit `--apply` | `apply` | `NO` | Patch does not affect CLI apply flag. |
| Guarded apply cannot run in observe mode | `apply` | `NO` | `mode=="observe"` still blocks apply. |
| Atomic envelope validates selected move identity/source state | `_atomic_execution_envelope`, `_validate_atomic_execution_envelope` | `NO` | Patch should not modify envelope logic. |
| Rollback packet only from applied source operation | rollback packet methods | `NO` | Proposal visibility does not create applied source operation. |
| API plan endpoint is read-only | `autoswitch_plan_state` | `NO` | Parser fix should not change command semantics. |

## Restore Barrier Semantic Verification

Restore barrier can safely become:

```text
proposal visible
execution blocked
```

without changing authority, rollback, packet identity, or execution semantics **if and only if**:

1. active/post-TTL restore barrier blocks `selected_moves`, not `decisions`;
2. valid approved plan lock / generation clearance remains the only way to restore executable selected moves;
3. `apply()` continues to fail closed on `selected_moves=[]`, invalid lock, envelope mismatch, source mismatch, target mismatch, or expired lock;
4. operation/envelope/selected hash remain based on executable selected moves only;
5. UI labels the proposal as blocked, not ready-to-apply.

The existing code already supports most of the downstream guards, but it lacks the explicit active-barrier selected-move gate because the legacy behavior suppressed proposals earlier.

## API Compatibility

### `run_json_command` Callers

| Caller | Lines | Purpose | Compatibility impact |
| --- | --- | --- | --- |
| `autoswitch_plan_state` | `15995-16005` | read-only plan API | Must receive parsed JSON even for large output. |
| `autoswitch_dry_run_state` | `16008-16012` | audited dry-run action | Must preserve `rc`, `cmd`, `output`, `plan`. |
| `autoswitch_planner_refresh_dry_run_state` | `16060-16076` | planner refresh dry-run | Must preserve parsed plan for summary. |
| `autoswitch_apply_guarded` | `16102-16113` | guarded apply wrapper | Must not hide parse failures for apply; should remain fail-closed if plan missing. |

### Response Contract

Current response contract:

- `action`
- `target_egress`
- `rc`
- `plan`
- `output`
- `cmd`

Safe parser patch must preserve these fields. Optional diagnostics can be added:

- `parse_error`
- `output_truncated`
- `json_parse_source`

### Maximum Response Size

Current runner captures up to `5_000_000` bytes for parse, but API only returns `output[-12000:]`. Production evidence showed returned `output` begins mid-JSON and `plan=null`. Safe patch must parse the complete captured stdout before display truncation and must not require UI to parse the `output` tail.

### Backward Compatibility

Safe if:

- `run_json_command` still returns `json=None` on invalid output;
- existing callers that use `result.get("json") or {}` continue to work;
- parse diagnostics are additive only.

## UI Compatibility

| UI area | Lines | Uses | Classification |
| --- | --- | --- | --- |
| Channel drawer autoswitch plan | `29578-29606` | `/api/autoswitch-plan?egress=<id>`, filters `recommended_egress === id` | Needs API/source semantics and wording |
| Channel drawer apply | `29608-29629` | posts guarded apply with `egress:id` | Needs wording; execution must remain guarded |
| Assignment plan/status | `27856-28008` | `current_egress`, `recommended_egress`, selected from/to blockers | Minor wording/no runtime change |
| Global autoswitch plan | `35984-36029` | full plan decisions and selected moves | Minor wording; should show blocked proposal correctly |
| Operator KPIs | `30479-30525`, `31306-31307` | selected move counts/barrier status | No change if selected moves remain executable-only |

Current target-egress behavior is compatible for "moves TO channel" but insufficient for "evacuate FROM channel". Source evacuation needs a read-only API/UI extension, not a runtime path.

## Regression Matrix

Required tests before deploy:

| Test | Expected |
| --- | --- |
| restore barrier active + current channel FAIL + safe target exists | decision proposal visible; `selected_moves=0`; terminal reason restore barrier active/blocker |
| restore barrier inactive + current channel FAIL + safe target exists | proposal visible; selected bounded by policy/authority |
| restore barrier active + safe target absent | no selected moves; no eligible target reason preserved |
| restore barrier active + authority disabled/FROZEN | proposal may be visible; selected moves remain 0; authority blocker visible |
| restore barrier inactive + authority enabled | selected moves follow authority budget |
| active restore barrier + `--apply` | no mutation; fail closed with explicit restore-barrier/selected-moves blocker |
| valid approved plan lock + active barrier + matching selected identity | existing approved execution path remains valid |
| invalid approved plan lock | fail closed; no mutation |
| selected move hash unchanged for zero selected moves | deterministic hash over executable selected moves |
| selected move hash changes only when executable selected move changes | proposal-only data does not affect execution hash |
| atomic envelope no-selected path | valid no-execution envelope state |
| atomic envelope selected path | unchanged for approved selected moves |
| API large valid JSON stdout | `plan` parsed; `output` may be tail; parse diagnostics absent/OK |
| API invalid/mixed stdout | `plan=null`; parse diagnostics visible; no exception to UI |
| channel drawer target recommendation | target-egress still shows moves TO channel |
| channel drawer source evacuation | source/current-egress query shows users FROM channel |
| global autoswitch plan | blocked proposals visible; selected counts remain executable-only |
| dry-run endpoint | same response contract with parsed plan |
| guarded apply endpoint | fails closed when plan missing/invalid |

Existing tests requiring update:

- `tests/unit/test_v7_users_autoswitch_policy.py:1111-1133`
- `tests/unit/test_v7_users_autoswitch_policy.py:1476-1492`

Existing tests to preserve:

- approved plan lock / material state tests around `1897+`, `2036+`, `2209+`, `2301+`, `2375+`, `2524+`, `2906+`, `2947+`, `2990+`
- API command reuse test `tests/unit/test_api3_read_only_views.py:138-154`

## Implementation Order

### Step 1 - Restore Barrier Execution Gate

Owner: `tools/v7-users-autoswitch`

Change:

- keep failover decisions visible in `_decision_for_user`;
- after `_select_moves` and authority cap, before selected hash/operation/envelope finalization, if restore barrier is active/post-TTL and no valid clearance/approved plan lock exists, set executable `selected=[]`;
- preserve diagnostics with `selected_moves_before_restore_barrier` and explicit blocker reason.

Independently deployable: yes.

Rollbackable: yes, revert the planner change.

Safety requirement:

- no apply can occur from visible proposal while barrier blocks execution.

### Step 2 - Tests For Proposal Visible / Execution Blocked

Owner: `tests/unit/test_v7_users_autoswitch_policy.py`

Change:

- rewrite legacy suppression tests;
- add apply-fail-closed test under active barrier;
- preserve approved plan lock tests.

Independently deployable: with Step 1.

Rollbackable: yes.

### Step 3 - API Plan Materialization

Owner: `admin/v7-admin-api`

Change:

- parse full captured stdout before response truncation;
- add additive parse diagnostics;
- preserve response fields and caller compatibility.

Independently deployable: yes.

Rollbackable: yes.

### Step 4 - Source Evacuation Query / UI Wording

Owner: `tools/v7-users-autoswitch` and `admin/v7-admin-api`

Change:

- add read-only source/current-egress query semantics;
- keep target-egress semantics unchanged;
- channel drawer displays evacuation FROM channel separately from recommendation TO channel.

Independently deployable: yes after Step 3.

Rollbackable: yes.

## Remaining Risks

1. Semantic risk: `candidate_moves_total` may change from executable-only signal to proposal-visible signal unless selected/executable counts remain separate.
2. UI risk: operator may misread a visible proposal as ready-to-apply unless blocker wording is clear.
3. API risk: parser changes affect guarded apply wrapper if malformed stdout occurs; this must remain fail-closed.
4. Test risk: existing tests assert old behavior and need deliberate contract update.

No authority, architecture, runtime path, rollback model, or packet model risk remains if implementation order is followed.

## Production Safety

Production mutation remains impossible without:

- explicit `--apply`;
- non-observe mode;
- non-empty executable `selected_moves`;
- valid authority budget;
- valid restore barrier clearance or approved plan lock when barrier is active;
- valid atomic execution envelope;
- successful switch command;
- verification/rollback handling after mutation.

Patch A is safe only when restore barrier moves from proposal suppression to selected-move/apply suppression.

## Final Certification

1. Is root cause investigation complete?

Yes.

2. Is any important uncertainty still remaining?

No architecture uncertainty remains. Implementation must still prove selected-move blocking tests.

3. Can implementation begin safely?

Yes, with the implementation order above.

4. Is another audit still required?

No.

5. What production risks remain?

Main risk is accidental selected-move exposure if proposal visibility is patched without execution gating.

6. What is the smallest safe first patch?

In `tools/v7-users-autoswitch`, make current-ineligible failover proposal visible while adding an execution-only restore-barrier gate that zeroes `selected_moves` and reports an explicit blocker when barrier is active without valid clearance.

Final verdict: `IMPLEMENTATION_SAFE_WITH_MINOR_RISKS`.

