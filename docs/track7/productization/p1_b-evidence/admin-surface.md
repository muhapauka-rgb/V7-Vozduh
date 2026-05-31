# P1.B Admin Surface

proposal_admin_surface_defined=true

## Placement Rule

Proposal integrates into the current V7 Admin. No new top-level navigation item is introduced.

Proposal appears through:

- proposal chips;
- recommended action panels;
- row-level next-action indicators;
- proposal drawer links;
- evidence-backed route/channel/user recommendations.

## Existing Navigation Mapping

| Admin section | Proposal operator meaning | Visible surface | Drawer entry |
| --- | --- | --- | --- |
| `Главная` | Highest-priority recommendations and blocked actions. | Alert/next-action cards, summary rows. | Open proposal drawer from recommendation. |
| `Маршруты` | Why route/channel change is recommended or denied. | Route check result, route reality, preview panels. | Route proposal drawer. |
| `Пользователи` | What should be done for a user and why. | User row issue/next action, required-service mismatch, user drawer. | User proposal drawer. |
| `Каналы` | Which channel is suitable or unsafe for proposed use. | Channel readiness, service matrix, capacity/quality. | Channel proposal drawer. |

## What Operator Sees

The operator sees:

- proposal type;
- short reason;
- confidence;
- severity;
- affected users count;
- proposed target;
- blockers;
- expected benefit;
- linked evidence;
- governance state.

## What Stays Hidden By Default

The first view hides:

- raw scoring internals;
- full probe payloads;
- raw JSON;
- internal policy graph detail;
- secrets or private config values.

These can be shown in advanced details only when redacted and role-allowed.

## Drawer Behavior

Proposal opens in a right-side drawer inside the existing workflow.

Drawer is the normal detail surface for:

- recommendation;
- confidence;
- impact;
- evidence;
- expected benefit;
- rollback hint;
- governance path;
- advanced details.

## Admin Surface Verdict

Proposal is an action-intelligence layer inside existing admin sections. It must never appear as a direct mutation button without governance gates.
