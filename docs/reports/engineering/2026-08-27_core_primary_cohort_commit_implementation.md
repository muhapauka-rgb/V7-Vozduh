# Core-primary cohort commit — implementation report

## Purpose

Implement the owner-approved smallest extension needed before the next bounded
N10 production cohort: publish the route-map change for the admitted two-to-
four member group once, after all of its canonical assignments are staged.

## Reused owners and boundaries

- `v7-user-switch` remains the only low-level writer for the individual
  assignment, policy rule and route-table update.
- `v7-routing-sync` remains the only Core-primary map writer and derives its
  desired projection only from the canonical users registry.
- `v7-users-autoswitch` remains the existing governed Packet/Lease/Barrier
  consumer and serial cohort executor.
- No Matrix, Planner, queue, timer, registry or state source was added.

## Implemented behavior

For an already-authorized N10 small cohort (exactly two through four members):

```text
existing Packet / Lease / Barrier
  -> serial existing v7-user-switch staging for each selected identity
  -> one v7-routing-sync --core-primary-cohort-commit nft transaction
  -> exact selected-user route checks
  -> whole-system Core-primary verification
  -> existing rollback / containment on any failure
```

The new commit refuses to run when any non-selected map entry is stale, when a
class-to-egress change would be needed, when the Core-primary contract is not
active, or when the scope is not exactly 2–4 members. It therefore cannot turn
a partial/global routing inconsistency into a partial cohort update.

The former registry-wide Core-primary rebuild remains the fallback/repair
mechanism, but is no longer invoked once per member in this N10 path.

## Verification

Focused regression set:

```text
233 tests passed
```

It includes new checks proving that:

1. the kernel transaction contains only the selected identities;
2. a stale non-selected map fails closed before mutation;
3. a selected N10 member does not invoke the global rebuild while staging;
4. the governed cohort consumer invokes one projection commit only after all
   members are staged, then performs verification.

`python3 -m py_compile` loaded the sources successfully through the unit-test
imports. Its explicit bytecode-write step was blocked by the local macOS cache
directory permission, not by a source syntax error.

## Deployment and Runtime verification

Published commit: `b8400c480143f5529ee7bf2a718153b7d900aeb5`.

The standard `tools/v7-safe-deploy` passed after the existing required health
service restart. Runtime deployment receipt:
`deploy-z8-14-Updatesystem-b8400c4-20260827T104642`.

Independent Runtime checks passed:

| Check | Result |
| --- | --- |
| Local / GitHub / Runtime commit | aligned at `b8400c48` |
| `v7-health.service` | active |
| New Core-primary cohort command | present |
| Core map membership | 125 expected / 125 actual; zero mismatch |
| Class-to-egress mapping | 4 expected / 4 actual; zero mismatch |
| Whole-system route check | PASS |
| Desired-state check | PASS, zero errors |
| Standalone Matrix and Telegram timers | inactive as intended |

No client, route assignment, Matrix state, service profile or Authority
contract was changed while deploying or verifying this implementation.

## Next step

Request a fresh exact bounded N10 product/Authority contract before any
ordinary-client move. It must name the 2–4 member scope, source/target,
rollback, observation window and stop conditions; the old consumed contracts
cannot be reused.

Captured: `2026-08-27T10:44:51+03:00`
