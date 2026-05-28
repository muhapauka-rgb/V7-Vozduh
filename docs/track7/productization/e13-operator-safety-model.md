# E13 Operator Safety Model

## Purpose

The UI must prevent unsafe action by construction. Serious actions should be
possible, but bounded, fresh, explained, reversible, and auditable.

## Safety Gates

| Gate | Required for | Fail behavior |
|---|---|---|
| Evidence freshness | Any approval | Approval disabled and marked stale. |
| Registry hash match | Movement, rollback, clearance | Fail closed. |
| Selected-move fingerprint match | Movement and nonzero clearance | Fail closed. |
| Generation token match | Nonzero budget and apply restore | Fail closed. |
| Target readiness GO | Target use | Approval blocked. |
| Restore-settle GO | Apply restore | Approval blocked. |
| Rollback contract present | Forward movement | Approval blocked. |
| Hidden mover scan clean | Movement and restore | Approval blocked. |
| Runtime checkers OK | All governed actions | Approval blocked. |
| Timer state expected | Apply lifecycle | Approval blocked. |
| Capacity within hard limit | Target use | Approval blocked. |

## Evidence Freshness

Each approval surface shows:

- generated time;
- expiry time;
- source state;
- users registry hash;
- egress registry hash;
- planner generation;
- checker timestamp.

Expired evidence cannot be approved. The only allowed action is regenerate.

## Dangerous Action Confirmations

Confirmation text must be specific:

- "Approve movement of 2 listed users to WireGuard with rollback to target 1."
- "Restore apply timer for operation E13-preview after restore-settle GO."
- "Clear expired restore barrier with max selected moves 0."

Generic confirmations such as "Are you sure?" are not acceptable.

## Dual Confirmation Actions

Require two confirmations:

- nonzero movement budget;
- apply timer restore;
- barrier clearance;
- target reservation mutation;
- rollback after partial failure;
- emergency containment.

The second confirmation must restate blast radius and rollback state.

## Stale Evidence Warnings

Stale evidence appears as `unknown` or `blocked`, not as a soft warning, when it
is used for approval. Historical reports are clearly labeled historical and
cannot become an approval source.

## Hidden Movement Alerts

Hidden movement detection triggers:

- global warning;
- affected operation mark;
- apply timer state visibility;
- switch-history diff;
- emergency containment option;
- approval freeze until classified.

## Delayed Movement Alerts

Delayed movement after a restore or clearance opens the delayed monitor in
blocked state. It must show:

- moved users;
- from/to targets;
- whether movement was approved;
- timer/journal evidence;
- classification status;
- whether repair is prohibited until governance decision.

## Capacity Warnings

Target capacity warnings are shown before approval:

- approaching soft limit;
- hard limit boundary;
- target reserved;
- production capacity competition;
- rollback target load risk.

Hard limit breach blocks approval.

## Active Barrier Warnings

Active or expired barriers appear in the global status band. The UI must say
whether failover is suppressed, whether clearance is required, and whether
apply timer can safely run.

## Generation Mismatch Warnings

Generation mismatch should show:

- expected generation;
- current generation;
- affected approval;
- selected-move fingerprint mismatch if present;
- safe action: regenerate preview or revoke approval.

## Actions The UI Must Prevent

- approving stale movement preview;
- applying nonzero budget without generation token;
- approving movement without rollback contract;
- clearing a barrier without selected-move budget;
- using reserved target beyond approved scope;
- starting larger cohort from two-user approval;
- running broad autoswitch apply;
- silently repairing unexpected movement.

## Emergency Containment

Emergency containment is a narrow workflow:

- available only when unexpected movement or hidden apply is detected;
- primary action is to stop further apply movement;
- no manual user repair unless separately approved for safety;
- every containment emits evidence and mutation statement.

## Operator Trust Rule

Every unsafe disabled action must explain:

- which gate failed;
- what evidence is missing or stale;
- what safe next action exists.

