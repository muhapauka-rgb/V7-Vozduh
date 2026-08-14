# Final Repository-Wide Consumer Audit Before Restore-Barrier Patch

Status: READ_ONLY_AUDIT_COMPLETE  
Date: 2026-06-30  
Scope: Restore-barrier proposal visibility patch, Patch A readiness  
Runtime mutation: NO  
User movement: NO  
Automation enabled: NO  
Authority expanded: NO  

## Summary

The repository-wide consumer audit found no hidden execution path that moves users from proposal-only fields such as `decisions[].action`, `move_type`, `recommended_egress`, `candidate_moves_total`, or `affected_users`.

The single material safety issue remains inside the existing autoswitch planner owner itself: `tools/v7-users-autoswitch::_select_moves()` currently turns any visible `action == "switch"` decision into executable `selected_moves`. Therefore Patch A is safe only if it first adds an execution-only restore-barrier gate that keeps proposal decisions visible while forcing:

- `selected_moves = []`
- `selected_move_count = 0`
- explicit execution blocker
- apply fail-closed

With that selected-move gate in place, implementation can begin.

Final verdict: IMPLEMENTATION_GO_WITH_MINOR_UI_API_CHANGES.

## Repository-Wide XREF

Complete raw xref artifacts were generated under the paths below. The two
large repository-wide TSV indexes were retired from Git on 2026-08-14 after
consumer/reproducibility review because they are stale point-in-time generated
search output, have no executable consumer, and their decision-relevant result
is preserved by this report plus the retained scoped/summary projections.
Their retirement metadata is recorded in
`docs/reports/engineering/2026-08-14_100000_v7_repository_cleanup_batch1_cps_reconciliation_and_generated_xref_retirement.md`.

- retired: `docs/reports/engineering/final_consumer_audit_2026-06-30/xref.tsv`
- retired: `docs/reports/engineering/final_consumer_audit_2026-06-30/xref_important.tsv`
- `docs/reports/engineering/final_consumer_audit_2026-06-30/xref_scoped_code.tsv`
- `docs/reports/engineering/final_consumer_audit_2026-06-30/xref_summary.json`

The broad scan includes historical reports and evidence files, so the executable-risk review used the scoped code scan for `tools/`, `admin/`, `admin_core/`, `tests/`, and `systemd/`.

Scoped code xref summary:

| Consumer class | Hits |
|---|---:|
| test | 868 |
| admin_core_read_model_or_pipeline | 619 |
| admin_read_model_or_operator_api | 373 |
| tooling_or_runtime_support | 346 |
| planner_execution_identity_path | 309 |
| planner_read_model_or_policy | 213 |
| operator_ui | 168 |
| rollback_or_main_path | 37 |
| apply_path | 19 |
| api_or_apply_wrapper | 6 |

Highest-signal files:

| File | Hits | Role |
|---|---:|---|
| `tools/v7-users-autoswitch` | 578 | planner, selected-move generation, apply, restore barrier, terminal verdict |
| `admin/v7-admin-api` | 547 | API, operator UI, read models |
| `tests/unit/test_v7_users_autoswitch_policy.py` | 500 | planner/apply/restore-barrier contracts |
| `admin_core/operator_execution.py` | 222 | packet/execution identity |
| `tools/v7-control-plane-governance-check` | 193 | governance/read-only checks |
| `tests/unit/test_operator_execution_packet.py` | 132 | packet/lease/identity tests |
| `admin_core/operator_execution_pipeline.py` | 99 | execution pipeline identity |
| `admin_core/operator_observability.py` | 85 | observability/read model |
| `admin_core/autonomy_trust_acceleration.py` | 71 | trust/autonomy read model |
| `tools/v7-governed-canary-dry-run-cycle` | 42 | governed cycle orchestration |
| `tools/v7-restore-settle-gate` | 21 | restore-barrier support |

Representative xref table:

| Symbol | File | Line / area | Consumer type | Current meaning | Patch A impact | Risk |
|---|---|---:|---|---|---|---|
| `decisions[]` | `tools/v7-users-autoswitch` | plan construction around 4044 | planner read model | per-user planner decision | may expose proposal while barrier active | LOW if selected gate exists |
| `action == "switch"` | `tools/v7-users-autoswitch` | `_select_moves` around 6073 | executable selection | converts switch decisions into selected moves | must not consume restore-barrier proposals as executable | HIGH unless gated |
| `selected_moves` | `tools/v7-users-autoswitch` | plan/apply around 4057, 6177 | execution authority | actual executable movement set | must remain execution-only | LOW if zeroed under barrier |
| `selected_move_hash` | `tools/v7-users-autoswitch` | around 4130, 4731 | execution identity | selected move identity hash | unchanged | LOW |
| `operation_id` | `tools/v7-users-autoswitch` | around 4179 | execution identity | operation lineage | unchanged | LOW |
| `approved_plan_lock` | `tools/v7-users-autoswitch` | around 4097, 4296 | approval/lease identity | locked approved selected moves | unchanged | LOW |
| `apply()` | `tools/v7-users-autoswitch` | around 6177 | apply path | mutates only `plan["selected_moves"]` under `--apply` | remains fail-closed if selected empty | LOW after gate |
| `candidate_moves_total` | `tools/v7-users-autoswitch` | around 4257 | metric/read model | currently counts recommended non-current decisions | should be treated as proposal/opportunity count, not executable count | MEDIUM wording risk |
| `recommended_egress` | `admin/v7-admin-api` | around 29582, 35994 | UI/read model | recommended target display | proposal visible after Patch A | LOW with wording |
| `selected_moves` | `admin/v7-admin-api` | around 13371, 16032, 29622 | API/UI/apply wrapper | executable selected move count/list | unchanged | LOW |
| `candidate_moves_total` | `admin/v7-admin-api` | around 16036, 29596, 30594 | dashboard/KPI | planner opportunity count | label must not imply executable movement | MEDIUM wording risk |
| `current_egress_not_eligible` | `tests/unit/test_v7_users_autoswitch_policy.py` | around 885 | failover behavior test | current channel ineligible reason | preserve proposal behavior | LOW |
| `restore_barrier_failover_suppressed` | `tests/unit/test_v7_users_autoswitch_policy.py` | around 1111, 1476 | legacy test contract | proposal suppressed under barrier | rewrite to proposal visible + selected blocked | EXPECTED CHANGE |

## Hidden Execution Authority Check

No hidden execution path was found that moves users using only:

- `decision.action == "switch"`
- `move_type == "failover"`
- `recommended_egress`
- `candidate_moves_total`
- `affected_users`

The actual mutation path is:

`tools/v7-users-autoswitch.apply()` → iterate `plan["selected_moves"]` → `_run_switch(...)`.

`apply()` already fails closed when `selected_moves` is empty. However, `apply()` does not directly evaluate an active restore barrier. Therefore the restore-barrier protection must happen before apply by making the selected-move set execution-blocked.

Required invariant:

Proposal-visible restore barrier state MUST NOT produce executable `selected_moves` unless valid clearance / approved plan lock semantics explicitly allow it.

Execution authority remains tied to:

- explicit `--apply`
- executable `selected_moves`
- selected move identity/hash
- operation identity
- authority budget
- approved plan lock / restore-barrier clearance where required
- atomic execution envelope
- verification / rollback path

Hidden execution authority blocker: NO.

## UI / Dashboard Semantic Check

The UI reads both proposal and execution fields. No direct UI mutation path was found, but labels must distinguish proposal from executable selection.

| Component | Current data source | Semantic risk after Patch A | Required change |
|---|---|---|---|
| Channel autoswitch drawer | `/api/autoswitch-plan?egress=<id>`; filters `decisions[].recommended_egress === id` | It currently means "move TO this target", not "evacuate FROM this source" | Add/clarify source evacuation query before using it as evacuation UI |
| Channel autoswitch drawer selected count | `plan.selected_moves` filtered by target | Safe if selected remains execution-only | NONE beyond wording |
| Global autoswitch plan | `plan.decisions`, `plan.summary.selected_moves` | Proposal rows could look executable | Label proposal vs executable clearly |
| Operator KPI "К переносу" | selected moves adapter | Safe because it uses selected moves | NONE |
| Planner candidate KPI | `candidate_moves_total` | Can be misread as selected/apply-ready | Rename or label as proposal/opportunity count |
| Assignment blockers | decisions + selected moves | Read-only; already distinguishes blockers | Minor wording only |

UI risk: MINOR_UI_WORDING_RISK.

## Blast Radius / Metrics Check

Proposal count and executable selected count must remain separate.

Safe unchanged as execution-only:

- `selected_moves`
- `selected_move_count`
- `selected_move_hash`
- `operation_id`
- dynamic/effective execution blast radius derived from selected moves
- apply result
- rollback manifest lineage

Fields that need semantic clarification:

- `candidate_moves_total`
- `candidate_moves`
- UI labels like "Кандидатов"

Recommended additive fields:

- `proposal_moves_total`
- `executable_selected_moves`
- `execution_blocked`
- `execution_blocker`
- `execution_blocker_source`

`candidate_moves_total` must not be used as production maturity, execution evidence, blast-radius consumption, or A4 production outcome. It is a proposal/opportunity/read-model signal only unless canonical owners explicitly declare otherwise.

Metric verdict: METRIC_SEMANTIC_SPLIT_REQUIRED.

## API Contract Check

Relevant endpoints and wrappers:

| Endpoint / caller | Source | Response fields | Patch A impact | Backward compatibility |
|---|---|---|---|---|
| `/api/autoswitch-plan` | `autoswitch_plan_state()` | raw plan, decisions, selected_moves, summary, safety | proposals may become visible while selected stays zero | additive fields enough |
| `/api/actions/autoswitch-dry-run` | `autoswitch_dry_run_state()` | dry-run plan | same as above | additive fields enough |
| `/api/actions/autoswitch-apply-guarded` | `autoswitch_apply_guarded()` | guarded apply output | must still depend on selected moves | safe if selected zero under barrier |
| planner refresh view | `_planner_refresh_summary()` | `candidate_moves_total`, `selected_moves_before_gate`, `selected_moves_after_gate` | must show before/after execution gate clearly | additive fields enough |
| channel drawer preview | `previewV2ChannelAutoswitch()` | plan decisions/selected | target-vs-source ambiguity | needs wording/query fix |

API parse risk already observed in prior live trace: production-sized pretty JSON can cause `/api/autoswitch-plan` to return `plan=null` due stdout handling/truncation/mixed output. That is not an execution safety blocker, but it should be fixed before relying on the UI for proposal visibility.

API verdict: API_CONTRACT_ADDITIVE_FIELDS_REQUIRED.

## Test Contract Check

Tests to rewrite:

- `tests/unit/test_v7_users_autoswitch_policy.py` restore-barrier active failover suppression cases around the legacy `restore_barrier_failover_suppressed` assertions.
- Expected new behavior: decision/proposal visible, `candidate_moves_total` or proposal count visible, `selected_moves == 0`, explicit restore-barrier execution blocker.

Tests to preserve:

- Non-barrier hard failover creates selected move.
- `--apply` with empty selected moves fails closed.
- Authority budget gate drops selected moves.
- Approved plan lock identity preservation.
- Approved plan lock missing selected moves returns explicit unsafe blocker.
- Restore-barrier clearance hash/count/generation mismatch blocks selected moves.
- Expired restore-barrier clearance budget behavior.
- Rollback, verification, atomic envelope, historical packet compatibility.

Tests to add before production deploy:

1. Active restore barrier + failed current + safe target:
   - `decisions[].action == "switch"`
   - `move_type == "failover"`
   - `recommended_egress` populated
   - `reason` includes `current_egress_not_eligible`
   - `selected_moves == []`
   - selected count/hash represent no executable move
   - explicit execution blocker visible

2. Active restore barrier + `--apply`:
   - no `_run_switch`
   - no user movement
   - fail-closed result

3. Restore barrier inactive:
   - existing failover selected-move behavior unchanged

4. Valid clearance / approved lock:
   - existing permitted selected-move behavior unchanged

5. API plan parser:
   - valid large JSON is parsed
   - mixed/invalid output returns diagnostics without corrupting plan semantics

6. Channel drawer semantics:
   - target recommendation is not displayed as source evacuation
   - source evacuation query or label is explicit

7. Metrics:
   - proposal count and executable selected count remain distinct

## Performance / Size Check

Visible proposals can increase useful UI rows but should not materially increase planner compute cost at current production scale because decisions are already computed per user.

Current live-trace scale was small enough for Patch A:

- affected failed-channel users: approximately 14 in the latest trace family
- egress count: small single-digit production pool
- decisions already present in planner output

Risks at product scale:

- Full raw plan JSON can grow with users and candidate lists.
- UI must not render all raw history or all candidates by default.
- API should support compact summaries, pagination, or drill-down for 10,000+ users / 100+ channels.
- Existing production trace already showed API parsing/response handling fragility for large command output.

Performance verdict:

- Current scale: safe with minor API parser/UI wording work.
- Product scale: compact mode / summaries / pagination should be handled by existing Product Scale and Work Placement rules before broad deployment.
- No performance blocker for Patch A itself.

## Blocker Classification

| Classification | Result | Reason |
|---|---|---|
| NO_HIDDEN_CONSUMER_RISK | YES | No hidden mover consumes proposal-only fields as authority |
| MINOR_UI_WORDING_RISK | YES | Proposal vs executable labels need clarification |
| METRIC_SEMANTIC_SPLIT_REQUIRED | YES | Proposal count must not equal selected/executable count |
| API_CONTRACT_ADDITIVE_FIELDS_REQUIRED | YES | Additive fields needed for explicit blocked/executable semantics |
| EXECUTION_AUTHORITY_BLOCKER | NO, if selected-move gate is implemented first | The only high-risk path is `_select_moves`; it is controlled by the planned gate |
| PERFORMANCE_BLOCKER | NO | Current scale safe; product-scale compacting remains separate optimization |
| INSUFFICIENT_EVIDENCE | NO | Prior audits and xref are sufficient to begin implementation |

## Implementation GO / NO-GO

Patch A implementation can begin only under these conditions:

1. Add the execution-only restore-barrier selected-move gate first.
2. Keep proposal visibility separate from executable selected moves.
3. Keep apply fail-closed.
4. Add tests before production deploy.
5. Update UI/API wording additively.

Files that can be changed first:

1. `tools/v7-users-autoswitch`
2. `tests/unit/test_v7_users_autoswitch_policy.py`
3. `admin/v7-admin-api`
4. `tests/unit/test_api3_read_only_views.py`

Fields that must remain execution-only:

- `selected_moves`
- `selected_move_count`
- `selected_move_hash`
- `operation_id`
- `atomic_execution_envelope`
- `approved_plan_lock`
- `packet_id`
- `apply_result.applied`
- runtime mutation/apply

Fields that may become proposal-visible:

- `decisions[].action`
- `decisions[].move_type`
- `decisions[].recommended_egress`
- `decisions[].reason`
- `candidate_moves_total` only if documented/labeled as proposal/opportunity count
- additive `proposal_moves_total`
- additive `execution_blocked`
- additive `execution_blocker`

## Required Tests

Required before production deploy:

- restore barrier proposal visible + selected zero
- restore barrier active + apply fail-closed
- inactive barrier preserves selected failover
- valid clearance preserves selected behavior
- approved plan lock compatibility
- selected-move hash/count unchanged for executable paths
- API parses large valid autoswitch JSON
- API exposes additive execution-blocked fields
- UI labels proposal vs selected clearly
- source evacuation and target recommendation are not conflated

## Required UI/API Wording

Required wording distinctions:

- "Proposal" / "Рекомендация" for visible `decisions[]`
- "Executable selected move" / "Выбрано к исполнению" for `selected_moves`
- "Blocked by restore barrier" / "Исполнение заблокировано restore barrier"
- "Move TO target channel" vs "Evacuate FROM source channel"
- "Candidate/proposal count" vs "selected/executable count"

## Canonical Knowledge Changes or NONE

NONE.

Existing canonical knowledge is sufficient:

- proposal visibility and execution authority must be separate;
- runtime/apply authority remains selected-move based;
- restore barrier may block execution without hiding planner explanation;
- product-scale UI/API surfaces need compact summaries and clear read-model semantics.

No new owner, new backlog item, runtime path, architecture, or canonical document is required.

## Final Verdict

IMPLEMENTATION_GO_WITH_MINOR_UI_API_CHANGES.

Patch A is approved for implementation planning, not runtime deployment, provided the first implementation step is the execution-only selected-move gate under active restore barrier.
