# E25.12 First Movement Readiness Decision

## Decision

`first_movement_ready=true`

`recommended_target=amneziawg-exec-20260528-10-8-1-14`

`recommended_next_block=E25_13_FRESH_APPROVAL_PACKET_FOR_FIRST_MOVEMENT_WITH_EXECUTION_TARGET`

## Required Conditions

| Condition | Result |
| --- | --- |
| target readiness final status is `GO` | PASS |
| sustained GO over 20-sample window | PASS |
| avg Mbps >= `15.0` | PASS, `27.12` |
| min Mbps >= `10.0` | PASS, `10.67` |
| no sample below floor | PASS |
| runtime checkers OK | PASS |
| selected_moves zero | PASS |
| hidden movers absent | PASS |
| candidate still on `1` | PASS |
| target zero-user | PASS |
| execution-only/governance reservation preserved | PASS |

## Residual Risk

The lowest sample was `10.67 Mbps`, close to the `10.0 Mbps` hard floor. This does not block readiness, but it means the next block must not reuse stale readiness. E25.13 must create a fresh approval packet, and the eventual movement block must run fresh execution-time rechecks before any movement.

## No Execution Authorization

`execution_allowed_now=false`

This block does not authorize immediate user movement. It only re-establishes that the target is suitable for a fresh approval packet in the next block.
