# Wave 1 Operator Workflow Review

Verification date: 2026-05-30

Workflow under review:

Problem -> Evidence -> Diagnosis

## Working Flow

The Checks workflow is usable:

1. Operator sees a problem in `Проверки`.
2. Operator opens the diagnostics Evidence chip.
3. Drawer explains the object and shows one evidence bundle.
4. Operator opens the bundle.
5. Bundle shows:
   - current status
   - verification state
   - timeline
   - evidence items
   - related objects
   - recommendation

This supports the intended workflow.

## Operator Value

`operator_value_visible=true`

The operator can answer:

- what object is being explained
- what evidence exists
- whether the evidence is read-only
- what recent audit records support the finding
- what the recommendation says

## Remaining Workflow Gaps

The value is not yet evenly available across the admin:

- Route reality evidence exists in the API, but `Маршруты` does not expose a visible evidence entry point.
- Log evidence exists in the API, but `Логи` does not expose a visible evidence entry point.
- User/channel evidence exists, but current responsive layout hides the row action chips.

## Technicality Review

PARTIAL:

- Some summaries are operator-readable, for example: `Audit tail contains 2 recent records for operator review.`
- Some summaries are still runtime-file oriented, for example: `V7 state snapshot age is ...`

Recommended improvement:

Translate technical summaries into operator language while keeping raw evidence visible below the summary.

## Operator Workflow Verdict

The Evidence foundation is useful, but the workflow is only fully proven through `Проверки`.

`operator_value_visible=true`

`operator_workflow_complete=false`
