# Program Z2 Hybrid Approval And Autonomy Certification Report

Date: 2026-06-01

## 1. Reality Audit

Created `PROGRAM_Z2_REALITY_AUDIT.md`.

Latest repository runtime evidence was collected from `docs/track7/productization/e30-evidence`. Z2 also created a local certification fixture in `docs/track7/productization/z2-evidence`.

Live `/opt/v7/egress/state` is unavailable in this workspace, so live user movement was not attempted.

## 2. Conflict Audit

Created `PROGRAM_Z2_IMPLEMENTATION_CONFLICT_AUDIT.md`.

Z2 reused existing systems:

- `v7-users-autoswitch` as planner/apply authority
- `v7-autoswitch-proposal-cap` as proposal source
- `v7-autoswitch-safety-review` as safety review
- existing `v7-user-switch` movement authority
- existing zero-movement operator audit pattern

No duplicate movement engine was created.

## 3. Truth Source Audit

Created `PROGRAM_Z2_TRUTH_SOURCE_AUDIT.md`.

Runtime truth wins over approval truth. Approval can authorize policy scope, but runtime recheck denies on drift.

## 4. Runtime Audit

Created `PROGRAM_Z2_RUNTIME_AUDIT.md`.

Z2 fixture recheck returned:

- `ALLOW_HYBRID_BOUNDED_AUTONOMY`
- budget `1`
- selected move count `0`
- safety status `ok`

## 5. Hybrid Approval

Created `PROGRAM_Z2_HYBRID_APPROVAL.md`.

Implementation:

- `admin_core/hybrid_approval.py`
- `tools/v7-hybrid-approval-contract`
- `tests/unit/test_v7_hybrid_approval.py`

## 6. Policy Fingerprint

Created `PROGRAM_Z2_POLICY_FINGERPRINT.md`.

Fingerprints:

- proposal: `87eacb4f30bc23f5f13236d8a6296a282e63c1d03985105d46fa05f41a629692`
- policy: `7293744babf174e3d1fda4dc1416beddef2822493ac445edf080c4b877578fde`
- runtime: `a35ea271f45acc2416ecf9154ccecea37f84b58f87f1abb213dca469c6b77049`

## 7. Target Substitution

Created `PROGRAM_Z2_TARGET_SUBSTITUTION.md`.

Z2 policy substitution allowed target `awg3` because route class, trust class, policy class, capacity, user, and rollback were compatible.

Execution-only targets require exact target approval.

## 8. Runtime Recheck

Created `PROGRAM_Z2_RUNTIME_RECHECK.md`.

Recheck validates expiry, fingerprints, registry hashes, selected moves, safety state, budget, target substitution, and replay.

## 9. Autonomy Execution

Created `PROGRAM_Z2_AUTONOMY_EXECUTION.md`.

Z2 executed the governance record path:

- record type: `hybrid_autonomy_record`
- record hash: `15bdcb56f24898ff3a6855501514bcdaf16e11d73cda91c87f96461765586d2c`
- movement executor invoked: `false`

Real runtime movement was not executed.

## 10. Autonomy Certification

Created `PROGRAM_Z2_AUTONOMY_CERTIFICATION.md`.

Contract-level autonomy is certified. Live movement autonomy is not certified.

## 11. Replay

Replay protection was verified by rerunning validation after the audit record:

- verdict: `DENY_HYBRID_APPROVAL`
- error: `approval_replay`

## 12. Fail Closed

Created `PROGRAM_Z2_FAIL_CLOSED.md`.

Unit tests cover expired approval, stale fingerprint, budget greater than `1`, replay, and execution-only target without exact approval.

Verification:

- targeted Z2/operator tests: `14 tests OK`
- full unit discovery: `175 tests OK`
- `py_compile`: PASS
- trailing whitespace scan on Z2 files: PASS
- credential scan for pasted sensitive strings: PASS

## 13. Final Certification

Created `PROGRAM_Z2_FINAL_CERTIFICATION.md`.

Final certification:

`READY_WITH_BLOCKERS`

The contract is ready. Live bounded autonomy remains blocked until a fresh live runtime path is available and the existing movement authority is invoked through this validator or through an explicitly approved packet.

## 14. Remaining Risks

- Live runtime state was not mounted in this workspace.
- Real movement was not executed under Z2.
- Existing movement authority is still external to the new hybrid approval validator.
- Any Program Z3 live execution must run a fresh runtime recheck immediately before movement.

## 15. Recommendation For PROGRAM Z3

Program Z3 should be:

`Live Hybrid Bounded Autonomy Execution`

Required scope:

- use Z2 hybrid validator
- use budget `1`
- use exactly one user
- use existing `v7-users-autoswitch` or `v7-user-switch` movement authority
- run fresh live runtime recheck immediately before movement
- deny on any drift
- record before/after/delayed/final observation
- keep rollback ready

## Required Verdicts

- hybrid_approval_implemented=true
- policy_fingerprint_working=true
- target_substitution_working=true
- runtime_recheck_working=true
- autonomous_execution_successful=false
- autonomy_certified=false
- replay_protection_verified=true
- fail_closed_verified=true
- bounded_autonomy_certified=false
- safe_to_continue_to_program_z3=true

## Safety Verdict

- autonomous_budget<=1
- scope_expanded=false
- autoswitch_apply_outside_packet=false
- routing_changed_outside_scope=false
- deploy_performed=false
