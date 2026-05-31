# P3.A Implementation Conflict Audit

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Purpose

This audit checks whether equivalent implementations already exist before defining P3.A. Repository reality overrides assumptions. P3.A is architecture-only and must not create a parallel runtime system.

## Conflict Summary

Equivalent and adjacent implementations exist. They are not blockers because P3.A does not implement new runtime behavior. They are mandatory reuse boundaries.

## Existing Equivalent Surfaces

| Target P3.A capability | Existing implementation | Conflict risk | Required decision |
| --- | --- | --- | --- |
| Runtime observation | `tools/v7-observability-summary`, `tools/runtime-support/v7-state-json`, admin runtime views | Medium | Reuse existing observers as input adapters. |
| Runtime health evidence | Service matrix, Telegram sentinel, egress summaries, trusted RU diagnostics | Medium | Treat as canonical evidence, not duplicate stores. |
| Dry-run routing evaluation | `v7-proxy-service-aware-routing-dry-run`, trusted RU decision preview | Medium | Reuse read-only route simulation semantics. |
| Autoswitch candidate scoring | `tools/v7-users-autoswitch` | High | Reuse only non-apply evaluator semantics; never call apply. |
| Candidate/review/approval | Admin P2.7 candidate and execution candidate workflow responses | Medium | Reuse state vocabulary and UI placement. |
| Contract preview | Admin execution contract preview family | Medium | Extend conceptually; do not create second contract truth source. |
| Validation/verification/rollback preview | Admin execution preview family | Medium | Reuse preview vocabulary. |
| Operator governance/rehearsal preview | `admin_core/operator_observability.py` | Low | Reuse as operator-facing aggregation. |

## High-Risk Conflict Boundaries

### Autoswitch Apply Boundary

`tools/v7-users-autoswitch` contains the real candidate/gate/scoring vocabulary, but it also has apply-capable flows. P3.A must not invoke or wrap apply mode. Dry-run decisions may say `WOULD_MOVE`, but must never produce `MOVE`, `APPLY`, `EXECUTE` or `ROUTE`.

### Telegram Sentinel Boundary

`tools/v7-telegram-sentinel` is both an observer and an action-adjacent coordinator because it can trigger guarded autoswitch unless run with no-autoswitch or dry-run options. P3.A must consume sentinel outputs only. It must not call the sentinel as a runtime hook.

### Trusted RU Decision Boundary

`tools/runtime-support/v7-trusted-ru-decision` can produce read-only decisions and can optionally write state. P3.A may use read-only decision evidence only. It must not enable `--write-state`.

### Operator Execution Boundary

`admin_core/operator_execution.py` states that it does not move users, change routing or control services, but it contains execution-named flows and audit/governance append paths. P3.A must not depend on it as a runtime dry-run engine. It can be referenced only as an existing governance boundary and conflict area.

## Parallel System Risk

No new runtime engine, event bus, scheduler, routing hook, execution queue or autoswitch bridge should be introduced in P3.A. The foundation should be a normalized read model over existing evidence and previews.

## Migration Decision

| Existing area | Decision |
| --- | --- |
| Admin preview API family | Reuse / extend in later blocks if implementation is requested. |
| Existing runtime support dry-run CLIs | Reuse as source semantics, not runtime commands. |
| Existing state stores | Reuse as canonical inputs. |
| Existing execution events/contracts | Reuse as canonical preview store. |
| New P3.A persistent store | Do not create in P3.A. |

## Conflict Verdict

`implementation_conflict_audit_complete=true`

