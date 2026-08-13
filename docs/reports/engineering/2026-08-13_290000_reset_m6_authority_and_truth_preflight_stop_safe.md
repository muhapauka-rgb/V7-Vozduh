# RESET-M6 Authority and Truth Preflight Engineering Report

Status: `RESET_M6_STOP_SAFE_OWNER_ISSUED_CORE_CUTOVER_AUTHORITY_REQUIRED_SOURCE_CPS_TRUTH_REPAIRED`

What changed: no M6 Runtime adapter, deploy, writer transfer or production action was performed. The existing policy/Authority and truth owners were queried before any effectful work.

Evidence:

- no owner-issued policy/Authority contract exists for a Routing Core certification-user action class or Core writer transfer;
- `tools/v7-truth-check --all --json` returns `NO-GO` and `CPS_LIVE_STATE_CONTRADICTION_STOP_SAFE`;
- relevant blockers include `cps_authority_required_not_policy_bounded`, `delegated_policy_live_operational_authority_required`, `cps_normalized_field_divergence:ACTIVE_PROGRAM`, `cps_normalized_field_divergence:CURRENT_EXECUTION_FRONTIER`, dependency-frontier divergence and invalid Program frontier terminal/continuation projections;
- existing bounded delegated Service Failure/CT-M0F contracts do not authorize a new Core action class or writer ownership transfer.

Exact residual: the existing Authority owner must issue or reject a scope-specific contract for one designated certification user, exact source/target, Core decision fingerprint, current policy/Authority generations, one operation/lease/fencing token, legacy writer exclusion, rollback/fallback restoration and hard expiry. Before consumption, CPS/OMP normalization must converge so the active Reset frontier is not rewritten to historical Service Failure/Polygon state. A deploy package must then be explicitly scoped through the existing safe-deploy owner.

Re-entry condition: owner-issued Core certification contract exists, truth-check no longer reports active Program/frontier/Authority contradiction for that contract, and the exact source package/deploy scope is approved. Then M6 may implement/deploy the smallest adapter and run one controlled certification transaction.

## Targeted source truth repair

The existing CPS normalizer/validator was extended, not replaced:

- Reset is now an admitted reconstructable live Program, so atomic CPS rendering preserves its active Program, phase, generation and exact frontier instead of reverting to historical Polygon defaults.
- Reset phase frontiers are independent of the historical capability deterministic-sequence row; capability WIP remains preserved but cannot overwrite the Reset successor.
- RESET-M6 is represented as an explicit `ENGINEERING_AUTHORITY` boundary with external owner input required.
- legacy AEP functional-footprint projections are scoped out while Reset is active; the Reset phase contract owns completion.
- OMP current pointer now reflects the same M6 Authority stop.

Focused evidence: 10/10 Reset-normalizer/Core tests PASS. `tools/v7-truth-check --all --json` no longer reports CPS/OMP active Program, stage, frontier, continuation, terminal or Authority projection contradictions. Blockers reduced from 97 before repair to five infrastructure/worktree items: dirty/Runtime-relevant uncommitted source and unavailable/unreadable canonical remote/branch. This is source consistency evidence only, not deploy or production convergence.

Why this stop is mandatory: `NEW_CORE_EARNS_AUTHORITY_THROUGH_EVIDENCE`; reusing prior Service Failure Authority would be silent Authority expansion and could permit two writers.

Owner: existing `admin_core/operator_execution.py` Authority owner, CPS/OMP truth consumers and safe-deploy owner. No new owner is requested.

Current successor remains `EXECUTE_RESET_M6_CONTROLLED_MIGRATION_SINGLE_WRITER_FENCED_CUTOVER`; RESET-M6 is not complete and RESET-M7 is not admitted. Remaining independent external boundary: owner-issued Core certification action-class and writer-transfer Authority, followed by explicitly scoped safe publication/deploy.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
- User movement = `0`.
