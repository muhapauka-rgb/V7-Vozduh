# Authority and Bypass Suitability Analysis

## Authority Suitability

| Authority | Currently Has Authority | Should Have Authority | Should Lose Independent Authority Later | Advisory / Read-Only Candidate |
|---|---|---|---|---|
| Runtime lifecycle | Autoswitch partial; Admin/manual paths conflict | `tools/v7-users-autoswitch` | Direct Admin/CLI lifecycle authority | Admin/operator views |
| Scheduling | systemd autoswitch timer | systemd autoswitch timer only | draft planner timer if ever active | Admin visibility |
| Planning | Autoswitch | Autoswitch | draft planner scheduler | Admin dry-run |
| Proposal | Admin proposal layer, historical packets | Admin proposal layer | historical packet as live authority | Autoswitch consumes only approved/gated data if connected later |
| Selected moves | Autoswitch in-process; file readers | Autoswitch | persistent file readers as authority | Admin gates/observability |
| Restore barrier | Autoswitch enforcement; fragmented writer | Autoswitch for runtime lifecycle suitability | manual/historical writes as normal path | Admin closure/evidence |
| Runtime recheck | Autoswitch, operator zero-move, Admin preview | Autoswitch for movement, Admin/operator for evidence | zero-move engine as movement executor | Admin preview gates |
| Execution | Autoswitch, Admin, CLI primitive | Autoswitch | Admin direct switch and CLI independent lifecycle authority | Admin operator action surface |
| Rollback | Autoswitch, Admin, generic rollback | Autoswitch for movement rollback; generic tool as primitive | generic rollback as lifecycle owner | Admin rollback preview |
| Audit | `v7-audit-log`, Admin audit, operator audit, JSONL events | `v7-audit-log` as canonical sink | report-only/manual audit as source of truth | Admin/operator audit search/export |
| Closure | Admin closure records, historical reports | Admin/operator closure layer with runtime outcome input | historical report-only closure | Runtime owner emits final outcome |

## Bypass Inventory

| Bypass Path | Why It Exists | Required? | Duplicates Authority? | Conflicts With Ownership? | Production Safety |
|---|---|---:|---:|---:|---|
| `systemd/v7-users-autoswitch.service` running `--apply` | Autonomous guarded failover/rebalance | Yes | Yes, versus Admin execution contracts | Yes, because it bypasses approval packet path | Production-active but partially governed by policy/safety/barrier. |
| Admin autoswitch apply | Manual guarded operator action | Yes, as operator surface | Yes, same engine execution outside contract lifecycle | Medium conflict | Safer than raw CLI due confirm/audit, but still bypasses preview-only contracts. |
| Admin direct user switch | Manual targeted movement | Yes, break-glass/operator tool | Yes, bypasses planner selected moves | High conflict | Auth/CSRF/audit exists, but lifecycle conflict remains. |
| CLI `v7-user-switch` | Low-level movement primitive | Yes as primitive | Yes if used directly | High conflict | Unsafe as independent lifecycle path unless wrapped. |
| `v7-telegram-sentinel` autoswitch invocation without `--no-autoswitch` | Fast service-specific emergency action | Not required in production unit | Yes | High latent conflict | Production unit uses `--no-autoswitch`, lowering active risk. |
| `v7-rollback-last-change --apply` | Generic recovery from bad file/config changes | Yes as low-level rollback primitive | Yes, rollback not contract-scoped | Medium/high conflict | Confirmed through Admin endpoint; direct CLI remains broad. |
| Proxy runtime guard rollback | Domain-specific proxy rollback | Yes for proxy runtime failures | Some | Medium | Guarded Admin path. |
| Persistent selected-move file readers | Historical evidence and gates | Required as evidence/read adapters | Could duplicate selected-move truth | High if treated as live source | Safe only as read/evidence. |
| Draft planner timer | Draft planner refresh | No active production need found | Yes if enabled | High latent conflict | DO NOT TOUCH. |

## Components That Should Become Advisory or Read-Only

- `v7-telegram-sentinel`: advisory/signal writer only, not execution trigger.
- Admin execution contracts: read-only validation/governance until deliberately connected.
- Persistent selected-move file adapters: read/evidence only.
- Operator observability: evidence/audit/closure surface only.
- Draft planner timer: dormant/do-not-touch.

## Components That Should Remain Execution-Capable

- `tools/v7-users-autoswitch`: primary runtime/execution owner candidate.
- `v7-user-switch`: low-level primitive, but should not be independent lifecycle authority.
- `v7-rollback-last-change`: low-level rollback primitive, but should not be lifecycle owner alone.
- Admin action endpoints: operator surface for controlled invocation, not primary lifecycle owner.

