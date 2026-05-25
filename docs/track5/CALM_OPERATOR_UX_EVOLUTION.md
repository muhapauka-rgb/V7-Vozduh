# V7 Track 5 - Calm Operator UX Evolution

Purpose: evolve operator UX without turning V7 into an engineering cockpit.

## Current UX Maturity

V7 already has important Calm Operator UX foundations:

- summary-first information architecture;
- grouped diagnostics model;
- status semantics;
- operator block contract;
- autoswitch/capacity health summary;
- incident and event concepts.

But the UI is still embedded in a 30k-line monolith and is schema-coupled to many endpoints.

## Information Architecture

### Level 1 - Platform State

Default visible layer:

- overall state;
- active incidents;
- affected users/orgs;
- degraded channels;
- autoswitch guard state;
- capacity imbalance;
- sensitive-state warnings;
- runtime baseline/release status.

Must answer:

```text
what is happening?
who is affected?
how serious is it?
what is the next safe action?
```

### Level 2 - Grouped Diagnostics

Open only after a summary item:

- Channels;
- Routing;
- Services;
- Users;
- Trusted RU;
- Autoswitch;
- Provisioning;
- Security;
- Runtime governance.

Each group shows:

- status;
- affected object count;
- likely reason;
- confidence/verification state;
- suggested safe action.

### Level 3 - Deep Evidence

Hidden by default:

- route reality rows;
- command output;
- service matrix rows;
- MTU/path diagnostics;
- raw JSON;
- event streams.

## Cognitive-Load Risks

| Risk | Current Cause | UX Rule |
|---|---|---|
| too many entities | users, egress, route classes, services, devices | group by incident/workflow first |
| noisy diagnostics | service matrix and runtime checks | show status/reason first, rows later |
| dangerous actions feel easy | many action buttons in embedded UI | preview + impact + rollback context |
| hidden runtime governance | release/tool/permission state not visible | add compact governance summary |
| direct/RU ambiguity | trusted/direct state is nuanced | show unknown/degraded honestly, no forced green |

## Calm Summary Design Principles

- One status, one reason, one next action per block.
- Show counts before rows.
- Show "unknown" when evidence is absent.
- Do not show command output in default views.
- Do not add new primary navigation for every feature.
- Dangerous actions require explicit confirmation and impact preview.
- Operator wording should explain impact, not Linux internals.

## Workflow Risk Map

| Workflow | Current UX Risk | Maturity Priority |
|---|---|---|
| user switch | can be used during instability | show anti-flap/capacity context before action |
| autoswitch apply | high impact | keep guarded; show confidence and cooldown |
| egress enable | production impact | show lifecycle gate summary |
| egress delete/pause | user migration risk | show affected users + rollback |
| profile delivery | token sensitivity | show expiry/revoke status clearly |
| direct/RU changes | route policy sensitivity | keep confirmation and separate diagnostics |
| policy update | broad behavior change | show before/after and backup path |
| runtime cleanup | deploy ambiguity | show manifest/archive status |
| sensitive-state hardening | can break access | dry-run access requirements first |

## Operator Pages That Should Evolve First

1. Overview
   - add runtime governance summary;
   - add sensitive-state warning summary;
   - keep details collapsed.
2. Channels
   - show capacity/readiness/lifecycle status;
   - avoid full metrics wall.
3. Incidents / Checks
   - group autoswitch, services, routing, provisioning.
4. Users
   - show readiness and affected users;
   - avoid giant table as default.
5. Settings / Security
   - show release baseline and sensitive-state posture.

## Frontend Evolution Rules

- Preserve backend contracts.
- Preserve auth semantics.
- Preserve action confirmations.
- No frontend-only dangerous action.
- No heavy SPA rewrite before API contract freeze.
- Extract UI blocks only after their API payload is documented.

