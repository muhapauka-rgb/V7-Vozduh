# BLOCK E17 - Read-Only Operator Timeline And Approval Evidence Archive Report

## Executive Verdict

E17 implemented a read-only operation timeline and lineage archive in the
existing V7 embedded admin Operator section. The operator can now inspect what
happened, why, what moved, rollback status, delayed movement, generation
governance, restore state, runtime verdict, and linked evidence without opening
raw evidence folders manually.

No runtime mutation, runtime deploy, runtime control action, user movement,
routing mutation, kill-switch mutation, manual autoswitch apply, canary, cohort
execution, shell execution, DB migration, or mutating execution UX was
performed.

## Final Answers

operation_timeline_implemented=true
lineage_archive_implemented=true
delayed_movement_lineage_visible=true
rollback_lineage_visible=true
evidence_archive_implemented=true
stale_warning_system_implemented=true
read_only_api_extended=true
mutating_actions_present=false
tests_passed=true
remaining_ui_blockers=NO_PERSISTED_OPERATOR_AUDIT_DB;NO_LIVE_MULTI_OPERATOR_APPROVALS;RAW_EVIDENCE_FULLTEXT_SEARCH_NOT_IMPLEMENTED;MUTATING_EXECUTION_UX_STILL_FORBIDDEN
recommended_next_block=E18_OPERATOR_AUDIT_SEARCH_AND_READONLY_EVIDENCE_DETAIL_HARDENING
execution_allowed_now=false

## Implemented Scope

Lineage adapter:

- `OperationSummary`;
- `OperationTimelineEntry`;
- `MovementEvent`;
- `RollbackEvent`;
- `RestoreLifecycleEvent`;
- `DelayedMovementEvent`;
- `GenerationGovernanceEvent`;
- `EvidenceReference`;
- `BlastRadiusSummary`;
- `RuntimeVerdict`.

Read-only API:

- `GET /api/operator/timeline`;
- `GET /api/operator/lineage`;
- `GET /api/operator/runtime-verdicts`;
- `GET /api/operator/operation-detail?id=...`;
- `GET /api/operator/evidence-detail?id=...`.

UI:

- Operation Timeline panel in the `Оператор` tab;
- search input;
- type and state filters;
- timeline cards with movement, rollback, delayed movement, generation, and
  freshness labels;
- operation detail drawer with grouped runtime verdict, movement/rollback,
  restore/delayed/generation, and evidence references.

## Safety Boundary

E17 did not add:

- `POST /api/operator/*`;
- `/api/actions/operator*`;
- shell execution;
- runtime writes;
- user switch controls;
- autoswitch apply controls;
- service restart controls;
- kill switch controls;
- routing mutation controls.

The operation detail endpoint returns redacted report excerpts and evidence
metadata. Raw evidence content is not rendered by default.

## Tests And Checks

Passed:

- `python3 -m py_compile admin/v7-admin-api admin_core/operator_observability.py tests/unit/test_operator_observability.py`
- `python3 -m unittest tests.unit.test_operator_observability`
- `python3 -m unittest tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test`
- `python3 -m unittest discover tests` (`104` tests)
- `tools/v7-admin-endpoint-inventory`
- static `/admin-v2` render smoke
- touched-file credential scan
- `git diff --check`

Unavailable / not applicable:

- frontend build: current admin is embedded in `admin/v7-admin-api`, not an
  active React/package build.
- frontend lint/typecheck: unavailable for current embedded admin structure.
- live route render against server: not started because E17 did not deploy or
  mutate runtime.

## Productization Verdict

operation_lineage_archive_ready=true

The Operator section now has a coherent read-only lineage layer connecting
reports, evidence references, lifecycle summaries, rollback, delayed movement,
generation governance, and runtime verdicts.

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
