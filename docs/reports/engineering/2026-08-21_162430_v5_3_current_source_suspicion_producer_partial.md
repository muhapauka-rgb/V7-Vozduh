# V5.3 current-source suspicion producer implementation

Date: `2026-08-21`
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`
Input terminal: `FAST_SIGNAL_COVERAGE_PARTIAL`
Bounded block: `CURRENT_SOURCE_FAST_SUSPICION_PRODUCER_IMPLEMENTATION`

## 1. Final terminal

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

The missing upstream side is now implemented for one proven path:
`v7-egress-diagnose` can turn an existing current-source path failure
(`curl_failed_and_handshake_stale` or
`curl_failed_and_handshake_unsupported`) into the existing Matrix
observation-only exact-source/exact-service-subset trigger.

The implementation is opt-in and shadow/Polygon-only. The production health
unit does not pass the new trigger arguments, so cadence, routes, clients,
Runtime and automatic FAST are unchanged.

The remaining five action-relevant classes still lack a trustworthy upstream
producer and remain the exact residual.

## 2. Implemented producer and receiver chain

```text
current-source diagnose
→ bounded suspicion: TUNNEL_UP_INTERNET_DEAD
→ existing v7-service-matrix-refresh-all
→ exact source + exact non-empty service subset
→ existing v7-service-matrix-test
→ existing Matrix writer / episode / persistence
```

The producer only emits suspicion. It never writes canonical channel health,
selects a target, invokes Planner action, creates a Packet/Lease, changes a
route or moves a user.

New optional producer arguments in the existing `tools/v7-egress-diagnose`:

- `--shadow-trigger-command`;
- `--shadow-trigger-egress`;
- `--shadow-trigger-services`;
- `--shadow-trigger-event-dir`;
- `--shadow-trigger-cooldown-sec`.

The producer refuses an incomplete scope, requires an exact source and service
subset, and invokes the receiver only in `--matrix-observation-only` mode.
Duplicate wake is suppressed by the existing Matrix episode/generation
semantics plus a bounded producer cooldown in the existing diagnose state.

## 3. Existing owner boundary

No new owner, timer, queue, registry or truth source was introduced.
`v7-health.service` remains the existing 30-second producer cadence and
`v7-users-autoswitch.timer` remains the existing 20-second downstream caller.
The production unit files were not changed; the new arguments are used only by
the Polygon invocation.

The exact required-service subset remains supplied by the existing profile or
caller contract. The producer does not contain a global hard-coded service
policy.

## 4. Coverage of the frozen 17-class matrix

| Group | Classes | Status |
| --- | --- | --- |
| FAST failure covered | `HARD_CHANNEL_DOWN`, `INTERFACE_OR_TUNNEL_PROCESS_ABSENT`, `TUNNEL_UP_INTERNET_DEAD`, `TELEGRAM_PERSISTENT_FAILURE` | owner-backed shadow covered |
| FAST failure exact residual | `REQUIRED_SERVICE_FAILURE`, `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`, `DNS_FAILURE`, `PARTIAL_CENSORSHIP`, `MULTI_SERVICE_FAILURE` | no upstream producer proven |
| Intentionally degraded, not hard-down | `LATENCY_LOSS_JITTER_DEGRADATION` | quality/degraded semantics retained |
| Recovery only | `CLEAN_RECOVERY`, `FAIL_RECOVER_FAIL` | recovery/re-admission semantics retained |
| Safety class | `TRANSIENT_FALSE_ALARM`, `STALE_OR_UNKNOWN_STATE`, `CONFLICTING_GENERATION`, `TARGET_UNAVAILABLE`, `CAPACITY_OR_POLICY_DENIAL` | STOP_SAFE/fallback |

## 5. Causal timing and economics

Before, tunnel-up/Internet-dead failures entered the ordinary Matrix cadence:
up to `900 s` signal wait plus the existing confirmation policy.

With the producer enabled in the existing health cadence, the signal wait is
bounded by the existing approximately `30 s` health cycle; the receiver then
uses only the current source and supplied subset. The exact `F→T0` gain is not
promoted to production because the production unit remains unmodified and the
Polygon receiver path still uses existing confirmation/fallback rules.

| Scenario | Before | Shadow after | Full role |
| --- | ---: | ---: | --- |
| tunnel-up/Internet-dead | up to 900 s cadence | up to existing 30 s health cadence + bounded subset confirmation | disagreement/fallback |
| required service / DNS / partial / multi | up to 900 s cadence | no producer yet | required before T0/action |
| hard local channel/process | existing 30 s health + 20 s caller | existing path | async/fallback |
| Telegram persistent | 14 s sentinel | existing path | async deep/fallback |
| quality degradation | quality cadence | no hard-down trigger | background/degraded |
| recovery | recovery cadence | no failure wake | re-admission |

The producer performs no all-egress scan. Its work is one current source and
the exact subset. Duplicate invocations inside cooldown are suppressed.

## 6. Polygon proof

The real producer caller path was exercised in a temporary Polygon state:

```text
synthetic current-source path failure
→ v7-egress-diagnose producer
→ real v7-service-matrix-refresh-all
→ exact source/subset
→ real v7-service-matrix-test
→ temporary service-matrix.json writer
```

The test verified the exact `google,telegram` subset, Matrix state creation,
observation-only mode and zero client movement.

## 7. Mature-system conformance

| Pattern | Disposition |
| --- | --- |
| BFD/Cisco hard liveness separation | REUSE existing diagnose as suspicion only |
| Envoy passive escalation | ADAPT bounded wake, not route action |
| HAProxy fall/rise | REUSE Matrix persistence; no thresholds changed |
| Fortinet SLA distinction | REJECT hard-down shortcut for quality |
| Google target separation | REUSE existing Planner readiness |

## 8. Verification

Passed:

- `v7-egress-diagnose` producer and regression tests: `10/10`;
- owner/17-class/receiver contract tests: `6/6`;
- previous fast-signal coverage tests: `7/7`;
- autoswitch, causal, passive and sentinel tests: `40/40`;
- `tools/v7-truth-check --continue-omp --json`: `PASS`.

The full service-failure episode suite remains `90/92`; the same two legacy
CT-M0F controlled-source/binding tests fail their existing `result["ok"]`
assertion. They are outside this producer block.

## 9. Canonical residual and next stage

```text
FAST_FAILURE_EXACT_RESIDUAL
REQUIRED_SERVICE_FAILURE
OTHER_PROFILE_REQUIRED_SERVICE_FAILURE
DNS_FAILURE
PARTIAL_CENSORSHIP
MULTI_SERVICE_FAILURE
```

Next step: prove whether an existing health/profile observation can produce an
early suspicion for the five remaining classes. If not, retain
`FAST_SIGNAL_COVERAGE_PARTIAL` with this exact residual and move to the existing
admission decision. Do not create a generic ping or a new permanent timer.

