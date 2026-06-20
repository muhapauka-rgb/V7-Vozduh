# OBSERVED CAPACITY THEORY

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Question

Can V7 infer practical capacity from observations?

Answer: Yes, but only in shadow/advisory mode until enough evidence exists.

## Theory

Observed practical capacity is the highest user count at which a channel remains stable under measured service, speed, latency, runtime, and history signals.

It is not:

- a replacement for `soft_limit` / `hard_limit`;
- a physical provider bandwidth number;
- a planner hard gate;
- a one-sample conclusion.

## Evidence Needed

V7 needs observations like:

| Users | Quality | Interpretation |
| ---: | --- | --- |
| 5 | stable | channel works at 5 |
| 10 | stable | channel works at 10 |
| 15 | stable | channel works at 15 |
| 18 | degrading | possible practical threshold near 15-18 |
| 18 again | degrading | stronger evidence |
| 20 | broken | upper unsafe evidence |

## Existing Evidence

Current production evidence proves V7 can observe user count and quality together. It does not yet prove a stable capacity curve for each channel.

Examples from CAPACITY.1:

- `vless`: 11 users, good observed speed/stability, `HARD_FULL` assignment state.
- `awg3`: 8 users, good observed speed/stability, `HARD_FULL` assignment state.
- `awg0`: 0 users, good observed speed/stability, `OK` assignment state.

This shows static assignment limits and observed quality can disagree. It does not prove which channel has the higher practical maximum.

## Confidence Model

| Confidence | Requirement |
| --- | --- |
| `LOW` | one or few samples; no user-count variation |
| `MEDIUM` | stable quality across repeated windows at current user level |
| `HIGH` | repeated stable/degraded transitions across multiple user levels |
| `CERTIFIED` | controlled rollout/promotion evidence plus rollback-safe history |

## Audit Verdict

Observed capacity is viable. Static limits should remain the active safety model while V7 learns practical capacity in shadow mode.
