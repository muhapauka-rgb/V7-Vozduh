# Rollback, Restore Barrier, and Closure Models

## Rollback Model

| Rollback Type | Owner | Authority | Scope | Limitations |
|---|---|---|---|---|
| Primary movement rollback | `tools/v7-users-autoswitch` | Runtime movement lifecycle rollback | Users moved by the runtime owner in the current operation | Should not own broad file/config rollback. |
| Secondary generic rollback | `tools/runtime-support/v7-rollback-last-change` | Primitive rollback tool | Latest backup under configured roots | Too broad to be lifecycle owner; must be invoked through owner/surface. |
| Admin rollback surface | `admin/v7-admin-api` | Operator-controlled wrapper | Preview/apply wrapper around rollback primitive | Should not become independent rollback truth. |
| Proxy guard rollback | Admin + proxy runtime guard tool | Domain-specific emergency rollback | Proxy runtime guard domain | Supporting/emergency only. |
| Historical rollback | approval packets/reports | Evidence | Previous manual governed operations | Not live authority. |
| Emergency rollback | CLI primitives | Break-glass | Manual emergency recovery | Must remain exceptional, audited, and not canonical lifecycle path. |

Primary rollback owner:

`tools/v7-users-autoswitch` for movement lifecycle rollback.

Secondary rollback owner:

Admin operator surface plus `v7-rollback-last-change` as low-level primitive.

## Restore Barrier Model

Most important unresolved area from Z6.3.

| Restore Barrier Stage | Future Owner | Reason |
|---|---|---|
| creation | Admin/operator closure/governance surface initiates; autoswitch owns runtime-valid shape | Creation is an operator/governance event, but runtime owner must define what it will consume. |
| validation | `tools/v7-users-autoswitch` | Autoswitch already validates active/expired/cleared/generation/hash/count/budget semantics. |
| consumption | `tools/v7-users-autoswitch` | Barrier exists to suppress or allow runtime selected moves. |
| expiration | `tools/v7-users-autoswitch` interprets expiry; Admin displays expiry | Runtime meaning of expiry must live with runtime owner. |
| clearance | Admin/operator closure surface records intent; autoswitch validates generation/hash/count/budget | Clearance is operator intent plus runtime validation. |
| closure | Admin closure model + operator observability | Closure is lifecycle/evidence state, not movement execution. |
| audit | `v7-audit-log` | Canonical event sink. |

Restore-barrier target rule:

- Autoswitch owns whether a barrier allows or blocks execution.
- Admin owns the operator-visible lifecycle record for why the barrier exists or is closed.
- `v7-audit-log` owns canonical audit events.
- Persistent barrier files remain the transport/state object, not a separate owner.

## Lifecycle Closure Model

Operation considered COMPLETE when all are true:

1. Runtime owner has emitted terminal runtime outcome: no-op, executed-and-verified, failed-closed, rolled back, cancelled, expired, or denied.
2. Rollback requirement is either not applicable, completed, or explicitly failed-closed.
3. Canonical audit event exists or the absence is marked as a closure blocker.
4. Admin/operator closure record is set with actor, reason, timestamp, and terminal state.
5. Operator observability can display the operation with final runtime verdict and evidence references.

Who declares completion:

- Runtime completion: `tools/v7-users-autoswitch`.
- Operation closure: Admin closure model + operator observability.
- Audit completion: `v7-audit-log` presence plus Admin/operator closure evidence.

Who declares failure:

- Runtime failure: `tools/v7-users-autoswitch`.
- Closure failure/blocker: Admin/operator closure model.
- Audit failure/blocker: Admin/operator closure model based on missing or failed audit evidence.

Who declares rollback complete:

- Movement rollback complete: `tools/v7-users-autoswitch`.
- Generic rollback complete: `v7-rollback-last-change` result, recorded through Admin/audit.
- Operation rollback closure: Admin/operator closure model.

Who owns final lifecycle verdict:

- Runtime verdict: `tools/v7-users-autoswitch`.
- Operation/lifecycle closure verdict: Admin closure model + operator observability.
- Audit truth: `v7-audit-log`.

Who owns closure truth:

`admin/v7-admin-api` closure records plus `admin_core/operator_observability.py`.

