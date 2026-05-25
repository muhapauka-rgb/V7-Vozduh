# V7 Phase 3 - Service Matrix Maturity

## Purpose

Service matrix must measure usable service quality, not only whether a port answers.

Existing implementation already checks HTTP services, Telegram TCP endpoints, route-class fitness, and per-egress status. Phase 3 formalizes the platform-grade target.

## Service Coverage

Required service dimensions:

- Telegram;
- YouTube;
- Instagram;
- WhatsApp;
- DNS;
- HTTPS;
- TCP reachability;
- latency;
- MTU;
- throughput;
- reconnect quality.

## Quality Dimensions

Service result should distinguish:

- reachable;
- application/CDN limited but path reachable;
- degraded;
- blocked/down;
- not started;
- stale/unknown.

## Route Class Fitness

Service matrix must answer:

- is this egress fit for `GLOBAL_FAST`;
- is this egress fit for `GLOBAL_STABLE`;
- is this egress fit for `DIRECT_RU`;
- is this egress fit for `TRUSTED_RU_SENSITIVE`;
- which required service failed;
- why the fitness is not OK.

## Staleness

Old measurements must be visible as stale and must not be presented as current health.

Suggested staleness:

- under 5 minutes: fresh;
- 5-30 minutes: usable but mark age;
- over 30 minutes: stale warning;
- over 2 hours: unknown unless backed by other fresh evidence.

## Operator View

Summary:

- healthy/degraded services count;
- impacted route classes;
- worst affected egress;
- suggested safe action.

Drill-down:

- per-service HTTP/TCP samples;
- latency/first-byte;
- endpoint failures;
- raw command output if needed.

## Phase 3 Boundary

This document does not add service probes. It defines maturity expectations for existing and future matrix data.
