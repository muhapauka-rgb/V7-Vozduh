# V7 Chuck2 live HTTP-sentinel recovery repair

Date: 2026-08-29

## Scope

Investigate the live ordinary case after the operator assigned Chuck2
(`10.7.0.127`) to `vless` and selected `google`, `google_auth`, `instagram`
and `telegram` as required services.  Repair only the generic automatic
detection defect.  No user, source, target, Candidate, Packet, Lease, Barrier
or route was created or changed by engineering tooling.

## Current evidence

At investigation time Chuck2 was enabled on `vless`.  The current canonical
Matrix showed `google`, `google_auth` and `instagram` as fresh `FAIL` on that
source, while `telegram` was healthy.  `awg3` had fresh healthy evidence for
all four required services, so it was a potential target only if the normal
V7 consumer later admitted it.

The live ordinary detector did **not** report a profile failure:

- `profile_failure_count=0`;
- no receiver invocation and no consumer wake;
- no current source incident was available to the downstream consumer.

This was a genuine generic defect, not a reason to manually recover Chuck2.

## Root cause

The fast ordinary detector's lightweight sentinel considered a successful TCP
connection to the web-service port as service success.  A VLESS route can
therefore accept TCP on 443 while Google, Google Auth or Instagram fails at
the HTTP layer.  The full Matrix already detected those failures, but the
fast detector produced a false healthy result and never initiated its existing
Matrix-confirmation path.

## Repair

`tools/v7-service-matrix-test` now performs a bounded (maximum two seconds;
the Runtime asks for one) HTTP request through the exact source interface for
non-Telegram lightweight checks.  It retains the existing `HTTP_LIMITED`
semantics for expected unauthenticated 401/403/404/405/429 responses, so those
do not become false failure incidents.

The sentinel remains only suspicion evidence:

```text
short HTTP failure
-> existing Matrix confirmation
-> existing automatic consumer
-> existing Authority/Planner/governed execution
```

It cannot create T0, move a user or bypass any owner.  Telegram remains owned
by its existing dedicated sentinel.

## Verification

- new direct tests: HTTP 500 is a lightweight failure suspicion; HTTP 403 is
  `HTTP_LIMITED` and remains non-failing;
- `tests.unit.test_service_failure_episode`: 124 passed;
- relevant fast-producer, Matrix-consumer and health deadline tests: 5 passed;
- `git diff --check`: passed.

## Deployment and next action

The repair is committed locally as `747c55c5`.  The existing safe-deploy
allowlist passed and the local workspace is aligned, but its final verdict is
`NO-GO`: GitHub truth is unreadable and the canonical remote branch cannot be
independently verified.  It must not be deployed by bypassing those owners.

After GitHub becomes readable and the normal safe-deploy gate passes, the next
action is only observation: the normal V7 health caller must itself see the
current VLESS HTTP failure, obtain Matrix confirmation, select any lawful
target and complete required-service S11 for Chuck2.  Any manual movement
would be invalid acceptance evidence.
