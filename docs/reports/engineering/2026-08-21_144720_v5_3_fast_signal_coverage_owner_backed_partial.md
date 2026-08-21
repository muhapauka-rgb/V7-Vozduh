# V5.3 bounded fast-signal coverage and owner-backed shadow validation

Date: `2026-08-21`
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`
Input terminal: `B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS`
Bounded residual: `FAST_SIGNAL_COVERAGE_AND_OWNER_BACKED_EXECUTION_GAP`

## 1. Final decision

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

The existing V7 owners already provide one safe early-signal path for
Telegram-specific failure. They do not yet provide an early signal for the
other active service/channel failure classes. Those classes still enter through
the ordinary Matrix refresh cadence. The result is therefore partial coverage,
not a universal FAST pass and not a design-unsafe verdict.

No production timer, threshold, route, client, Runtime or automatic FAST
consumer was changed.

## 2. Authoritative intake and reused owners

The CPS terminal remains `B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS`; this report is a
bounded residual result and does not rename Stage E. Reused existing owners:

- `tools/v7-telegram-sentinel` — bounded Telegram TCP signal;
- `tools/v7-service-matrix-test.update_matrix` — canonical Matrix writer,
  episode, persistence and event owner;
- `tools/v7-service-matrix-refresh-all` — existing caller, exact egress/service
  subset forwarding and ordinary cadence owner;
- existing `v7-users-autoswitch` passive consumer — downstream event consumer;
- existing Planner/target/recovery owners — readiness and fail-closed decision.

No new watcher, scheduler, queue, state store, event truth or health owner was
introduced.

## 3. Frozen failure-class coverage

The exact frozen scope was the 16 classes from the bounded prompt. The coverage
classification is:

| Coverage group | Classes | Current earliest signal | Result |
| --- | --- | --- | --- |
| Early covered | `TELEGRAM_PERSISTENT_FAILURE` | Telegram sentinel, configured 14 s grace | `COVERED_FOR_TELEGRAM_ONLY` |
| Cadence-bound | hard channel, interface/process absent, tunnel/Internet, required services, DNS, partial censorship, multi-service, quality, clean recovery | ordinary Matrix refresh; exact subset is available only after trigger | `UNCOVERED_EARLY_SIGNAL` |
| Safety roles | transient, stale/unknown/conflict, target failure, recovery failure, flapping | existing Matrix/Planner/recovery state | `STOP_SAFE_OR_FALLBACK`, not an early-signal gap |

The cadence-bound group remains bounded by the existing caller and canonical
writer, but its earliest signal is still the configured `900 s` refresh. The
existing Matrix persistence contract adds up to `180 s` (or the configured
sample equivalent) before confirmation.

## 4. Owner-backed proof

`tests/unit/test_v5_3_fast_signal_coverage.py` proves, without production
effects:

- exact `--services` is deduplicated by the existing Matrix checker;
- refresh caller forwards the exact subset to the existing checker;
- three failed observations create the existing canonical service episode and
  event, whose consumer remains `tools/v7-users-autoswitch`;
- Telegram sentinel data is translated into the same canonical Matrix service
  shape and retains its service-specific owner;
- safety classes produce no fast action;
- fast probe scale is one sentinel observation per egress, not every service;
- the full 16-class frozen scope is deterministic.

Focused result: `7/7` new tests passed.

The existing owner-backed implementation is therefore sufficient for the
covered Telegram class and for bounded confirmation after a Matrix trigger. It
does not contain a safe trigger surface for required-service or generic
channel/service failure before cadence.

## 5. Causal timing bounds (seconds)

These are configured/owner-backed bounds, not Python wall-clock measurements.

| Scenario | Signal owner | Failure→signal | Signal→T0 | Failure→T0 | T0→T11 | Full barrier |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Telegram persistent failure | Telegram sentinel → Matrix | 14 | 0 | **14** | 0.024 | no; DEEP async/fallback |
| Required service failure | Matrix refresh → Matrix | 900 | 180 | **1080** | 85.699 | yes until new trigger proven |
| Hard channel down | Matrix refresh → Matrix | 900 | 180 | **1080** | 85.699 | yes until new trigger proven |
| DNS / partial / quality | Matrix refresh → Matrix | 900 | 180 | **1080** | 85.699 | yes/fallback |
| Stale/unknown/conflict | Matrix + Planner | UNKNOWN | UNKNOWN | UNKNOWN | STOP_SAFE | STOP_SAFE |

The previous causal B+C model remains valid as a design proof for a future
owner-backed trigger, but this block does not promote that model to current
coverage. The owner-backed implementation reproduces the fast result only for
Telegram.

## 6. Mature-system mapping

| V7 gap | Mature mechanism | Existing V7 action | Disposition |
| --- | --- | --- | --- |
| Telegram liveness | Envoy passive escalation / BFD-like cheap liveness | Telegram sentinel into Matrix episode | Reuse; already covered |
| Required service | HAProxy fall/rise and active service checks | Matrix exact subset + existing persistence | Reuse primitive; trigger gap remains |
| Hard channel/interface | BFD/Cisco liveness separation | Matrix interface/path evidence | Adapt only after owner trigger is proven |
| Quality degradation | Fortinet Performance SLA | Matrix quality/deep evidence | Do not treat as hard-down; keep deep/fallback |
| Target readiness | Google/HAProxy/Envoy eligibility | existing Planner readiness | Reuse; stale/unknown remains fail-closed |
| Recovery | HAProxy rise / Envoy recovery | existing Matrix recovery episode | Reuse asymmetric recovery; no fast re-admission yet |

Vendor numeric defaults were not copied.

## 7. Full Matrix role and target readiness

Full Matrix remains:

- `ASYNC_DEEP_CONFIRMATION` for Telegram fast signal;
- `REQUIRED_BEFORE_T0` or `REQUIRED_BEFORE_ACTION` for classes without a
  trustworthy early trigger;
- `DISAGREEMENT_FALLBACK` for stale, conflicting or partial evidence;
- `BACKGROUND_STATE_REFRESH` for quality, capacity and broad service detail.

Existing target readiness remains a separate Planner concern. No stale target
was accepted to make the timing look better; unknown generation, policy,
capacity or readiness remains `STOP_SAFE`.

## 8. Passive value and scale

Passive escalation has measurable value only for Telegram in the current owner
set: it reduces the modelled signal wait from `900 s` to `14 s` and permits the
governed transaction without a universal Full barrier. It must not be used as a
generic proof of channel or application health.

At 7/50/100/1,000 egress boundaries, the current fast policy is one Telegram
sentinel observation per egress. Full fallback remains `14 × egress_count`
service observations. The bounded policy therefore does not become
`every-service × every-egress × every-few-seconds`.

## 9. Policy-change register

| Rule | Current purpose/cost | Safe conclusion | Admission needed |
| --- | --- | --- | --- |
| 15-minute-only discovery | ordinary refresh covers all services; worst wait `900 s` | unresolved for non-Telegram classes | existing-owner trigger proof, then shadow/controlled admission |
| universal 180 s persistence | protects against false failure | retain for cadence-bound classes; make role-specific only with FP/FN proof | per-class Polygon evidence |
| Full-DEEP-before-action | safety for ambiguous evidence | bypass only for fresh Telegram-specific bounded evidence | owner-backed scenario barrier proof |
| target revalidation timing | prevents stale target use | reuse current readiness; no stale shortcut | current generation/policy/capacity evidence |
| passive escalation | early Telegram signal | keep service-specific, do not generalize | separate admission per signal family |

## 10. Verification and limitations

Passed:

- new coverage harness: `7/7`;
- existing operator/subset caller tests: `6/6`;
- existing Telegram sentinel lock/bridge tests: `14/14`;
- existing causal revalidation: `8/8`;
- controlled Matrix comparison: `6/6`;
- `tools/v7-truth-check --continue-omp --json`: `PASS`.

The broader `test_service_failure_episode` suite passed `90/92`; two legacy
CT-M0F controlled-source/binding tests still fail their existing `result["ok"]`
assertion. They are outside this signal-coverage path and were not changed or
used as evidence for a FAST decision.

No route mutation, Runtime mutation, user movement, packet/lease execution or
Authority expansion occurred.

## 11. Canonical conclusion and residual

The covered Telegram path is owner-backed and safe to retain. The following
classes remain the single bounded residual:

```text
HARD_CHANNEL_DOWN
INTERFACE_OR_TUNNEL_PROCESS_ABSENT
TUNNEL_UP_INTERNET_DEAD
REQUIRED_SERVICE_FAILURE
OTHER_PROFILE_REQUIRED_SERVICE_FAILURE
DNS_FAILURE
PARTIAL_CENSORSHIP
MULTI_SERVICE_FAILURE
LATENCY_LOSS_JITTER_DEGRADATION
CLEAN_RECOVERY
```

They require a proven existing-owner trigger or must retain cadence/full
fallback. No generic FAST scheduler is allowed.

Exact next step: discover whether an existing Matrix/health caller can safely
trigger a bounded required-service observation for the above residual classes;
if not, design one minimal shadow-only extension of that existing trigger
surface, then repeat this same frozen 16-class matrix before any production
admission.
