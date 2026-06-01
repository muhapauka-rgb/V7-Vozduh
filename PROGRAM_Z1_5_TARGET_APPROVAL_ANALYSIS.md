# Program Z1.5 Target Approval Analysis

Date: 2026-06-01

## Model

Approval for:

- `user=X`
- `target=Y`
- `budget=1`

## Advantages

- Very easy for an operator to understand.
- Strong blast-radius control.
- Replay and rollback are simple.
- Audit trail is concrete.
- Safe by default when target drifts because stale approval is denied.

## Risks

- High stale-denial rate when live quality changes quickly.
- Operator may repeatedly approve targets that become stale before execution.
- Does not express "move this user to the best safe target"; it expresses only "move to this exact target".
- Can block useful bounded autonomy even when a safer equivalent target exists.

## Failure Modes

- target changed
- target health changed
- target capacity changed
- target trust class changed
- target became ineligible
- candidate changed

## Operational Cost

High during unstable periods. The operator loop becomes:

proposal -> approve -> fresh recheck -> stale -> reapprove -> stale.

## Verdict

target_approval_understood=true

