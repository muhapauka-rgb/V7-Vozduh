# V7 Vozduh - BLOCK 2 Health Semantics Unification & Operator Truth Model

Дата выполнения: 2026-05-23, live VPS `195.2.79.116`.

Цель: выстроить единый operator-facing truth model без изменения datapath, routing, route classes, Trusted RU/Gosuslugi или autoswitch code.

## Scope Guardrails

Не изменялось:

- kill switch;
- nftables;
- routing tables;
- route classes;
- direct/RU policy;
- TRUSTED_RU / Gosuslugi behavior;
- autoswitch planner;
- service matrix probes;
- Telegram sentinel timer;
- user registry structure.

Изменено:

- локальный и live read-only helper `v7-observability-summary`.

Назначение изменения:

- читать существующие state files;
- нормализовать statuses в один operator-facing язык;
- показывать source authority hierarchy;
- показывать contradiction catalog;
- не запускать probes;
- не писать runtime state;
- не менять routing.

## Full Health-Source Map

| Source | Writer | Reader | Cadence | Authority | Runtime critical |
|---|---|---|---|---|---|
| `/etc/v7/policy.json` | operator/admin | autoswitch/admin | on change | hard policy authority | yes |
| `/etc/v7/org-egress-policy.json` | operator/admin | autoswitch/admin | on change | tenant policy authority | yes |
| `/opt/v7/egress/state/service-matrix.json` | `v7-service-matrix-test`, `v7-service-matrix-refresh-all`, `v7-telegram-sentinel` | autoswitch/admin/observability | timer + ad-hoc | supporting live service health | yes |
| `/opt/v7/egress/state/telegram-sentinel.json` | `v7-telegram-sentinel` | autoswitch/admin/observability | fast timer | advisory fast Telegram signal | yes |
| `/opt/v7/egress/state/egress-quality-summary.json` | `v7-egress-quality-compact` | autoswitch/admin/observability | periodic compaction | supporting historical quality | no |
| `/opt/v7/egress/state/autoswitch-safety.json` | `v7-users-autoswitch` | autoswitch/admin/observability | on autoswitch run | anti-flap authority | yes |
| `/opt/v7/egress/state/client-reconnect-state.json` | autoswitch/client observers | autoswitch/admin/observability | on observation | supporting client experience signal | no |
| `/opt/v7/egress/state/egress-load-summary.json` | optional/future | admin/observability | optional | supporting capacity signal | no |
| `v7-killswitch-check` | live Linux runtime check | operator/admin | manual/read-only | datapath safety verification | yes |
| `v7-user-route-check` | live Linux runtime check | operator/admin | manual/read-only | route correctness verification | yes |
| `v7-provisioning-reconcile-check` | live Linux runtime check | operator/admin | manual/read-only | runtime consistency verification | yes |

## Authority Hierarchy

Proposed and now reflected in `v7-observability-summary`:

1. Hard policy: `policy.json`, `org-egress-policy.json`
   - hard limits and eligibility;
   - never advisory;
   - must not be overridden by service noise.

2. Safety: `autoswitch-safety.json`
   - anti-flap, freezes, target blocks, quarantine memory;
   - authoritative for movement suppression.

3. Live service health: `service-matrix.json`
   - broad current service usability;
   - supporting input for routing decisions.

4. Fast service signal: `telegram-sentinel.json`
   - fast Telegram-specific signal;
   - advisory after Block 1.1;
   - should influence severity/scoring, not directly execute apply.

5. Capacity: autoswitch dynamic load / optional `egress-load-summary.json`
   - capacity and overload signal;
   - should not override policy or safety.

6. Client experience: `client-reconnect-state.json`
   - supporting user-impact signal;
   - should not be a single-signal trigger.

7. Historical quality: `egress-quality-summary.json`
   - confidence modifier;
   - not sole live blocker.

8. Runtime verification:
   - `v7-killswitch-check`;
   - `v7-user-route-check`;
   - `v7-provisioning-reconcile-check`.

## Live Contradiction Catalog

Live summary result after deployment:

```json
{
  "status": "unstable",
  "severity": "critical",
  "affected_users": 0,
  "attention_incidents": 6,
  "autoswitch_state": "degraded",
  "degraded_channels": 2,
  "trusted_ru_state": "unknown"
}
```

Detected contradictions:

1. Capacity summary missing
   - Sources: `egress-load-summary.json`, autoswitch internal `dynamic_load`.
   - Live state: persisted load summary is missing.
   - Impact: operator cannot independently verify overload semantics.
   - Severity: warning.

2. Historical quality exists for non-enabled/missing egress `awg2`
   - Sources: `egress-quality-summary.json`, `egress.registry`.
   - Impact: archived/legacy history can be mistaken for live health.
   - Severity: info.

3. Historical quality exists for non-enabled/missing egress `amneziawg-1779227510-8c08e7`
   - Same risk as above.
   - Severity: info.

4. `vless`: historical quality degraded while live service matrix is not blocked
   - Evidence: low stability around `0.256-0.276`.
   - Impact: autoswitch/operator may reject a usable channel or overstate degradation.
   - Severity: warning.

5. `awg0`: historical quality degraded while live service matrix is not blocked
   - Evidence: low stability around `0.295-0.308`.
   - Impact: same as above.
   - Severity: warning.

6. `openvpn-1779388847-d2ad7c`: historical quality unstable while live service matrix is not blocked
   - Evidence: historical fail rate near `1.000`, penalty near `100`.
   - Impact: historical signal can dominate a currently reachable service state.
   - Severity: critical.

7. `wireguard-1779454504-c43409`: historical quality unstable while live service matrix is not blocked
   - Evidence: historical fail rate near `1.000`, penalty near `100`.
   - Impact: same as above.
   - Severity: critical.

8. Trusted/direct RU diagnostics unavailable
   - Source: missing `direct-ru-diagnostics.json`.
   - Impact: operator truth for Trusted RU must remain `unknown`, not `healthy`.
   - Severity: warning.

## Live Group Summary

From `v7-observability-summary --pretty`:

- `channels`: `unstable`
  - reason: historical quality unstable on 2 egress.
- `services`: `degraded`
  - reason: degraded services on 6 egress.
- `autoswitch`: `degraded`
  - reason: 16 users frozen by anti-flap safety.
- `routing`: `degraded`
  - reason: path benchmark needs attention on 1 egress.
- `trusted_ru`: `unknown`
  - reason: trusted/direct RU diagnostics unavailable.
- `users`: `healthy`
  - reason: 16 active users tracked.
- `provisioning`: `healthy`
  - reason: registry assignments explainable at summary level.
- `security`: `healthy`
  - reason: state sources parsed.

## Autoswitch Signal Influence Map

Current autoswitch reads:

- `policy.json`
  - switch mode;
  - cooldown;
  - max planned/failover bounds;
  - quality/load/reconnect/safety policies.

- `org-egress-policy.json`
  - org-level overrides.

- `service-matrix.json`
  - service rows;
  - route class fitness;
  - service scoring.

- `telegram-sentinel.json`
  - Telegram-specific state;
  - `blocked`, `matrix_status`, `bad_for_seconds`, `score`, `reason`.

- `egress-quality-summary.json`
  - historical fail rate;
  - stability;
  - trend;
  - quality history score.

- `autoswitch-safety.json`
  - user freezes;
  - blocked targets;
  - egress quarantine;
  - switch counters.

- `client-reconnect-state.json`
  - reconnect observations.

- registry state:
  - current user assignments;
  - enabled egress;
  - capacity fields;
  - manual/reserve flags.

Dangerous interaction still present:

- Telegram sentinel is no longer direct apply, but autoswitch timer still sees sentinel degradation.
- After Block 1.1, `v7-users-autoswitch.timer` still produced 6 bounded moves from `1 -> awg3`.
- That means self-healing is preserved, but health ambiguity can still create movement pressure.

## Historical vs Live Signal Model

Required semantics:

- Live hard block:
  - current service/routing/runtime failure;
  - may prevent routing if verified.

- Live degradation:
  - current service reduced but usable;
  - may increase severity and reduce score.

- Historical instability:
  - previous fail rate / quality trend;
  - confidence modifier only.

- Transient failure:
  - short timeout / grace state;
  - should not trigger migration alone.

- Persistent failure:
  - multi-signal sustained degradation;
  - eligible for bounded autoswitch.

Current misuse risk:

- `egress-quality-summary.json` can make a live-usable egress look unusable because historical fail rate is high.
- Missing capacity summary means operator cannot see why autoswitch considers load OK or full.
- Missing Trusted RU diagnostics must remain unknown; showing it as healthy would violate operator clarity.

## Minimal Safe Changes Applied

Updated local:

```text
tools/v7-observability-summary
```

Installed live:

```text
/usr/local/bin/v7-observability-summary
```

Behavior added:

- health source map;
- authority hierarchy;
- contradiction catalog;
- normalized operator statuses:
  - `healthy`
  - `degraded`
  - `unstable`
  - `overloaded`
  - `blocked`
  - `quarantined`
  - `maintenance`
  - `recovering`
  - `unknown`
- historical-vs-live separation;
- non-enabled quality history detection;
- missing capacity summary detection;
- Trusted RU unknown preservation.

No runtime actions are executed by the tool.

## Runtime Verification

Executed after change:

- `v7-observability-summary --pretty`: OK
- `v7-killswitch-check`: `OK`
- `v7-user-route-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

Switch-history observation:

- total switches: `1164`
- last switch: `2026-05-22T21:51:17.461211+00:00`
- after Block 1.1 cut (`2026-05-22T21:43:40Z`): `6` switches
- all observed after-cut switches: `1 -> awg3`

Interpretation:

- Sentinel no longer directly applies.
- Autoswitch timer still applies bounded moves.
- Current movement is no longer a storm, but semantics still need policy-level persistence refinement.

## Operator Truth Model

Recommended compact display:

```text
System: unstable
Autoswitch: degraded, anti-flap protecting 16 users
Channels: 2 historically unstable
Services: degraded on 6 egress
Capacity: unknown to operator, dynamic internally
Trusted RU: unknown
Recent movement: bounded 1 -> awg3 failovers
Datapath checks: OK
```

This avoids raw telemetry walls while giving the operator the real state.

## Remaining Instability Risks

1. Autoswitch still has movement authority via timer.
2. Historical quality can still strongly influence candidate rejection.
3. Capacity is computed internally but not persisted as an operator-verifiable source.
4. Trusted RU remains unknown in summary until explicit diagnostics.
5. Service matrix `WARN` is broad and can be noisy if HTTP-limited services are treated like hard degradation.
6. Users are still anti-flap protected from prior storm, which means the system is recovering, not cleanly healthy.

## Next Engineering Priorities

1. Persist autoswitch dynamic load summary as read-only operator state.
2. Treat historical quality as confidence modifier unless paired with live service degradation.
3. Add same-pair oscillation guard for `A -> B -> A`.
4. Make service matrix severity clearer:
   - hard block;
   - degraded;
   - HTTP-limited/advisory;
   - unknown.
5. Add compact autoswitch incident summary:
   - recent switches;
   - frozen users;
   - current guardrails;
   - latest moved pair.

## Final Verdict

BLOCK 2 established a single operator truth model without touching datapath. The platform now has a read-only summary that explicitly separates hard policy, safety authority, live service state, fast Telegram advisory signal, historical quality, client experience and unknown areas.

V7 is calmer and more explainable than before Block 2, but autoswitch is not fully production-mature until historical/live signal misuse and capacity visibility are tightened.
