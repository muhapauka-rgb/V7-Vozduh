# V7 Phase 4 Autoswitch Decision Model

## Purpose

Autoswitch is a stability preservation engine, not a fastest-route optimizer.

Its job is to keep user-visible internet access stable while preserving:

- deterministic routing;
- route-class policy;
- kill switch guarantees;
- operator trust;
- bounded and reversible behavior.

## Decision Inputs

Autoswitch decisions MAY consider these inputs:

- service availability and service-specific degradation;
- degradation duration and persistence;
- packet loss and latency quality;
- reconnect frequency and client instability;
- historical egress reliability;
- route-class compatibility;
- client experience signals;
- egress load and capacity limits;
- cooldown and freeze state;
- operator policy and organization policy;
- quarantine and maintenance state.

Autoswitch MUST NOT switch only because one route is slightly faster.

## State Hierarchy

Autoswitch must treat these layers as separate concepts:

- desired assignment: registry and policy intent;
- observed quality: service matrix, Telegram sentinel, reconnect state, quality summary;
- runtime safety: route verification, kill switch compatibility, quarantine state;
- effective decision: the bounded plan that may be applied only after gates pass.

## Decision Pipeline

1. Collect evidence from state files and runtime summaries.
2. Classify the issue as service, route-class, egress, client, direct routing, or trusted RU degradation.
3. Apply hard safety gates:
   - target enabled;
   - target not quarantined;
   - route class compatible;
   - organization policy allows target;
   - capacity and load bounds respected;
   - cooldown and freeze gates satisfied.
4. Score candidates using stability-first weighting.
5. Assign confidence:
   - low: weak or conflicting evidence;
   - medium: persistent degradation with acceptable target;
   - high: multi-signal degradation with stable verified target.
6. Select a bounded migration set.
7. Produce an explainable plan.
8. If applied, audit before/after and verify result.

## Required Explanation

Every planned or applied switch must include:

- affected user or group;
- source egress;
- target egress;
- route class;
- service impact;
- degradation evidence;
- cooldown/freeze status;
- confidence;
- rejected candidates;
- rollback context.

## Forbidden Decision Patterns

Autoswitch MUST NOT:

- chase transient latency changes;
- mass-migrate users without high confidence;
- switch around route-class policy;
- use quarantined or unverified egress;
- silently bypass direct or trusted RU safety rules;
- hide why a switch was planned or applied.

