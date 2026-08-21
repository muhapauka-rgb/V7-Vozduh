# V5.3 non-Telegram trigger revalidation and exact residual

Date: `2026-08-21`
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`
Input terminal: `FAST_SIGNAL_COVERAGE_PARTIAL`
Bounded residual: `NON_TELEGRAM_FAST_SIGNAL_TRIGGER_INTEGRATION`

## 1. Result

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

The owner scan found an existing early signal for hard local channel failure:
`v7-egress-diagnose` writes the existing diagnose state, `v7-health` merges it,
and the already active `v7-users-autoswitch` caller reads it and can produce
`confirmed_current_channel_failure`. The same path is safe-by-default and does
not itself apply a route while automatic FAST remains held.

Telegram remains covered by its existing sentinel. No safe existing producer
was found for application/service, DNS, Internet-behind-tunnel, quality or
clean-recovery triggers. Those classes still begin with the ordinary 15-minute
Matrix refresh and retain the existing Full/persistence fallback.

No production timer, threshold, route, client, Runtime, Authority or automatic
FAST consumer was changed.

## 2. Existing owner and caller chain

| Function | Existing owner/caller | Evidence | Finding |
| --- | --- | --- | --- |
| local transport/process observation | `tools/v7-egress-diagnose` | emits `diagnose_reason`/`diagnose_severity`, including `interface_down_or_missing` | usable early source for hard local failure |
| state projection | `systemd/v7-health.service` | 30-second loop includes diagnose and `v7-state-merge` | existing producer cadence, no new timer |
| governed read/decision | `systemd/v7-users-autoswitch.timer` -> `v7-governed-canary-dry-run-cycle` -> `tools/v7-users-autoswitch` | active 20-second caller; existing `_current_channel_failure_evidence` | accepts only fresh/aging hard evidence and affected scope |
| canonical service evidence | `tools/v7-service-matrix-refresh-all` -> `tools/v7-service-matrix-test` | exact `--services` forwarding and existing persistence/event writer | available after a Matrix trigger, not an early generic producer |
| Telegram passive signal | `tools/v7-telegram-sentinel` | existing Matrix bridge and consumer wake | service-specific early path already covered |
| quality/history | `tools/v7-egress-quality-compact` | writes quality summary/ring under Matrix lock | evidence-only; no wake/trigger |

The draft `systemd/drafts/v7-autoswitch-planner.*` was inspected but not
activated. It consumes already-written service-failure events and therefore
cannot create a pre-Matrix trigger.

## 3. Frozen 17-class coverage

| Group | Classes | Earliest owner-backed signal | Status |
| --- | --- | --- | --- |
| early signal available | `HARD_CHANNEL_DOWN`, `INTERFACE_OR_TUNNEL_PROCESS_ABSENT`, `TELEGRAM_PERSISTENT_FAILURE` | diagnose+health+existing autoswitch; Telegram sentinel | `COVERED_IN_SHADOW; no FAST admission` |
| cadence-bound residual | `TUNNEL_UP_INTERNET_DEAD`, `REQUIRED_SERVICE_FAILURE`, `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`, `DNS_FAILURE`, `PARTIAL_CENSORSHIP`, `MULTI_SERVICE_FAILURE`, `LATENCY_LOSS_JITTER_DEGRADATION`, `CLEAN_RECOVERY` | ordinary Matrix refresh / exact subset | `UNCOVERED_EARLY_SIGNAL` |
| safety-only roles | `TRANSIENT_FALSE_ALARM`, `STALE_OR_UNKNOWN_STATE`, `CONFLICTING_GENERATION`, `TARGET_UNAVAILABLE`, `CAPACITY_OR_POLICY_DENIAL`, `FAIL_RECOVER_FAIL` | existing Matrix/Planner/recovery gates | `STOP_SAFE_OR_FALLBACK` |

`COVERED_IN_SHADOW` is not a production approval. It means the signal and its
real existing consumer are present and bounded; it does not permit a route or
client change.

## 4. Timing and probe budget

Configured/owner-backed bounds, not a production wall-clock claim:

| Failure class | Failure -> first signal | Signal -> existing read/decision | Current production implication |
| --- | ---: | ---: | --- |
| hard local channel/process | up to 30 s health projection + up to 20 s autoswitch caller | same existing caller; fresh/aging gate | early evidence exists; automatic FAST held |
| Telegram persistent | 14 s sentinel threshold | existing Matrix episode/consumer | bounded early path; no automatic FAST |
| service/DNS/Internet/quality/recovery | up to 900 s Matrix cadence | existing persistence up to 180 s | Full/persistence remains required |
| stale/unknown/conflict/target/policy | unknown by design | fail closed | `STOP_SAFE` |

The fast local path does not multiply probes: it reads existing state. For
7/50/100/1,000 egresses it adds zero network probes; Telegram remains one
sentinel observation per egress; cadence-bound classes remain the existing Full
budget until a new trigger is proven.

## 5. Confirmation, disagreement and target readiness

- Hard local evidence is accepted only for `FAIL` + exact reason
  `interface_down_or_missing`, affected users > 0 and state freshness `FRESH`
  or `AGING`.
- Unknown, stale, conflicting generation, target unavailability and policy or
  capacity denial remain fail-closed.
- Existing Matrix persistence and exact required-service subset remain the
  canonical confirmation path for application failures.
- Full Matrix remains the disagreement/fallback path; no short result can
  authorize a route by itself.

## 6. Mature-system reuse decision

| Proven V7 need | Mature pattern | V7 disposition |
| --- | --- | --- |
| cheap hard liveness | BFD/Cisco object tracking separation | reuse existing diagnose signal; do not copy thresholds |
| service confirmation | HAProxy fall/rise, Envoy active checks | reuse Matrix persistence/subset; trigger gap remains |
| passive escalation | Envoy/HAProxy passive escalation | retain Telegram-only owner path |
| quality degradation | Fortinet Performance SLA | keep as quality evidence, never hard-down shortcut |
| target readiness | Google/HAProxy/Envoy eligibility gates | reuse existing Planner readiness and fail-closed gates |
| recovery/re-admission | rise/hysteresis patterns | retain existing recovery owner; no fast clean-recovery trigger yet |

## 7. Verification

Passed:

- new owner/trigger revalidation: `4/4`;
- previous fast-signal coverage harness: `7/7`;
- existing autoswitch owner path: `3/3` targeted tests;
- egress diagnose: `7/7`;
- causal/passive/sentinel tests: `28/28`;
- `tools/v7-truth-check --continue-omp --json`: `PASS`.

The full service-failure episode suite remains `90/92`; the same two legacy
CT-M0F controlled-source/binding tests fail their existing `result["ok"]`
assertion. They are outside this residual and were not changed.

The local Matrix comparison test could not bind its loopback test server in
this sandbox (`PermissionError: Operation not permitted`); no production
effect occurred and the already recorded `6/6` controlled comparison remains
historical evidence.

## 8. Canonical conclusion and exact next step

Covered in shadow:

```text
HARD_CHANNEL_DOWN
INTERFACE_OR_TUNNEL_PROCESS_ABSENT
TELEGRAM_PERSISTENT_FAILURE
```

Exact residual:

```text
TUNNEL_UP_INTERNET_DEAD
REQUIRED_SERVICE_FAILURE
OTHER_PROFILE_REQUIRED_SERVICE_FAILURE
DNS_FAILURE
PARTIAL_CENSORSHIP
MULTI_SERVICE_FAILURE
LATENCY_LOSS_JITTER_DEGRADATION
CLEAN_RECOVERY
```

Next step in the V5.3 plan: use the existing Matrix/health owner to design and
run a shadow-only bounded trigger for the exact residual above, or prove that
no existing signal can safely trigger it. Then rerun the same 17-class Polygon,
causal-timing, fallback and scale comparison. Until that result, Full Matrix
remains the safe baseline and automatic FAST remains held.

