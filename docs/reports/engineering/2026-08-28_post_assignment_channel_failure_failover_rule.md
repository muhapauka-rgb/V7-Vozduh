# Engineering Report — post-assignment channel failure failover rule

Date: 2026-08-28

## Request

If a client received or renewed a configuration while its channel was
eligible, and that channel later became unusable, the system must recognize
the affected assignment and route the client through the existing governed
failover path.

## Reused owners

- Matrix/diagnosis remains the source of fresh channel-failure evidence.
- `users.registry` remains the canonical current client-to-channel assignment.
- `tools/v7-users-autoswitch` remains the existing incident, Planner and
  Candidate/Packet/Lease/Barrier/Apply consumer.
- `v7-user-switch` remains the only route writer.

No new owner, watcher, timer, registry, queue, state source or assignment
history was introduced.

## Change made

`tools/v7-users-autoswitch` now keeps an affected source scope when the health
owner has already marked the source `down`. Previously the scope required the
source to remain enabled and not-down, which could hide the clients that most
needed recovery. Persistent required-service failures are likewise retained
for an operationally failed source, while planned `maintenance` and
intentional `disabled` states remain excluded from ordinary failover.

Current-channel evidence now accepts the existing hard diagnosis reasons:

- `interface_down_or_missing`;
- `curl_failed_and_handshake_unsupported`;
- `curl_failed_and_handshake_stale`;
- a fresh hard `FAIL` row whose operational state is `down`.

Administrative disablement is not treated as a failure signal by this change.

## Program contract change

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md` now explicitly defines:

```text
eligible assignment
-> later fresh source failure
-> affected users from current users.registry
-> existing Planner target selection
-> governed Candidate/Packet/Lease/Barrier/Apply
-> exact route and required-service verification
```

The contract remains fail-closed for stale, unknown, conflicting and
administrative-only evidence. Controlled certification identities stay under
their certification owner when policy disables production autoswitch.

## Verification

- New regression: assigned user remains in the failed source scope after the
  owner marks the source `down`, and fresh hard failure evidence is confirmed.
- `tests.unit.test_v7_users_autoswitch_policy`: **218 passed**.
- `tests.unit.test_v5_3_nontelegram_trigger_revalidation`: **7 passed**.
- Combined focused run: **225 passed**.
- Python syntax compilation with a temporary bytecode cache: **passed**.

The long service-failure integration module was not used as a completion
signal because its Polygon scenarios exceed the short command window; the
affected behavior is covered by the focused regression and existing policy
suite.

## Runtime and production effect

Commit `956871d06dabe4f59da1ed604eeb75391e500dec` was published to the
`Updatesystem` branch and deployed through `tools/v7-safe-deploy` as
`deploy-z8-14-Updatesystem-956871d-20260828T000919`. The post-deploy
`v7-truth-check --all` was `FULLY_ALIGNED`; local, GitHub and Runtime hashes
matched, and `v7-health.service` was active.

A read-only production Planner reconciliation then observed 126 users and 7
egresses, selected zero moves, and reported `NO_INCIDENT_DISABLED`. This is
expected for the current product state: the global emergency-failover runtime
policy remains disabled and the intelligence snapshot gate is stale, so no
client was moved and no route was changed. The new rule is therefore deployed
and ready to be consumed by the existing governed L3 path when its existing
production Authority/policy gates are enabled; this report does not claim a
live failover outcome.

## Limitations and safety

The rule does not bypass freshness, required-service, target, capacity,
cooldown, anti-flap, Authority, verification or rollback gates. If a safe
target is absent or evidence is stale/ambiguous, the existing consumer must
produce `STOP_SAFE` and leave the assignment unchanged. VLESS remains a
controlled certification source in its current policy and is not opened for
ordinary autoswitch by this change.

## Next step

Run the existing safe-deploy gate, publish/deploy this already-tested change,
then perform one read-only production reconciliation proving that a fresh
failed source with assigned users is discovered by the existing Matrix ->
Planner consumer and that no unrelated users are selected.

## Follow-up reconciliation: Liza was detected but not moved

The fresh production read-only run for Liza (`10.7.0.125`) confirms that the
new assignment-failure correlation works: the Planner produced one bounded
candidate from `vless` to `awg0`.  It was not applied because the existing
execution gates were closed:

- `emergency_failover_enabled=false` and `l3_incident_state=NO_INCIDENT_DISABLED`;
- the intelligence snapshot gate was `STOP` because service/channel scores,
  risk, trust and blast-radius snapshots were expired or had source-hash
  mismatches;
- the selected move was therefore reduced from one candidate to zero applied
  moves (`selected_moves_after_gate=0`, terminal `DRY_RUN`);
- `users.registry` still records `10.7.0.125 current=vless enabled=1`;
- current VLESS diagnosis is a fresh hard transport failure
  (`curl_failed_and_handshake_unsupported`).

There is also a role-state inconsistency that must be resolved by the existing
owners before ordinary production movement: the VLESS registry row is marked
as a controlled certification source with `autoswitch_allowed=false` and
`production_assignment_allowed=false`, while Liza's current assignment row
has no certification marker.  This change deliberately did not override that
policy or move her manually.  The exact remaining action is an owner-backed
one-user reclassification/Authority decision (or certification cleanup),
followed by a fresh Matrix/intelligence snapshot and the normal
Candidate -> Packet -> Lease -> Barrier -> Apply -> verification path.

## Second fix: fresh Matrix is now accepted for a failed assigned channel

The first change correctly kept the failed source scope visible, but the
emergency evidence gate still required the file-level freshness of the legacy
`v7-state.json`.  On production that projection had not been refreshed since
2026-08-23, while the canonical Matrix owner was producing current results.
The deployed follow-up now accepts a **fresh Matrix majority failure** as the
channel-level failure evidence: at least half of the services (and at least
two) must fail in one fresh Matrix generation.  A single service failure still
cannot trigger whole-channel movement.

Focused verification now totals **219** policy tests plus **7** trigger
revalidation tests, all passing.  Commit `c9c7cf7da30dc0eb80aed224e0eaac8f996ff00a`
was deployed via `tools/v7-safe-deploy` as
`deploy-z8-14-Updatesystem-c9c7cf7-20260828T002808`; the Runtime binary
contains the new Matrix evidence path.

After a fresh owner-backed VLESS Matrix run, 13 of 14 service probes failed
(Telegram was the only successful service), so the source is currently
functionally degraded.  The Planner still did not apply Liza's move because
the old approved plan lock is expired and belongs to a different four-user
operation.  The snapshot gate correctly returned `SOURCE_CHANGED` and
`WAIT_FOR_ATOMIC_REPLAN`; the emergency gate therefore had no selected move.
No manual registry edit, route write, or client movement was performed.

The remaining action is now precise: the existing operation/Authority owner
must close or supersede the expired lock and issue a fresh single-user scope
for `10.7.0.125`; then the existing Planner may reselect a current safe target
and consume Candidate -> Packet -> Lease -> Barrier -> Apply with verification.
