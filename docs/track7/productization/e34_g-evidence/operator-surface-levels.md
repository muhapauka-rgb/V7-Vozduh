# E34.G Operator Surface Levels

operator_surface_levels_defined=true

## Level Model

| Level | Name | Purpose | Current UI pattern |
| --- | --- | --- | --- |
| Level 1 | System overview | Show state, urgency, affected scope, and next safe action. | `Главная`, metrics, topology, important events. |
| Level 2 | Problem explanation | Explain what happened and who/what is affected. | Alert drawer, user/channel/routing detail drawer. |
| Level 3 | Operational detail | Show preview, evidence, impact, rollback, and verification. | Workspace panels, wizard result panels, check result drawers. |
| Level 4 | Expert diagnostics | Show raw proof only when needed. | Expert drawer sections, logs, audit detail, hidden JSON summaries. |

## Surface Rules

Level 1 must answer:

- is the system OK;
- who is affected;
- what is the next safe action.

Level 2 must answer:

- why this status exists;
- what evidence supports it;
- where to go next.

Level 3 must answer:

- what action is proposed;
- what will change;
- what will not change;
- what rollback or containment exists.

Level 4 must answer:

- what exact evidence exists;
- what internal state produced the decision;
- what audit/provenance record supports it.

## Hidden Complexity

By default, hide:

- capacity formulas;
- scheduler internals;
- lock ordering;
- policy graph internals;
- raw packet/replay ledger;
- raw release/backup manifests;
- raw command output.

Show these only in expert diagnostics, logs, or support drawers.
