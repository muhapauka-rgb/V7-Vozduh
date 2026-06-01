# Legacy Owner and Closure Analysis

## Legacy / Partial / Dormant Owners

| Owner | Type | Current Role | Suitability |
|---|---|---|---|
| `systemd/drafts/v7-autoswitch-planner.*` | Draft/dormant | Alternative planner scheduler path | Do Not Touch. Keep out of production authority unless later explicitly retired or governed. |
| Persistent selected-move evidence files | Historical/evidence | Read by Admin/operator gates and restore-settle samples | Retire Later as authority; keep as evidence until canonical selected-move source is settled. |
| Historical approval packets | Historical | Manual/governed movement instructions and rollback hints | Keep as evidence, not live authority. |
| Operator execution zero-move engine | Partial owner | Recheck and append-only record for zero-move governance | Keep and extend suitability later; do not treat as current movement executor. |
| Admin execution contract store | Partial/read-only owner | Preview contracts, validation, rollback preview, event views | Keep as governance/read model; not current execution authority. |
| Manual CLI movement | Break-glass/primitive | Direct `v7-user-switch` use | Retire Later as independent lifecycle path; keep primitive behind owner. |
| Manual/generic rollback | Break-glass/primitive | `v7-rollback-last-change --apply` | Retire Later as lifecycle authority; keep primitive. |
| Report-only closeouts | Historical closure | Human-generated final reports | Keep as evidence; not machine lifecycle owner. |

## Closure Reality

Z6.2 found no unified lifecycle closure owner. Z6.3 confirms that closure is split across:

- autoswitch command completion and stdout JSON;
- autoswitch safety/reconnect/load state writes;
- Admin audit wrappers;
- `v7-audit-log`;
- Admin closure records through `/api/actions/closure-set`;
- operator observability timeline and audit export preview;
- historical markdown reports.

## Closure Suitability

The closest existing component to becoming lifecycle closure owner is:

`admin/v7-admin-api` closure model + `admin_core/operator_observability.py`, backed by `tools/runtime-support/v7-audit-log`.

Reason:

- Admin already has closure records with `object_type`, `object_id`, `closure_state`, reason, actor, timestamp, and audit call.
- Operator observability already presents operation timeline, runtime verdicts, operation detail, audit export preview, governance preview, and rehearsal preview.
- It is already operator-facing and non-runtime-mutating.
- It should not own live movement execution.

Boundary:

- The runtime owner candidate (`tools/v7-users-autoswitch`) should provide execution outcomes and terminal runtime facts.
- The closure owner candidate should record final operation closure and audit completion.
- The audit sink candidate (`v7-audit-log`) should remain the canonical event sink.

## Closure Conflict

Conflict level: HIGH.

Reasons:

- Autoswitch can complete a runtime cycle without an Admin closure record.
- Admin direct user-switch can complete movement outside autoswitch selected moves.
- Generic rollback can complete rollback outside contract-scoped rollback.
- Historical reports close operations in markdown without becoming machine-readable runtime closure.
- Execution contracts define terminal event names but are preview-only and non-authoritative.

## Owner Candidate Verdicts

| Lifecycle Completion Area | Owner Candidate |
|---|---|
| final runtime verdict | `tools/v7-users-autoswitch` should provide runtime outcome; Admin/operator should display and close. |
| operation closure | Admin closure model + operator observability. |
| execution completion | `tools/v7-users-autoswitch` for live movement; Admin action surface only as secondary. |
| rollback completion | `tools/v7-users-autoswitch` for movement rollback, `v7-rollback-last-change` for generic primitive, Admin/operator for closure. |
| final audit completion | `v7-audit-log` as sink, Admin/operator closure as surface. |

