# Isolated Polygon Authority and runtime-event binding

Status: implementation/integration progress, Mission incomplete. No Production
deployment or user-route execution in this block. No S11, full E2E, seven-second
or 1,000/10,000-user claim.

## Changes and evidence

- Existing Authority owner now accepts an explicitly versioned `v2-polygon`
  standing contract. The fresh lab approval cannot reuse the production v1
  approval. Scope binds actual Docker preflight, Linux namespaces, root mount,
  GRE topology, finite CPU/memory, implementation hashes, exact certification
  registry and target inventory. Expiry is 120 seconds. Production v1 remains
  one member and one transaction; current lab scope is five members and one
  concurrent transaction.
- Actual source-down testing exposed an isolation-check defect: a vanished
  default route was misclassified as an external route. Absence is now allowed;
  an actual external-interface/gateway default still denies admission.
- Controlled health now passes the same audit store to Matrix and invokes the
  actual existing governed-canary executor, not the Planner executable in the
  executor position.
- Actual Matrix `V7_HEALTH_RUNTIME` events were rejected by the certification
  binder's external-only comparison. It now reuses the existing reconcilable
  provenance allowlist. Fresh incident/service/current-registry checks remain.
- Real replay: contract `ctm0fsdpc_5ca66ce13d1dded798657093` active before fault;
  source physical GRE-down detected, selector phase became
  `EXECUTE_CONTROLLED_FAILURE_CUTOVER`; five certification members, ordinary
  scope zero. Target still had 14/14 actual Matrix services. All owned
  containers, image and network were removed and their absence verified.
- Focused regression command covered new lab Authority tests, the complete
  health-fast-deadline test module, four existing standing-policy lifecycle
  tests and runtime-provenance binding denial cases: 50 tests passed in 17.246 s.
  Unit fixtures are not E2E evidence. Independent review was not performed in
  this block; Controller provided architectural direction, not a code-review PASS.
- Subsequent Controller decision admitted truthful COLD lab-only measurement,
  not invented 5m/1h history. Existing `v7-client-speed-api` now performs three
  waves of five concurrent TLS-verified 1 MiB downloads through each real GRE.
  Actual replay at 07:10:36Z: 30/30 payloads verified, 30 MiB total, target stream
  rates 330.004105–1071.062830 Mbps for this short offered load. Both long windows
  remain `NOT_OBSERVED`. This is target transport evidence only; not traffic
  from five switched clients, sustainable bandwidth or E2E. No measured-capacity
  evidence is yet consumed as a Planner/Authority admission grant.

## Exact remaining boundary

The existing target diagnostic returns `no_distinct_controlled_contract_admitted_target`:
the isolated target is reachable and its existing load-policy remaining bound
is nine, but quality current/5m/1h and throughput observations are absent, and
the production availability-first policy is not the new lab Authority. The new
raw prefault payload observations have not yet been bound to admission. These
are distinct missing inputs/coverage, not a failed target network.

Continue in the existing standing Matrix consumer and Planner. Obtain genuine
bounded pre-fault quality/capacity observations, bind approved lab semantics
without inventing history, and carry the entire approved cohort through existing
Candidate/Packet/Lease/Barrier/writer and last-member S11. Do not execute five
independently prepared one-user experiments or restart T0 per member. The source
must stay failed until the real terminal/rollback condition; teardown is not
recovery credit. Production quality floors and ordinary-user routing stay intact.

Actual scheduled re-entry in this same task occurred at 2026-09-07T06:39:26Z;
this proves the restored continuation heartbeat fired, not that the autonomous
engineering Mission or full campaign entry is complete. Architectural questions
and these measured boundaries were sent directly to «Агент Времени».
