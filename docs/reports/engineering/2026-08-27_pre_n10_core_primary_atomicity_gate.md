# Pre-N10 Core-primary atomicity gate — 2026-08-27

## Objective

Execute the first mandatory gate from the accepted N10 bounded-production
prompt: determine whether the current owner can update Core-primary routing
once at the lawful governed cohort boundary, without a full production rebuild
for every individual client switch.

No client, route, Matrix, Planner, Authority, service profile, timer or
production configuration was changed in this block.

## Fresh current evidence

The current Runtime Core-primary verification passes under approved contract
`rcpp_6bfcaa2063bd7567c9554b6d`:

| Check | Result |
| --- | --- |
| Enabled identity/class membership | 125 expected, 125 actual, 0 missing, 0 unexpected |
| Class-to-egress mapping | 4 expected, 4 actual, 0 missing, 0 unexpected |
| Whole-system route check | PASS in `CORE_PRIMARY_CLASS_ROUTING` mode |
| Desired-state check | PASS, zero errors |
| Health Runtime | `v7-health.service` active |
| Legacy standalone Matrix/Telegram timers | inactive as intended |

Thus there is no current routing incident and no basis for a repair movement.

## Existing-owner capability audit

The deployed `v7-routing-sync --help` exposes only:

- `--core-primary-apply`;
- `--core-primary-fallback`;
- `--core-primary-verify`;
- `--user`.

`--core-primary-apply` derives every enabled registry user, deletes and
recreates the whole `v7_routing_core` nft table, writes all membership entries,
updates every current class route, and retires legacy routes. It is atomic for
that complete global projection but is not an affected-cohort operation.

The deployed `v7-user-switch` has no Core-primary hand-off. The unpublished
source change `97692b70` calls the global apply after every individual switch;
the standard safe-deploy gate correctly rejected that broader blast radius.

No current caller or owner implements:

```text
governed cohort transaction
-> canonical cohort assignments
-> one affected-cohort Core-primary projection commit
-> affected-scope verification
-> whole-system verification
```

## Result

```text
CORE_PRIMARY_COHORT_COMMIT_ARCHITECTURE_DECISION_REQUIRED
```

This is an architecture/ownership boundary, not an ordinary implementation
defect. N10 bounded production cannot safely issue or consume a movement
contract until the smallest existing-owner extension is selected.

## Required owner decision

Choose and bound one existing-owner extension that provides all of:

1. one atomic projection update for the exact admitted cohort or class delta;
2. no second route writer and no second registry/truth source;
3. no full-population rebuild once per moved identity;
4. preimage/rollback tied to the same governed operation;
5. exact affected-scope verification plus whole-system Core-primary
   verification before terminal success;
6. failure containment that prevents later members from using a stale map.

After that decision is implemented and proven, the separate exact
`N10_BOUNDED_PRODUCTION` product/Authority contract remains required before
any new ordinary-client movement.

## Next frontier

`CORE_PRIMARY_COHORT_COMMIT_ARCHITECTURE_DECISION_REQUIRED`.
