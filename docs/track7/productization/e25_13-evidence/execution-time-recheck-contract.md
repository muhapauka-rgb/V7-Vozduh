# E25.13 Execution-Time Recheck Contract

## Purpose

This contract defines the mandatory checks for the future movement block. The E25.13 approval packet does not allow immediate execution.

`execution_allowed_now=false`

## Required Recheck Gates

The next execution block must collect fresh runtime truth and deny execution unless every gate passes:

| Gate | Required Value |
| --- | --- |
| packet not expired | `true` |
| packet not replayed | `true` |
| dual confirmation valid | `true` |
| candidate user | `10.7.0.11` |
| candidate current egress | `1` |
| candidate table | `1009` |
| target egress | `amneziawg-exec-20260528-10-8-1-14` |
| target role | `EXECUTION_ONLY` |
| target readiness | `GO` |
| target users | `0` before movement |
| selected_moves | `0` |
| hidden movers | absent |
| runtime checkers | all OK |
| restore-settle gate | `GO` |
| rollback target | `1` valid |
| movement budget | exactly `1` |
| allowed users | exactly `["10.7.0.11"]` |
| allowed targets | exactly `["amneziawg-exec-20260528-10-8-1-14"]` |
| autoswitch_allowed | `false` |
| rebalance_allowed | `false` |
| production_assignment_allowed | `false` |

## Hash Gates

The next execution block must recompute:

- `users.registry` hash
- `egress.registry` hash
- selected moves hash
- selected move fingerprint
- runtime snapshot hash

If hashes differ from the packet, the execution block may continue only if it performs and records a fresh equivalent recheck proving:

- candidate still on `1`;
- target still `GO`;
- blast radius still exactly one user;
- rollback target still valid;
- no selected moves or hidden movers exist;
- execution-only isolation remains valid.

Any unexplained hash drift must deny execution.

## Approved Commands For Next Execution Block Only

Forward:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Rollback:

```bash
v7-user-switch 10.7.0.11 1
```

No other raw movement command is approved.

## Deny Conditions

Deny and write an audit/denial record if any of these occur:

- packet expired
- approval replayed
- candidate already moved
- target readiness `NO-GO`
- restore-settle `NO-GO`
- selected moves appear
- hidden mover active
- runtime checker fails
- target no longer zero-user before movement
- target not execution-only
- autoswitch/rebalance exclusion missing
- movement budget changed
- unauthorized user added
- unauthorized target changed
- rollback target invalid
- route table `1009` drifted

## Final Rule

Fresh execution-time recheck is mandatory even if E25.13 packet remains non-expired.
