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

## Production effect at this point

None yet. No Runtime deployment, route, assignment, client, Matrix, timer or
Authority contract changed during implementation. Safe deploy, Runtime
alignment and an owner-admitted controlled proof remain mandatory.

## Next step

Run the existing safe-deploy gate for this exact implementation. If it admits
the manifest, publish/deploy, prove Runtime alignment, then request a fresh
exact bounded N10 product/Authority contract before any ordinary-client move.

Captured: `2026-08-27T10:44:51+03:00`
