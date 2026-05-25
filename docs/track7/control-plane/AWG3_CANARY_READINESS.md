# AWG3 Canary Readiness

This document evaluates `awg3` as a future one-user canary target using copied read-only runtime state. No user was switched to `awg3`.

## Current Signals

Sampled `v7-state.json`:

```text
egress=awg3
diagnose_severity=OK
code=200
users=0
load_status=OK
avg_mbps=8.427
min_mbps=5.11
stability=0.606384
handshake_age_seconds=77
```

Sampled 1h quality summary:

```text
avg_mbps=9.1
min_mbps=4.576
fail_rate=0.0716
stability=0.5101
score=69.19
```

Sampled load summary:

```text
users=0
status=OK
operator_status=warm
```

## Interpretation

Positive:

- enabled in `egress.registry`;
- interface exists as `awg3`;
- 0 assigned users;
- load status OK;
- current diagnostic severity OK;
- stability is above the policy stability floor.

Negative:

- 1h average speed is below the policy minimum average;
- 1h minimum speed is below the policy floor;
- 5m and 24h windows show the same weak throughput pattern;
- platform load summary says operator status `warm`, with limited healthy capacity;
- canary target quality is not strong enough to treat as automatically safe.

## Can AWG3 Ever Be A Canary Target?

Yes, but only conditionally. `awg3` is a reasonable canary target candidate because it is empty, enabled, and routable. It is not GO-ready under the sampled quality floor.

## Required Future Conditions

- current diagnostic remains OK;
- current and 1h quality meet policy floor or receive explicit operator waiver;
- load remains OK;
- no autoswitch penalty applies to the candidate user;
- kill switch and route checks are OK;
- reconcile FAIL is resolved or explained;
- rollback to previous egress is prepared.

## Waiver Boundary

A quality waiver may be acceptable only for a one-user, time-bounded canary when the purpose is to verify routing mechanics rather than user experience. It must not be used for broad migration.

## Verdict

`awg3` is **CONDITIONAL**, not GO-ready. It can be used as a future canary target only after the hard blockers are handled or explicitly waived.
