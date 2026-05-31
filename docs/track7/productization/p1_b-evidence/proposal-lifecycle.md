# P1.B Proposal Lifecycle

proposal_lifecycle_defined=true

## States

| State | Meaning | Visibility | Closure |
| --- | --- | --- | --- |
| `DRAFT` | Created by analysis but not ready for operator display. | Hidden or expert-only. | Can become `OBSERVED` or be discarded. |
| `OBSERVED` | Evidence indicates a possible issue or opportunity. | Visible as low-pressure insight. | Can become `ACTIVE`, `REVIEW_REQUIRED`, `EXPIRED`, `CLOSED`. |
| `ACTIVE` | Recommendation is ready for operator review. | Visible in admin surfaces. | Can enter governance path or close. |
| `REVIEW_REQUIRED` | Human review needed before governance. | Visible with blocker/reason. | Can become `ACTIVE`, `SUPERSEDED`, `CLOSED`. |
| `EXPIRED` | Evidence or proposal freshness elapsed. | Visible as stale/disabled. | Requires refresh or closure. |
| `SUPERSEDED` | Newer proposal replaced this one. | Visible in history, not actionable. | Terminal. |
| `CLOSED` | Proposal resolved, rejected or no longer relevant. | Visible in history/audit. | Terminal. |

## Transition Model

```text
DRAFT
-> OBSERVED
-> ACTIVE
-> governance path
-> CLOSED
```

Failure/staleness paths:

```text
OBSERVED -> EXPIRED
ACTIVE -> EXPIRED
ACTIVE -> REVIEW_REQUIRED
ACTIVE -> SUPERSEDED
REVIEW_REQUIRED -> ACTIVE
REVIEW_REQUIRED -> CLOSED
EXPIRED -> CLOSED
EXPIRED -> OBSERVED after evidence refresh
```

## Visibility Rules

Default operator surfaces show:

- `OBSERVED`;
- `ACTIVE`;
- `REVIEW_REQUIRED`;
- `EXPIRED` when relevant.

`DRAFT` is not shown in normal operator flow.

`SUPERSEDED` and `CLOSED` are shown in history, logs or advanced drawer sections.

## Closure Rules

Closure records must include:

- closure reason;
- actor/source;
- timestamp;
- linked evidence;
- whether governance execution occurred;
- whether verification passed.

## Lifecycle Verdict

Proposal lifecycle is evidence-driven and fail-closed. Stale or review-required proposals cannot become execution without fresh governance.
