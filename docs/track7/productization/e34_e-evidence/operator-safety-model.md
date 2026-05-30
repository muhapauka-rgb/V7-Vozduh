# E34.E Operator Safety Model

operator_safety_defined=true

## Safety Principle

Operator Independence is safe only if the system makes dangerous actions visible, hard to execute accidentally, and impossible to execute silently.

## Protections

| Protection | Requirement |
| --- | --- |
| Dangerous action warnings | Any action affecting runtime, users, routing, release state, restore state, or scheduler state must show blast radius and rollback path. |
| Dual confirmation | Destructive, irreversible, production-affecting, or multi-user actions require dual confirmation. |
| Blast radius visibility | Operator must see affected users, targets, route tables, batches, and services before execution. |
| Rollback visibility | Operator must see rollback target, rollback confidence, rollback manifest, and rollback verification plan. |
| Fail-closed defaults | Unknown evidence, stale certification, policy conflict, runtime drift, or missing rollback denies forward execution. |
| Safe recovery defaults | Default next action is evidence collection, validation refresh, containment, or rollback, not arbitrary mutation. |

## Forbidden Operator Paths

- execute before evidence;
- modify routing outside governance;
- use stale approval packets;
- bypass replay protection;
- promote uncertified release;
- restore unverified backup;
- ignore hidden movers or selected moves;
- lower gates to clear a blocker.

## Operator UI Requirements

Any future UI/TUI/CLI should present:

```text
status
blocked_reason
evidence_bundle
blast_radius
rollback_path
required_confirmations
next_safe_action
closure_verdict
```

## Emergency Behavior

Emergency containment may be faster than normal recovery, but it must still be:

- scoped;
- logged;
- reversible where possible;
- followed by verification and closure;
- unable to authorize unrelated forward execution.
