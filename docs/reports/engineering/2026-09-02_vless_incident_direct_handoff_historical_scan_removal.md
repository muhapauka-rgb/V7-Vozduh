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
runtime outcome, not SLO credit.

## Deployment and Runtime alignment

The bounded repair was committed as `c25bf2747ace8bcb15992253039482025fdec79b`,
published to `Updatesystem`, and deployed with the existing safe-deploy owner:
`deploy-z8-14-Updatesystem-c25bf27-20260902T140438`.

The deploy gate reported no blockers and final truth verification passed.
Independent post-deploy checks confirmed:

- local and Runtime `v7_sync_lib.py` SHA-256:
  `79bf55959f365855e70c1ffa1583368e9df67a24077aee22ffb7964bac64a3b6`;
- local and Runtime Matrix executable SHA-256:
  `9d51fc3f0b6c451891f4571a95b17f80e53d51f82d73ee0b30e63f115c09d142`;
- `v7-health.service`: `active`.

No post-repair live automatic timing is claimed yet. The next acceptable
measurement must originate from the normal V7 Runtime caller and retain all
required route and service S11 checks.

## Remaining work

Observe the next live automatic incident through the normal Runtime caller.
The measurement must retain all required route and service S11 checks and
separately quantify the remaining advisory and Apply/verification time.

## Follow-up: stale Telegram wake rejection

After the preceding deploy, the restarted health owner consumed one historical
Telegram Matrix row as if it were a new wake. Its receipt had no current
ordinary failed scope, no attempted action and no user movement, yet consumed
23,014 ms and preempted ordinary detection work. The row's Matrix observation
was more than two days old.

`tools/runtime-support/v7-health-loop` now applies the existing 10-second
freshness law to direct service/HARD wake rows as well as profile-required
rows. Rows without an ISO timestamp retain controlled-fixture compatibility;
production rows with stale or malformed timestamps cannot start a persistent
recovery transaction. This changes no Matrix status, target choice, Authority,
Candidate, Packet, Lease, Barrier, route writer or S11 rule.

Focused verification: 4/4 freshness cases passed; the full
`test_v5_3_role_based_recovery` suite passed 24/24.

The change was published as `f3a0259a465f3e431f57dd94ffdc3ace54f46c1b`
and safely deployed as
`deploy-z8-14-Updatesystem-f3a0259-20260902T141543`. The safe-deploy gate
reported no blockers and GitHub truth passed. Independent Runtime verification
confirmed `v7-health.service` is active and its deployed health-loop SHA-256
matches local source:
`ebc1b64a7c8ff5a5cdd57aaa60c2960757a1c6e45fe843992f6dec4d0650cddc`.

Immediately after the service restart, the health journal emitted no recovery
receipt for the stale Telegram row. Current canonical scope has no ordinary
user on VLESS; the still-visible VLESS failure therefore creates no empty
ordinary recovery transaction. This is the expected no-op until a current
ordinary profile is actually affected.
