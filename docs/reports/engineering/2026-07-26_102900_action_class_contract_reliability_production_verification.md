# Engineering Report — Action Class Contract reliability hardening

Date: 2026-07-26

## Scope and owner

The existing `admin_core/operator_execution.py` Authority owner and the
existing `/etc/v7/policy.json` contract field were hardened. No new Authority,
registry, queue, watcher, Runtime or routing path was introduced.

## Implemented closure

- Consumption rejects an expired v2 contract.
- The existing owner serializes policy read, validation and atomic replacement
  with an interprocess advisory lock. Two consumers cannot both consume one
  `ISSUED` contract.
- The existing append-only production owner
  `/opt/v7/audit/operator-execution-audit.jsonl` records one exact
  `APPROVE_ONCE_AS_SCOPED` or `DECLINE` with actor provenance and records
  consumption.
- Requests bind a nonempty incident identity/generation, fresh source
  generation, current policy generation, exact one-user scope and the actual
  Authority ceiling. Incomplete verification/rollback contracts, missing
  mandatory STOP conditions, a changed policy generation or an exceeded ceiling
  fail closed.

## Verification

- Focused suite: 366 tests passed.
- Commit `b12a99a48f62e83c8d2ed3c7b2a77d6aebd41375` was deployed only through
  `tools/v7-safe-deploy`; its passed manifest replaced only
  `/usr/local/bin/v7-users-autoswitch` and
  `/usr/local/bin/admin_core/operator_execution.py`.
- Production non-test caller
  `v7-users-autoswitch --action-class-contract-reconciliation-only` returned
  `PASS` / `ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY` with a fresh owner-backed
  incident generation, source generation, policy-generation binding and
  Authority ceiling.
- Caller effects remained zero: no policy write, Authority grant, Candidate,
  Packet, lease, Runtime apply, routing mutation, user movement, rollback or
  Production Maturity change.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`, `FULLY_ALIGNED`; local, GitHub
  and production deploy provenance matched the deployed commit.

## Legal terminal

Engineering repair and production caller verification are complete. The only
remaining boundary is an independent exact decision for the caller's fresh
one-use request. No contract was issued and no production action occurred.
