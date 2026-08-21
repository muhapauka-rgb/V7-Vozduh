# V5.3 profile/service and DNS fast-suspicion implementation — partial

Date: 2026-08-21 16:43 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Bounded block: `PROFILE_SERVICE_AND_DNS_FAST_SUSPICION_IMPLEMENTATION`

## Result

The existing per-user service profile contract is now accepted by the existing
Matrix shadow-trigger owner. The producer can pass a profile identity instead
of duplicating a service list; the Matrix owner resolves the exact services
from `state/service-preferences.json:users.<profile>.services` and forwards only
that subset to the existing `v7-service-matrix-test` writer.

This is an observation-only extension. It does not enable FAST, change the
15-minute Matrix cadence, add a timer, alter thresholds, call a consumer,
change routes, or move users. Full Matrix remains the fallback.

## Discover → Reuse → Extend → Implement

- Existing profile source: `service-preferences.json` per-user `services` (and
  `required_services` when present).
- Existing owners reused: `tools/v7-egress-diagnose`,
  `tools/v7-service-matrix-refresh-all`, and
  `tools/v7-service-matrix-test`.
- Minimal extension: `--shadow-trigger-profile-user`, mutually exclusive with
  an explicit service list; missing/empty profiles fail closed.
- No new owner, Runtime, timer, queue, watcher, registry, state database,
  truth source, Authority, event, or route action was created.

## Evidence

### Profile/service path

Two different synthetic profiles were exercised with distinct service sets.
The real producer passed the profile identity to the real Matrix receiver; the
receiver resolved the profile and the real Matrix writer persisted exactly
`google,telegram` for the test profile. A missing or empty profile returned
`profile_service_subset_missing_or_empty` before any probe.

### DNS and service-failure producers

Repository/runtime discovery found no existing early, DNS-specific producer and
no existing passive required-service failure signal that can be safely reused
without inventing a new owner or probe contract. Generic HTTP/curl failure is
not DNS evidence and is not promoted to `DNS_FAILURE`; a targeted Matrix check
is confirmation after a suspicion, not an independent early signal.

Therefore the canonical terminal remains:

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

Covered classes remain `HARD_CHANNEL_DOWN`,
`INTERFACE_OR_TUNNEL_PROCESS_ABSENT`, `TUNNEL_UP_INTERNET_DEAD`, and
`TELEGRAM_PERSISTENT_FAILURE`. Exact residual remains:
`REQUIRED_SERVICE_FAILURE`, `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`,
`DNS_FAILURE`, `PARTIAL_CENSORSHIP`, `MULTI_SERVICE_FAILURE`.

## Tests and measurements

- `tests.unit.test_v7_egress_diagnose`: **13/13 passed**.
- Combined fast-signal suite (diagnose, non-Telegram revalidation, coverage):
  **26/26 passed**.
- Existing autoswitch/causal/passive/sentinel focused suite: **209/209 passed**.
- `tests.unit.test_service_failure_episode`: **90 tests, 2 pre-existing CT-M0F
  failures** (`test_ct_m0f_active_service_failure_binding_requires_accounted_live_owner`
  and `test_ct_m0f_standing_source_selection_reuses_controlled_pool_owner`);
  this block does not touch that owner or failure path.
- Polygon path proved producer → real receiver → real Matrix writer with an
  exact profile subset. No production invocation was enabled, so no production
  latency or probe-count gain is claimed.
- `python3 tools/v7-truth-check --continue-omp --json`: `PASS`; authority,
  routing, Runtime, packet execution, automatic FAST enablement and user
  movement all remained unchanged.

## Safety and production effect

Before and after production routes, clients, timers, Matrix cadence, and
automatic FAST authority are unchanged. Unknown, empty, conflicting, or
duplicated service-source inputs fail closed. The full check remains available
as the safe fallback.

## Plan position and next step

This closes the bounded implementation attempt under the current
`FAST_SIGNAL_COVERAGE_PARTIAL` terminal. In the overall plan it is after
`CURRENT V7 BASELINE` → `PROVEN BOTTLENECKS` → `STRONGEST-SYSTEM PATTERNS` →
`CANDIDATE ARCHITECTURES` → `POLYGON + SCALE TOURNAMENT` → `ARCHITECTURE
DECISION`, and before FAST admission or production T0→T11 proof.

Exact next step: use this profile-bound Matrix path in a controlled Polygon
comparison for required-service versus Full checks, while separately deciding
whether an existing owner can provide genuine DNS/passive evidence. If no such
owner exists, retain the five-class residual and proceed to the existing
Full-fallback/production-boundary proof; do not fabricate DNS or service
signals.
