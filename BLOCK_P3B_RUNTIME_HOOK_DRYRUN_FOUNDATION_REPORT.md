# BLOCK P3.B Runtime Hook Dry-Run Foundation Report

Project: V7 Vozduh
Program: P3
Block: P3.B
Mode: Architecture / Discovery / Hook Design / Certification

## Baseline

- Current branch: `v7-next`
- Local HEAD: `afcdd9cc61b7a1302c8785489991b0eac217b395`
- P3.A status: complete
- P3.A continuation verdict: `safe_to_continue_to_runtime_hook_dryrun=true`
- Runtime mutation performed: no
- Deployment performed: no
- Git push/merge performed: no

## 1. Reality Audit

Created: `P3B_REALITY_AUDIT.md`

The repository already has runtime observers, dry-run route evaluators, autoswitch evaluator semantics, trusted RU diagnostics/decision previews, execution previews, candidate workflow, readiness, simulation, verification, rollback and operator observability.

P3.B therefore defines hook design as a passive derived layer over existing sources. It does not create a new runtime hook daemon, event stream, execution queue or autoswitch engine.

## 2. Conflict Audit

Created: `P3B_IMPLEMENTATION_CONFLICT_AUDIT.md`

Conflict zones:

- `tools/v7-users-autoswitch` is useful as non-apply evaluator semantics, but `--apply` is forbidden.
- `tools/v7-telegram-sentinel` is useful as observer evidence, but its autoswitch trigger path is forbidden.
- `tools/runtime-support/v7-trusted-ru-decision` is useful as read-only preview, but `--write-state` is forbidden.
- `admin_core/operator_execution.py` is not a hook foundation because it has execution-named and append-capable modes.

## 3. Truth Source Audit

Created: `P3B_TRUTH_SOURCE_AUDIT.md`

Hook outputs are derived only. Canonical sources remain:

- Existing runtime state files and registries.
- Existing audit/event stores.
- Existing execution contracts/events.
- Existing candidate/proposal/evidence stores.
- Existing readiness/simulation/verification/rollback preview sources.

No new hook-owned truth source is allowed.

## 4. Runtime Audit

Created: `P3B_RUNTIME_AUDIT.md`

Runtime evidence sources were mapped: health, capacity, required services, runtime trust, release trust, candidate state, execution state, audit state, sentinel state, autoswitch inputs and rollback state.

Runtime mutation boundaries remain excluded: autoswitch apply, policy apply, routing apply, user movement, decision state writes, systemd/service control, deployment, and operator execution append/execute paths.

## 5. Hook Domain Model

Created: `P3B_HOOK_DOMAIN_MODEL.md`

Defined roles:

- Runtime Hook
- Observer
- Evaluator
- Decision Producer
- Verification Producer
- Report Producer

The hook lifecycle is passive: observe, load canonical inputs, check freshness, evaluate fail-closed, produce non-executable decision, attach evidence, render report, expire/compact.

## 6. Hook Inputs

Created: `P3B_HOOK_INPUT_MODEL.md`

Inputs include health, capacity, required services, runtime trust, release trust, candidate state, execution state, audit state, sentinel state and autoswitch inputs. Each input has ownership, freshness and retention constraints.

## 7. Hook Outputs

Created: `P3B_HOOK_OUTPUT_MODEL.md`

Allowed outputs:

- `NO_ACTION`
- `WOULD_MOVE`
- `WOULD_BLOCK`
- `WOULD_REVIEW`
- `WOULD_ROLLBACK`

Forbidden outputs:

- `MOVE`
- `EXECUTE`
- `APPLY`
- `ROUTE`
- `AUTOSWITCH_APPLY`

## 8. Hook Contract

Created: `P3B_HOOK_CONTRACT_MODEL.md`

The hook contract binds trigger, scope, input refs, input hashes, freshness, ownership, decision, evidence, simulation, verification plan, rollback simulation, confidence, authority flags, expiry and retention class.

It is not an execution contract and cannot be accepted by an executor.

## 9. Hook Observability

Created: `P3B_HOOK_OBSERVABILITY_MODEL.md`

Operators should see what happened, what was observed, what would happen, why, evidence, confidence, verification plan and rollback simulation. Existing `/admin-v2` surfaces should be reused; no new top-level section is needed.

Forbidden UI controls: execute, apply, route, autoswitch apply, move user, write decision state, register authoritative runtime hook.

## 10. Hook Retention

Created: `P3B_HOOK_RETENTION_MODEL.md`

Retention follows P2.5 and P3.A:

- Derived views by default.
- TTL-bound hook contracts only if persistence is later required.
- Source refs and hashes instead of copied truth.
- No infinite streams.
- No hook-local queues.

## 11. Hook Certification

Created: `P3B_HOOK_CERTIFICATION_MODEL.md`

The certification model proves:

- No execution authority.
- No runtime mutation.
- No routing mutation.
- No autoswitch authority.
- No user movement.
- No policy apply.
- No deploy/systemd.
- Fail-closed behavior.
- Bounded retention.
- Clean truth-source ownership.

## 12. Risks

| Risk | Level | Mitigation |
| --- | --- | --- |
| Hook accidentally reaches autoswitch apply | Critical | Static denylist and tests before any implementation. |
| Sentinel action path treated as hook | High | Consume sentinel state only. |
| Trusted RU write-state used by hook | High | Read-only mode only. |
| Hook output becomes decision truth | High | Derived-only contract with source refs and expiry. |
| Hook-local queue grows forever | Medium | No hook-local queues; TTL/compaction if persistence is needed. |
| UI adds action controls | High | Existing admin surfaces only, disabled/no execute controls. |
| Operator execution boundary reused | Medium | Keep out of P3.B hook lifecycle. |

## 13. Recommendation For P3.C

Proceed to First Runtime Dry-Run only as a non-executable implementation block with tests first. P3.C should implement the smallest read-only report path, ideally behind existing admin preview/read surfaces, using existing canonical inputs and without any runtime hook with authority.

P3.C must include fail-closed tests proving:

- No apply/execute/route/autoswitch endpoints or command paths.
- No runtime state writes.
- No decision state writes.
- No user movement.
- No deploy/systemd.
- No unbounded hook-local stream.

## Required Verdicts

`reality_audit_complete=true`

`implementation_conflict_audit_complete=true`

`truth_source_audit_complete=true`

`runtime_audit_complete=true`

`hook_domain_defined=true`

`hook_input_model_defined=true`

`hook_output_model_defined=true`

`hook_contract_defined=true`

`hook_observability_defined=true`

`hook_retention_defined=true`

`hook_certified_non_executable=true`

`safe_to_continue_to_first_runtime_dry_run=true`

## Safety Verdict

`runtime_mutation_performed=false`

`routing_changed=false`

`users_moved=false`

`autoswitch_apply_run=false`

`execution_engine_implemented=false`

`runtime_hooks_with_authority=false`

`deploy_performed=false`

## Stop Condition

P3.B report complete. P3.C was not started.

