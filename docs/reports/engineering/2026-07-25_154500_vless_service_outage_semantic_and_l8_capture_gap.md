# VLESS: service outage, semantic display and L8 capture gap

## Scope

Read-only production audit after an operator observed the `vless` channel with users assigned, a red service signal and a green Runtime/readiness signal. No user, route, packet, Runtime state, restore barrier, rollback, Authority or Production Maturity was changed.

## Observed facts

- Fresh service matrix observation: `2026-07-25T08:42:18Z`.
- `vless` matrix status: `WARN`; `youtube`, `whatsapp`, `google`, `apple`, `google_auth`, `chatgpt`, `openai_auth`, `instagram`, `facebook`, `spotify`, `soundcloud`, `claude` and `anthropic` were `FAIL`; only `telegram` was `OK`.
- Failure class in each observed row: TLS receive-reset (`curl: (35)`), not one of the configured HTTP probe-methodology exceptions.
- Existing quality owner simultaneously reported `current=0.0`, `trend=degrading`, `penalty=99.15`.
- The UI green `R` signal is not a service-health assertion. Its owner is `egress_runtime_readiness()`: registry/config/enable-readiness. The tooltip says «канал подтвержден текущим снимком», which is technically about Runtime readiness but is misleading next to a red service signal.
- The UI decision `Перевести` is a recommendation, not execution. No new VLESS Candidate, Packet, lease, movement or Outcome Passport was found for this observation.

## Root cause

`tools/v7-users-autoswitch` correctly requires `service_failure_persistence_samples=3` or `service_failure_persistence_window_seconds=180` before it treats a service failure as `PERSISTENT_FAIL`. The producer `tools/v7-service-matrix-test` currently writes service status/OK data but does not persist `failure_samples`, `consecutive_failures`, `bad_for_seconds` or an equivalent durable history. On a new planner load the consumer therefore falls back to one transient sample.

Result: a broad fresh service outage can remain a visible warning/recommendation without producing the existing owner chain:

`service matrix → persistence classification → source incident → Situation → Decision Trace → safe Candidate/STOP_SAFE → Outcome Passport → replay/Learning → CPS/OMP`.

## L8 classification

This is an `L8_CANDIDATE_PENDING_PROVENANCE_AND_PERSISTENCE`, not L8 credit.

It may become qualifying natural L8 evidence only if the outage is proven not operator-induced and the full existing-owner chain records a complete outcome. A screenshot or a single probe batch is not a natural Outcome Passport. It must not cause a bulk move: any action remains constrained by the existing policy, fresh source/target verification and bounded scope.

## Required smallest repair

Extend the existing service-matrix/history producer so repeated, source-bound failures are durably carried into the existing autoswitch consumer with timestamp, count/window, provenance and probe-methodology classification. Then run focused regression tests and an affected replay. The admin surface must name the green signal `Runtime/config readiness` and explicitly state that it does not certify service availability.

## Legal terminal

`IMPLEMENTATION_DEFECT_SERVICE_FAILURE_PERSISTENCE_AND_OPERATOR_SEMANTICS`; no L7/L8, Authority or Production Maturity credit granted.
