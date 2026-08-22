# V5.3 controlled-source readiness and Polygon revalidation

Date: 2026-08-22 (MSK)  
Scope: continue the existing `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION` track. This is one logical readiness block, not a new Program, owner, Runtime, Matrix, Planner or source of truth.

## Purpose

Prepare the next lawful real controlled observation for the existing chain
`two FAST observations -> Matrix -> T0 -> … -> T11`, while preserving the
Full Matrix fallback and never involving ordinary customers merely to make a
test happen.

## What was observed

| Check | Result | Meaning |
| --- | --- | --- |
| Existing Matrix lifecycle | `WORKING`; Matrix and refresh summary were fresh at observation time | Matrix is not the current blocker. |
| Existing foreground health owner | active | FAST observation remains observation-only and does not move anyone. |
| Empty dedicated source `1` | `0/14` observation-only Matrix probes passed | It is not a safe baseline: the existing diagnosis is `curl_failed_and_handshake_stale`. |
| Existing `EXECUTION_ONLY` source | zero ordinary users, but five certification identities and an expired/misaligned prior reservation | It cannot be reclassified as the exact one-user source. |
| Selected dedicated draft | native admin pool preview returned `duplicate_interface_config` | It is a duplicate of the unhealthy source, not an independent recovery path. It was not materialized. |

All counts above are aggregate only. No customer identity, route or raw
configuration was copied into this report.

## Actions and safety result

1. Reused `v7-users-autoswitch --controlled-source-topology-diagnostic` with
   the existing one-user validation profile. It rejected every shared ordinary
   source and the multi-identity service source.
2. Ran `v7-service-matrix-test` only in `--probe-observation-only` mode on the
   empty dedicated source. It wrote no Matrix result and changed no routing.
3. Registered/reused the exact existing Engineering-Authority request and,
   under the user's standing approval, recorded decision
   `APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE` through
   `v7-operator-execution-packet`. That action only appended an Authority
   audit decision: `runtime_apply=false`, `routing_mutation=false`,
   `users_moved=0`.
4. Re-ran the native admin draft pool preview before materialization. Its
   duplicate guard stopped the operation. No duplicate interface, disabled
   pool entry, runtime profile, client assignment or route was created.

The request is therefore **approved but not consumable**: the existing admin
owner correctly requires a genuinely independent, healthy egress profile/peer
before it can materialize an isolated source.

## Independent Polygon evidence revalidated

The following existing tests passed after the source-readiness finding; they
do not claim a production client recovery:

- candidate failure matrix: same contract at scale, full fallback on
  disagreement, stale/certification fail-closed;
- controlled Matrix full/subset equivalence and required-service failure
  equivalence;
- causal T0–T11 candidates, recovery conservatism and safety invariants;
- FAST foreground deadline loop, including no backlog and no legacy tail
  delaying the next FAST phase.

The local test sandbox initially forbade binding a loopback HTTP fixture. The
two affected Polygon modules were re-run outside that sandbox and passed:
`11` tests in `6.855 s`. The complete focused set passed `35` assertions/tests
across both runs. The previous C8 three-phase evidence remains unchanged:
`19.441 s`, `22.324 s`, `22.030 s` for 1,000 controlled contracts, below the
30-second FAST phase budget, with cap 8.

## Decision and exact residual

`STOP_SAFE_CONTROLLED_REAL_PATH_SUBSTRATE_UNAVAILABLE` is the only residual
for the real controlled T0–T11 path. It is not a Matrix, FAST timing, Planner
or ordinary-production blocker.

Required re-entry evidence: an owner-verified **healthy and independent**
dedicated egress profile/peer which passes the native disabled-pool preview
and has capacity for exactly one certification identity. A duplicate of source
`1`, a shared egress, an expired reservation, or a source with more than one
certification identity must remain rejected.

## Plan position

- Expanded execution plan: **32%**.
- Stage 1 (isolated controlled source): readiness investigation and authority
  path are complete; actual controlled T0 creation is blocked on the external
  healthy profile/peer.
- Stages 3 and 7: existing Polygon safety, comparison and scale evidence is
  revalidated; it remains Engineering evidence only.
- Stages 2, 4–6 and 8: not admissible until Stage 1 produces a healthy exact
  source and the existing owners revalidate the full chain.

The smallest executable successor is to obtain a distinct owner-verified
egress profile/peer through the existing admin draft lifecycle, then re-run
its native disabled-pool preview and the existing one-user source selection.
