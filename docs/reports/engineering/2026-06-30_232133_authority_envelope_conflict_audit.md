# Authority Envelope Conflict Audit

Дата: 2026-06-30 23:21:33 +0700

Вердикт: `AUTHORITY_LAYERING_CANONICAL_NEEDS_FRESH_ENVELOPE`

## Summary

L3 first Production Validation сейчас проходит через несколько authority/safety gates. Это не конфликт архитектур.

Каноническая композиция такая:

```text
OMP / L3 Production Validation authority
  -> fresh concrete execution envelope
  -> approved plan lock / restore barrier
  -> L3 runtime eligibility
  -> apply / verify / rollback / learning
```

Текущий STOP_SAFE произошел потому, что L3 Production Validation authority не была материализована в свежий `approved_plan_lock` + restore-barrier clearance для текущего one-user L3 candidate. Runtime consumed старый governed envelope и правильно fail-closed.

## Semantic Duplicate Audit

| Семантика | Статус | Existing owner |
| --- | --- | --- |
| Explicit scoped authority | `EXISTS_COMPLETE` | `docs/policies/POLICY_004_AUTHORITY.md` |
| L3 production validation authority | `EXISTS_COMPLETE` | OMP + `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` |
| Runtime authority consumption | `EXISTS_COMPLETE` | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` |
| Restore barrier / approved plan lock | `EXISTS_COMPLETE` | `admin_core/operator_execution.py` |
| L3 execution consumer | `EXISTS_COMPLETE` | `tools/v7-users-autoswitch` |
| Fresh L3 PV envelope materialization | `EXISTS_PARTIAL` | Existing restore-barrier owner exists; L3 PV path did not invoke it for the current candidate |

Need New Owner: `FALSE`.
Need New Runtime: `FALSE`.
Need New Architecture: `FALSE`.

## Authority Gates

| Gate | Owner | Purpose | Input | Output | Consumer | Scope / binding | Expiration |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OMP / L3 Production Validation authority | OMP + Policy 004 + L3 capability | Approve the first one-user production-validation rung | L3 state, operator/OMP approval, candidate scope | Approved bounded L3 PV authority | Envelope materialization owner | L3, one user, failover, no expansion | One validation rung / explicit scope |
| Approved plan lock | `admin_core/operator_execution.py` | Bind authority to exact selected move | Packet/selected move | `approved_plan_lock` | Restore barrier + autoswitch | user, source, target, selected move hash, packet, operation | `expires_at` / packet TTL |
| Restore barrier clearance | `admin_core/operator_execution.py` | Materialize executable clearance and rollback/verification readiness | Packet + approved plan lock | `autoswitch-restore-barrier.json` | `tools/v7-users-autoswitch` | generation, selected move hash, allowed users/targets, rollback manifest | `clearance_expires_at` / generation |
| L3 emergency failover authority gate | `tools/v7-users-autoswitch` | Confirm runtime may execute inside emergency failover bounds | selected moves + restore barrier + CLI policy | `ok` or STOP_SAFE blockers | apply stage | max users, restore barrier, rollback, verification, fresh evidence | Live runtime check |
| Execution eligibility / apply gate | `tools/v7-users-autoswitch` | Final execute-or-stop decision | authority, freshness, movement protection, target/source eligibility, restore barrier | apply or STOP_SAFE | verification/rollback/learning | one run, one selected move | current runtime cycle |

## Classification

Restore Barrier / Approved Plan Lock is:

```text
B: additional concrete safety/execution gate after OMP authority
```

It is not the product-level authority itself. It is also not bypassable legacy state. It is the concrete executable envelope that turns an approved scope into one exact safe mutation.

## Live State

Current production restore-barrier file exists and is owned by `admin_core/operator_execution.py`.

Current live envelope:

| Field | Value |
| --- | --- |
| approved user | `10.7.0.25` |
| approved target | `wireguard-1779454504-c43409` |
| packet | `pkt_preview_2e561e6cbcf2e0257692f8f2` |
| operation | `govdry_c56b2d208b64981ccbb6c312` |
| clearance expires | `2026-06-27T16:30:27.502938+00:00` |
| lock expires | `2026-06-27T16:30:27.502938+00:00` |

The current L3 Production Validation candidate from the previous run was:

| Field | Value |
| --- | --- |
| user | `10.0.0.2` |
| source | `openvpn-1779388847-d2ad7c` |
| target | `vless` |
| move type | `failover` |

Therefore the live lock is stale and not scoped to the L3 PV candidate.

## Code Owner Trace

`tools/v7-users-autoswitch`:

- reads restore barrier in `_restore_barrier_status`;
- validates `approved_plan_lock` in `_approved_plan_lock_validation`;
- rejects expired locks with `approved_plan_lock_expired`;
- rejects user/source drift with `approved_plan_lock_user_source_mismatch`;
- checks generation in `_restore_clearance_generation_check`;
- removes selected moves before apply when generation or lock is invalid.

`admin_core/operator_execution.py`:

- canonical clearance owner is `admin_core/operator_execution.py`;
- `build_restore_barrier_clearance` creates `allowed_users`, `allowed_targets`, `approved_selected_moves_hash`, `clearance_generation_id`, `approval_id`, `packet_id`, `operation_id`, rollback id, and attached `approved_plan_lock`;
- `append_restore_barrier_clearance` writes the concrete restore-barrier file.

`tools/v7-governed-canary-dry-run-cycle`:

- can create a fresh governed transaction envelope through the same owner;
- current implementation path is governed/A4 oriented and does not by itself represent the L3 Production Validation materialization contract.

## Canonical Finding

The stale lock is correctly blocking execution.

Reason:

- Policy 004 separates permission from operational safety.
- L3 requires authority inside the current envelope.
- Autonomous Runtime Model requires authority, restore barrier, rollback, verification, freshness, and live eligibility before execute.
- No canonical rule allows L3 PV to ignore an existing invalid concrete execution envelope during apply.

## First Broken Transition

```text
OMP approves one-user L3 Production Validation
  -> fresh approved-plan-lock / restore-barrier clearance materialized
```

The first transition is incomplete. The approval scope exists, but the executable envelope for the selected candidate was not freshly materialized.

## Root Cause

```text
MISSING_AUTHORITY_MATERIALIZATION
```

Canonical root-cause class:

```text
AUTHORITY_LAYERING_CANONICAL_NEEDS_FRESH_ENVELOPE
```

This is not:

- `AUTHORITY_LAYERING_BUG`;
- `STALE_LOCK_CLEANUP_BUG`;
- new authority model;
- new runtime path;
- architecture gap.

The stale lock shadowed the L3 candidate only because no fresh L3 PV envelope replaced it through the existing owner.

## Minimal Executable Fix

Responsible owner:

```text
admin_core/operator_execution.py
```

Authority owner:

```text
OMP + L3 Production Validation + Policy 004
```

Runtime consumer:

```text
tools/v7-users-autoswitch
```

Minimal executable fix:

```text
When OMP/operator approves the one-user L3 Production Validation rung,
materialize a fresh approved_plan_lock + restore-barrier clearance
through the existing operator_execution owner,
bound to the current selected L3 candidate:

user/source/target/selected_move_hash/generation/rollback/verification.

Then run the existing L3 apply/verify/rollback path.
```

No redesign.
No new architecture.
No new owner.
No speculative improvement.

