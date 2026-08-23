# V5.3 N5 — pre-ready targets and prepared data plane

Date: 2026-08-23 14:30 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Phase: `N5 PRE_READY_TARGET_AND_PREPARED_DATAPLANE`  
Implementation: `c74db2c822ced8917a766501f6dc9a48dabb5418`  
Deploy: `deploy-z8-14-Updatesystem-c74db2c-20260823T142328`

## Result

N5 is complete. The existing `AutoswitchPlanner.plan` remains the only owner of
target eligibility and ranking. Its existing prepared-class projection now
retains a bounded top-H set (`H <= 4`) of eligible non-canary targets and the
critical-service contract for each target. The adapter does not select a server
manually, create a Candidate/Packet/lease, or persist another source of truth.

The hot projection contains only semantic-class and membership fingerprints;
it does not carry raw member lists. Duplicate target/service contracts are
collapsed globally. The existing V4 Routing Core remains the prepared data-plane
owner.

## Freshness and fail-closed law

The projection binds the existing Matrix, capacity, policy, organisation policy,
egress topology, service preference, safety and operation generations. It also
declares fact-specific age contracts:

| Fact | Maximum age / equality law |
|---|---|
| path liveness | 3 s |
| Telegram when required | 2 s |
| other required service | 10 s |
| target capacity | 30 s |
| policy | current generation equality |
| identity and role | current topology generation equality |

Any generation mismatch returns `PREPARED_CLASS_DECISION_STALE`. Absence of an
official compatible target returns `NO_3S_TARGET_CAPACITY`; it never widens the
search or invents a target during an incident.

## Evidence

- Focused N5/N6/role/health/Routing Core suite: 34 tests passed in 10.349 s.
- 1,000 compatible users collapse to one semantic class and four bounded hot
  target/service contracts; no raw member list is serialized.
- Capacity generation mutation invalidates the projection.
- Missing official target produces `NO_3S_TARGET_CAPACITY`.
- Existing Routing Core cohorts 1/10/100/1,000 produce
  `CLASS_BUCKET_COMMIT_READY`, with zero per-user writes and zero incident-time
  member scans.
- Existing larger V4 evidence remains applicable: 10k/20k/50k preparation,
  50 semantic classes; pure hot commit p95 approximately 0.005 ms; non-hooked
  10k kernel Polygon p95 18.8 ms, max 105 ms, below the 250 ms ceiling.

Production advisory/shadow-only execution after deploy returned:

```text
status = PASS
mode = INCIDENT_ADVISORY_AND_SHADOW_ONLY
prepared classes = 6
hot target/service contracts = 4
projection = PREPARED_CLASS_DECISION_AVAILABLE
freshness = PREPARED_CLASS_DECISION_FRESH
target readiness = PRE_READY_TARGET_SET_PROJECTED
routing mutation = false
users moved = 0
```

This is real owner/consumer evidence, but not permission to switch a client.
The existing Candidate -> Packet -> lease -> barrier -> Apply chain remains
mandatory.

## Runtime and production effect

Local and production hashes match for `v7-users-autoswitch`. Runtime truth is
aligned to the deployed commit. No route changed and no user moved. The role
Runtime is deliberately not activated in N5; `v7-health.service` still starts
the loop without `--role-based-fast`. Activation belongs to N8 after the N7
integrated tournament.

## Limits and next step

N5 proves precomputation, bounded hot validation and official target ownership.
It does not prove the complete causal failure-to-S11 latency. That proof is N7,
where target readiness must run concurrently with source confirmation in every
failure class and phase offset.
