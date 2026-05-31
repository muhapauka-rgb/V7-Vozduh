# E35.B Conflict Resolution Model

## Rule

Every conflict has deterministic outcome.

No movement can proceed while conflict state is ambiguous.

## Conflict Resolution Table

| Conflict | Outcome | Explanation |
|---|---|---|
| Group says AUTO, Operator says MANUAL | MANUAL wins if operator override allowed; otherwise REVIEW_REQUIRED. | Operator owns explicit user intent, but regulated group may require review. |
| Group allows A, Operator pins B | DENY or REVIEW_REQUIRED unless B is group-allowed or explicit group override exists. | Group hard restrictions constrain operator. |
| Operator pin vs Required Services | If pinned channel fails required services, normal movement DENY; containment may EMERGENCY_ONLY. | Pin does not force unsafe service failure. |
| Operator pin vs Safety | Safety wins. | No actor can force unsafe forward movement. |
| Operator pin vs Containment | Containment wins temporarily if hard emergency trigger exists. | Emergency reduces harm. |
| Autoswitch vs Governance | Governance wins. | Autoswitch cannot bypass packet/scope/replay. |
| Scheduler vs Operator | Operator wins unless governance packet explicitly includes override. | Scheduler has no authority creation power. |
| Containment vs MANUAL | Containment wins temporarily on emergency only. | Manual does not trap user on failed channel. |
| Group preferred channel vs Speed | Hard gates first; then score/preference only. | Preference is soft. |
| Sticky current vs Required Services | Required Services win. | Sticky is soft. |
| Capacity full vs Operator pin target | Existing pin may remain if current; new movement to full target denied/review. | Current placement and new movement differ. |
| Governance packet vs stale runtime | DENY. | Packet-bound hashes/recheck are hard. |
| Proposal recommends move vs Authority denies | DENY. | Proposal explains; it never authorizes. |
| User request vs Operator pin | Operator pin wins. | User has no direct routing authority. |

## Conflict States

| State | Meaning |
|---|---|
| `NO_CONFLICT` | Movement may continue to gates. |
| `REVIEW_REQUIRED` | Human/governance decision needed. |
| `DENIED_BY_BOUNDARY` | Hard boundary blocks movement. |
| `EMERGENCY_ONLY` | Only containment/rollback allowed. |

## Admin Surface

Users drawer:

- conflict explanation;
- authority chain;
- next safe action.

Logs:

- conflict resolved;
- actor;
- final outcome.

## Tests

- each table row has deterministic output;
- no ambiguous conflict returns ALLOW;
- conflict reasons appear in admin/API.

## Verdict

```text
conflict_resolution_defined=true
```
