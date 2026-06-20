# DEGRADATION MODEL

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Degradation Definition

A channel is degrading when observed user-facing or service-facing quality worsens while the channel remains present enough to measure.

Observed degradation is not the same as configured capacity pressure. Configured capacity says "policy limit reached." Observed degradation says "quality began to worsen in measured reality."

## Strongest Signals

| Signal | Strength | Why |
| --- | --- | --- |
| Service failures / partial service matrix | High | Direct user-facing service availability symptom. |
| Fail rate increase | High | Direct error/success signal; aligns with SRE error signal. |
| P95 latency increase | High | Captures slow degradation before total failure. |
| Min Mbps collapse | High | Detects floor degradation even if average remains acceptable. |
| Stability decline | High | Detects flapping and runtime/service inconsistency. |
| Avg Mbps decline | Medium-high | Useful but can hide tail/floor problems. |
| Runtime readiness loss | Medium | Often binary or evidence-readiness related. |
| Route readiness issue | Medium | Important for safety/topology, weaker for capacity unless tied to traffic quality. |
| History trend `degrading` | Medium | Helpful summary, must be explained by underlying signals. |

## Proposed Shadow Degradation State

| State | Meaning | Suggested inputs |
| --- | --- | --- |
| `STABLE` | Quality stable at current observed users | no service failure, stable latency, no speed floor collapse |
| `WATCH` | Weak early degradation | one yellow symptom or freshness gap |
| `DEGRADING` | Multiple quality symptoms or clear trend decline | fail rate, latency, min Mbps, stability trend |
| `BROKEN` | Services fail or runtime unavailable | service matrix fail, runtime down, hard service failure |
| `UNKNOWN` | Insufficient samples | missing windows or stale measurements |

## Important Non-Causal Rule

Degradation must not be attributed to user count until V7 has enough observations at different assigned-user levels.

Example:

- `10 users + speed collapsed` is degradation.
- It is not "capacity is 10 users" unless repeated observations show quality stable below 10 and degraded at/above 10 with other causes excluded.

## Audit Verdict

The degradation model is viable as a shadow diagnostic layer. It should be causal only when history proves a repeated relationship between user count and degradation.
