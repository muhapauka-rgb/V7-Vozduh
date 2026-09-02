# VLESS incident: direct-handoff historical scan removal

Date: 2026-09-02

## Scope

One fresh ordinary VLESS service-failure recovery was inspected through the
existing Health, Matrix, L3, Planner, Authority and governed-execution owners.
Codex did not select a user or target, create an execution object, invoke the
route writer, or advance the recovery transaction.

## Production evidence before the repair

The ordinary runtime owner completed one automatic VLESS recovery:

- Matrix T0: `2026-09-02T10:45:01Z` / monotonic
  `10273774497840677`;
- Health consumer entry: 267 ms after T0;
- automatic result: one ordinary user moved, `ACTION_COMPLETED`;
- total T0 to health-consumer completion: **21,762 ms**;
- governed transaction: **7,712.798 ms**;
- governed Apply plus verification: **6,035.280 ms**.

The Matrix-to-governed-dispatch pretransaction receipt measured **10,263.998
ms**. Its dominant spans were:

| Span | Measured time |
| --- | ---: |
| Exact current-source/L3 handoff lookup | 6,922.272 ms |
| Fresh existing advisory owner | 3,222.840 ms |
| All other measured Matrix pretransaction work | under 400 ms |

The L3 state file was 3.0 MiB, while the append-only closure history was 230
MiB (2,928 records). The direct-handoff reader parsed the whole history before
it could discover that a newly assigned profile had no matching current L3
handoff. That historical read was not an admission, Authority, target,
Packet, Lease, Barrier, route, or S11 requirement.

## Repair

`tools/v7_sync_lib.py` now handles a Matrix-scoped direct-handoff request as
follows:

1. Read the existing canonical L3 incident and exact current scope first.
2. If no matching live L3 handoff exists, return the established
   `NO_CURRENT_DIRECT_HANDOFF` terminal immediately; the existing advisory
   owner remains responsible for materialising a fresh exact obligation.
3. If the L3 record supplies an exact obligation identity, read only the
   bounded recent tail of the existing closure history.
4. Accept only one matching ready obligation; absent, truncated or ambiguous
   evidence fails closed into the already-existing advisory path.

No new owner, state file, cache, timer, queue, Planner, Authority, route
writer, target-selection rule, or verification rule was added. Unscoped
compatibility reads retain their historical behavior.

## Verification

Focused unit verification passed:

- exact fresh L3 obligation before OMP receipt;
- exact Matrix-scoped handoff selection;
- deterministic 100-transition current-scope soak;
- stale receipt-copy rejection;
- scoped new incident proves the full historical closure reader is not
  invoked;
- syntax compilation passed using an isolated bytecode cache.

The production 21.762-second observation is preserved as an automatic
runtime outcome, not SLO credit. The repair has not yet been deployed, and no
post-repair production timing is claimed in this report.

## Remaining work

Publish and deploy the bounded reader repair through `tools/v7-safe-deploy`,
verify Runtime alignment, then observe the next live automatic incident.
The next measurement must retain all required route and service S11 checks and
must separately quantify the remaining advisory and Apply/verification time.
