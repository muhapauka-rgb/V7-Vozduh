# V7 admin operator rebind contention admission repair

## Trigger and current cause

The operator UI reported `operator_profile_rebind_deadline_exceeded` while an
ordinary V7 recovery was active.  The browser retried a canonical
execution-control conflict for only seven seconds, although the live recovery
could legitimately hold that single protected window longer.  The request was
therefore abandoned by the browser before it had been admitted; this was not a
health or target-eligibility rejection.

## Change

`admin/v7-admin-api` now separates two different bounds:

- route mutation and its exact route verification remain bounded by the
  existing seven-second operator contract;
- browser-local admission retry waits up to 45 seconds only while the existing
  execution-control owner reports a busy protected window.

There is no server queue, durable retry state, new owner, target selection,
route writer, or user-state mutation.  Each retry re-reads the same canonical
control and then uses the existing governed `v7-user-switch` path.  At seven
seconds the UI reports a pending protected window rather than falsely marking
the selected channel as failed; on final admission timeout it rolls back the
optimistic display and states that the route did not change.

## Verification

Focused regression passed:

```text
python3 -m unittest \
  tests.unit.test_admin_realtime_truth.AdminRealtimeTruthTest.test_inline_channel_choice_starts_governed_rebind_without_intermediate_drawer \
  tests.unit.test_admin_realtime_truth.AdminRealtimeTruthTest.test_operator_rebind_reports_held_route_writer_as_retryable_and_reopens_control \
  tests.unit.test_admin_realtime_truth.AdminRealtimeTruthTest.test_operator_rebind_accepts_timeout_only_after_existing_core_primary_verify

Ran 3 tests: OK
```

## Scope and next evidence

This repairs operator-intent admission under real V7 recovery contention.  It
does not relax route safety and it does not certify the seven-second end-to-end
recovery SLO.  The next valid evidence is a user-originated channel selection
that overlaps a live protected V7 operation and reaches existing governed route
verification without a browser-side seven-second abandonment.
