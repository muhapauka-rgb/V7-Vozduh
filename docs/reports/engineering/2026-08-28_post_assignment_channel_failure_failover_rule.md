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

No production service, route, client assignment, Matrix cadence or Authority
state was changed in this block. The code change is ready for the normal
safe-deploy gate; no live client was moved merely to test the rule.

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

