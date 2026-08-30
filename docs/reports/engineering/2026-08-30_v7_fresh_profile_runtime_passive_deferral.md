# V7 fresh profile runtime passive deferral — 2026-08-30

## Evidence

After deploy `f52684cf`, the normal V7 health caller produced an exact current
VLESS scope: two enabled ordinary users, a current source incident, and
Matrix-selected healthy alternatives.  The current source is not healthy for
their required services.

The new source-bound Matrix invocation was observable as an existing child of
`v7-egress-diagnose`, but the preceding passive-event consumer still ran
before the fresh advisory/executor path.  Its measured spans included roughly
15–18 seconds of recovery/state reconciliation and 17–18 seconds of
post-consumption scope reconciliation.  In a separate run the total
`other_required` health role took 45–62 seconds.  The later advisory had no
current obligation and stopped safely, leaving the two users on VLESS.

## Causal conclusion

The failure is generic orchestration order, not a manually chosen source or
target:

`fresh, owner-bound VLESS profile failure -> retrospective passive history ->
freshness/obligation loss -> STOP_SAFE`.

The passive reconciler remains valuable as a durable history and outcome
consumer, but it supplies no additional mutable safety fact to the first
governed attempt for an exact fresh source/profile Matrix binding.

## Repair

The existing Matrix owner now defers that passive historical consumer for only
this narrow case:

- Runtime hot path;
- persistent V7 health owner;
- exactly one current Matrix-bound failed source;
- current incident id and non-empty ordinary affected scope;
- no explicit passive-consumer skip.

The unchanged advisory owner therefore produces the current obligation first,
and the unchanged governed executor retains Candidate, Packet, Lease, Barrier,
Authority, target, capacity, source assignment and required-service S11
checks.  The passive reconciliation remains a later existing-owner consumer.

## Verification

- Python compilation: PASS.
- New focused gate for exact current runtime profile deferment: PASS.
- Existing focused handoff deferment regression: PASS.
- `git diff --check`: PASS.

## Next evidence

Deploy this repair.  The next valid outcome must originate only from V7's
normal health caller and show either automatic governed recovery with exact
per-member S11 timing, or a newly measured generic STOP_SAFE cause.  No Codex
route action, target choice, incident creation, Candidate, Packet, Lease or
Barrier creation is permitted.
