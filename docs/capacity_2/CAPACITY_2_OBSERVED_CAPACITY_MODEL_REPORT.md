# CAPACITY.2 Observed Capacity Model Report

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Date: 2026-06-20
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

No runtime, planner, assignment, governance, autoswitch, UI, score, formula, database, or capacity-limit changes were made.

## 1. Current Model

Current capacity is assignment/load safety:

- assigned users vs soft/hard/failover-hard limits;
- dynamic limits from active users and healthy working pool;
- explicit per-egress caps when present;
- planner gates that restrict planned/failover movement.

It is not physical tunnel capacity.

Artifact: `docs/capacity_2/CURRENT_CAPACITY_MODEL.md`

## 2. Limit Origin

The active limit model was introduced across guarded autoswitch/dynamic-load work and later locked by CAPACITY.1 / ADR-009.

Key commits found by history search:

- `152c1ce5 Add guarded VPN autoswitch dynamic load policy`
- `9c36f0f6 Add POOL promotion equivalence rule`
- `3f699567 Establish capacity semantics reference`

Artifact: `docs/capacity_2/LIMIT_ORIGIN_REPORT.md`

## 3. Observable Signals

V7 already observes:

- assigned users;
- service matrix;
- avg/min Mbps;
- p95 latency;
- fail rate;
- stability;
- runtime readiness;
- route readiness;
- history windows;
- planner candidate reasons;
- intelligence/shadow evidence patterns.

Artifact: `docs/capacity_2/OBSERVABLE_SIGNAL_INVENTORY.md`

## 4. Degradation Model

Strongest degradation signals:

1. service failures / partial service matrix;
2. fail rate increase;
3. p95 latency increase;
4. min Mbps collapse;
5. stability decline;
6. avg Mbps decline.

Artifact: `docs/capacity_2/DEGRADATION_MODEL.md`

## 5. Observed Capacity Theory

V7 can infer practical capacity only by observing quality at different user-count levels.

Current evidence proves V7 can observe users and quality together. It does not yet prove per-channel capacity curves.

Artifact: `docs/capacity_2/OBSERVED_CAPACITY_THEORY.md`

## 6. Industry Review

Industry pattern: static limits are not enough. Successful systems combine configured bounds with observed metrics, health, demand, latency/errors, and conservative control loops.

Sources reviewed:

- Google SRE capacity planning and golden signals.
- AWS target tracking scaling.
- Kubernetes HPA observed metrics.
- Cloudflare load balancing health/traffic steering.

Artifact: `docs/capacity_2/INDUSTRY_CAPACITY_REVIEW.md`

## 7. Shadow Model

Recommended model:

`Observed Capacity Shadow`

Allowed:

- observe;
- measure;
- learn;
- record;
- recommend future review.

Forbidden:

- planner influence;
- assignment influence;
- runtime execution;
- autoswitch influence;
- automatic limit changes.

Artifact: `docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md`

## 8. Data Gaps

Main missing data:

- causal load-step history;
- per-channel user traffic demand;
- packet loss/reconnect trend;
- tunnel ownership metadata;
- controlled promotion/demotion samples;
- confidence per observation.

Artifact: `docs/capacity_2/DATA_GAP_ANALYSIS.md`

## 9. Safety Model

Safe progression:

```text
Observe
  |
  v
Learn
  |
  v
Recommend
  |
  v
Future planner integration only after separate approval
```

Artifact: `docs/capacity_2/SAFETY_MODEL.md`

## 10. Canonical Updates

Stable conclusions were moved into:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-011-observed-capacity-model.md`

## 11. Answers

| Question | Answer |
| --- | --- |
| Should V7 continue using only static limits? | No. Static limits remain active safety rails, but V7 should learn observed practical capacity in shadow mode. |
| Should V7 learn real capacity from observations? | Yes, because V7 often does not own third-party tunnels and already observes quality symptoms. |
| Can V7 estimate practical capacity without owning the tunnel? | Yes, with confidence limits and enough repeated observations. |
| Should observed capacity affect planner now? | No. Shadow/advisory only until separate approval. |
| Future architecture | Derived snapshot-only Observed Capacity Shadow, reusing quality summary, service matrix, runtime readiness, history, and assigned users. |

## 12. Tests Run

Pre-audit:

- `tools/v7-truth-check --all --json`: PASS / `FULLY_ALIGNED`
- `tools/v7-convergence-status --json`: PASS / `ALIGNED`

Final verification is recorded after commit/push.

## 13. Final Verdict

Verdict: `OBSERVED_CAPACITY_VIABLE`

Observed capacity is viable as a shadow/advisory model. Static limits remain preferred for active planner safety until observed capacity is certified by future evidence and a separate governed implementation.
