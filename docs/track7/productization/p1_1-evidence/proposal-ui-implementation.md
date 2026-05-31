# P1.1 Proposal UI Implementation

proposal_ui_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: show recommendations in context
Admin Surface: Главная, Пользователи, Каналы, Маршруты
Runtime Service: Proposal API read calls
Storage: Proposal Store
API: GET /api/proposals*
UI Component: ProposalCard, ProposalDrawer, ProposalTimeline, ProposalStatus
```

## Components

### ProposalCard

Used for prominent recommendations on `Главная` and `Маршруты`.

Shows:

- proposal type;
- status;
- confidence;
- severity;
- reason;
- affected users count;
- proposed target;
- evidence link.

### ProposalStatus

Compact indicator for table rows.

Shows:

- `ACTIVE`;
- `REVIEW_REQUIRED`;
- `EXPIRED`;
- confidence pill;
- blocker count if available.

### ProposalTimeline

Drawer section.

Shows:

- observed;
- activated;
- review required;
- refreshed;
- expired;
- superseded;
- closed.

### ProposalDrawer

Shared drawer.

Sections:

- summary;
- confidence;
- impact;
- affected users;
- required services;
- evidence link;
- expected benefit;
- rollback hint;
- governance path;
- advanced details.

## Exact Admin Placement

| Section | Placement |
| --- | --- |
| `Главная` | Top recommendations / attention list; no direct apply button. |
| `Пользователи` | User row next-action column and user drawer proposal section. |
| `Каналы` | Channel drawer proposal section for suitability/avoidance/capacity. |
| `Маршруты` | Route check results and service-aware preview panels. |

## UI Data Flow

```text
render section
-> call /api/proposals or /api/proposals/by-object/{type}/{id}
-> render cards/chips
-> open ProposalDrawer
-> call /api/proposals/{proposal_id}
-> optional open EvidenceDrawer from linked evidence
```

## Safety Rules

- No direct movement button inside ProposalCard.
- Any future "prepare batch" action must clearly enter governance.
- Expired/review-required proposals are visually disabled for action.
- Required services must be visible when they influenced proposal.

## Implementation Completeness

UI plan is implementation-ready for read-only recommendations in current `/admin-v2`.
