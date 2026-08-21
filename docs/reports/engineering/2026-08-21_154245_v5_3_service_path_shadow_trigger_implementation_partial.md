# V5.3 service-path shadow trigger implementation and coverage result

Date: `2026-08-21`
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`
Input terminal: `FAST_SIGNAL_COVERAGE_PARTIAL`
Bounded block: `SERVICE_PATH_FAST_TRIGGER_OWNER_BACKED_IMPLEMENTATION`

## 1. Summary and terminal

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

The existing Matrix owner now exposes a guarded shadow-only trigger contract.
An existing caller must provide one exact source, one failure class, one stable
trigger identity and the exact required-service subset. The owner then reuses
the normal Matrix probe/writer path in observation-only mode. It does not call a
consumer, make a Planner decision, create a Packet/Lease, change a route or move
a client.

This closes the owner-side implementation gap, but it does not invent an early
signal producer. Therefore the six action-relevant non-Telegram classes remain
an exact residual until an existing health/path suspicion can invoke this
contract safely.

## 2. Code changes and reuse boundary

Changed only the existing owner `tools/v7-service-matrix-refresh-all`:

- added `build_shadow_trigger_contract(...)`;
- added `--shadow-trigger-source`;
- added `--shadow-trigger-class`;
- added `--shadow-trigger-id`;
- required `--matrix-observation-only`, exactly one `--egresses` value and a
  non-empty `--services` subset;
- rejected missing, multi-source, all-service or non-observation invocations;
- preserved normal `run_one()` and `v7-service-matrix-test` canonical writing;
- emitted only a read-only contract/receipt in the shadow result.

Existing Matrix episode/generation semantics remain the duplicate-suppression
boundary. No new state file, event family, timer, scheduler or truth owner was
added.

## 3. Real caller and consumer

The owner-side call is now proven:

```text
existing health/path caller
→ explicit shadow trigger arguments
→ v7-service-matrix-refresh-all
→ exact current source + exact service subset
→ existing v7-service-matrix-test writer
→ existing Matrix state/episode
```

The shadow contract stops before the downstream consumer. Existing Planner,
target readiness, Packet, lease, barrier, apply and verification owners remain
unchanged. Production automatic FAST remains held, so no production caller was
rewired in this block.

## 4. Failure-class coverage

| Class group | Classes | Result |
| --- | --- | --- |
| Existing early shadow coverage | `HARD_CHANNEL_DOWN`, `INTERFACE_OR_TUNNEL_PROCESS_ABSENT`, `TELEGRAM_PERSISTENT_FAILURE` | owner-backed shadow covered |
| New owner-side trigger contract | `TUNNEL_UP_INTERNET_DEAD`, `REQUIRED_SERVICE_FAILURE`, `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`, `DNS_FAILURE`, `PARTIAL_CENSORSHIP`, `MULTI_SERVICE_FAILURE` | implemented, but upstream suspicion producer not proven |
| Intentionally degraded, not FAST down | `LATENCY_LOSS_JITTER_DEGRADATION` | existing quality/degraded semantics; no hard-down shortcut |
| Recovery only | `CLEAN_RECOVERY`, `FAIL_RECOVER_FAIL` | existing recovery/re-admission semantics; no FAST failure claim |
| Safety roles | `TRANSIENT_FALSE_ALARM`, `STALE_OR_UNKNOWN_STATE`, `CONFLICTING_GENERATION`, `TARGET_UNAVAILABLE`, `CAPACITY_OR_POLICY_DENIAL` | existing STOP_SAFE/fallback gates |

## 5. Confirmation and safety

- A shadow trigger must identify one current source and a non-empty exact
  service subset.
- `--matrix-observation-only` is mandatory.
- Full Matrix remains the fallback and disagreement path.
- Stale, unknown, conflicting, target-invalid or policy-invalid evidence stays
  `STOP_SAFE`.
- Existing Matrix persistence, episode and generation logic is retained.
- No route decision, authority expansion, Packet, Lease or user movement can
  be produced by this contract.
- Quality degradation is not converted into hard failure.
- Recovery is not used to manufacture a failure trigger.

## 6. Causal timing and probe economics

The implementation proves the owner-side bound, not an end-to-end production
gain, because no upstream non-Telegram suspicion producer is currently
connected.

| Scenario | Before failure→signal | Shadow owner segment | Current failure→T0 conclusion | Full role |
| --- | ---: | ---: | --- | --- |
| hard local channel/process | up to 30 s state projection + 20 s caller | existing read path | early shadow evidence | fallback/async |
| Telegram persistent | 14 s | existing sentinel/Matrix path | 14 s modelled | async deep/fallback |
| service/DNS/Internet/partial/multi | up to 900 s Matrix cadence | exact subset through existing owner; bounded by existing probe timeout | end-to-end gain not yet proven | required until trigger source exists |
| quality degradation | quality cadence/history | no hard-down trigger | not a FAST failure clock | background/degraded |
| clean recovery | recovery evidence | no failure trigger | recovery-only | re-admission |

The shadow contract scales with one current source and the supplied subset. It
does not scan all egresses or all services. No production trigger rate or
network budget is claimed until a real existing producer is connected.

## 7. Mature-pattern conformance

| Pattern | V7 disposition |
| --- | --- |
| BFD/Cisco hard liveness separation | reuse existing diagnose path |
| Envoy passive suspicion | adapt as observation-only wake, never direct routing |
| HAProxy fall/rise | retain existing Matrix persistence; no vendor thresholds copied |
| Fortinet service/SLA distinction | reject hard-down shortcut for quality |
| Google target eligibility separation | reuse existing Planner readiness gates |

## 8. Frozen 17-class Polygon and scale status

The exact 17-class inventory was retained. Shadow contract tests cover the six
action-relevant classes and regression groups without production effects. The
owner-side scale model is bounded for 7/50/100/1,000 egresses because the
trigger receives one exact source and subset; a full trigger-rate tournament is
deferred until an upstream producer is connected.

## 9. Verification

Passed:

- owner/trigger/17-class harness: `6/6`;
- previous fast-signal coverage harness: `7/7`;
- autoswitch owner-path targeted tests: `3/3`;
- diagnose, causal, passive and sentinel tests: `38/38`;
- `tools/v7-truth-check --continue-omp --json`: `PASS`.

The complete service-failure episode suite remains `90/92`; the same two
legacy CT-M0F controlled-source/binding tests fail their existing
`result["ok"]` assertion. They are outside this implementation block.

## 10. Final coverage and exact residual

```text
FAST_FAILURE_COVERED
HARD_CHANNEL_DOWN
INTERFACE_OR_TUNNEL_PROCESS_ABSENT
TELEGRAM_PERSISTENT_FAILURE
```

```text
ACTION_RELEVANT_EXACT_RESIDUAL
TUNNEL_UP_INTERNET_DEAD
REQUIRED_SERVICE_FAILURE
OTHER_PROFILE_REQUIRED_SERVICE_FAILURE
DNS_FAILURE
PARTIAL_CENSORSHIP
MULTI_SERVICE_FAILURE
```

```text
INTENTIONALLY_DEGRADED_NOT_FAST_DOWN
LATENCY_LOSS_JITTER_DEGRADATION
```

```text
RECOVERY_ONLY
CLEAN_RECOVERY
FAIL_RECOVER_FAIL
```

## 11. Next stage

Use an existing health/path suspicion producer to invoke the new shadow
contract for one synthetic Polygon source, then run the complete 17-class
causal, fallback and scale comparison. If no safe existing producer can be
connected, retain `FAST_SIGNAL_COVERAGE_PARTIAL`, record the six-class exact
residual and advance only to the existing admission decision. Full Matrix and
automatic FAST policy remain unchanged.

