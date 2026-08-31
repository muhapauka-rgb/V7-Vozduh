# Historical incident gate — causal repair

Date: 2026-09-01

## Finding

The existing read-only integrity projection found 156 records marked OPEN.
They covered four sources and had scope timestamps from previous events, while
the currently enabled-user registry had no user on VLESS.  Their invalid
historical scope accounting set a single global `STOP_SAFE` result even though
they were not fresh evidence of a current source failure.

This was a real availability defect: an unrelated new failure could inherit a
historical stop condition before the live Matrix had a chance to establish its
own current source scope.

## Repair

`service_failure_causal_integrity_status` now separates records as follows:

- a fresh or timestamp-less open record remains live and blocks safely on any
  integrity defect;
- an open record whose owner-backed source-scope observation is older than the
  existing 900-second service-truth freshness window remains auditable, but is
  excluded from the live execution gate;
- its source, count, age and defects are reported as compact historical
  warnings.  No incident state, registry, Authority, candidate, packet, lease,
  route or user was modified by the status read.

The normal Matrix path independently validates every new failure.  Therefore
the repair does not permit stale or unknown source health to execute recovery.

## Verification

- Four focused integrity tests pass: broken current scope still blocks; valid
  current open scope passes; closed historical anomaly remains visible; stale
  open anomaly no longer blocks a fresh unrelated runtime event.
- Runtime before the repair: current branch and deployed fingerprint aligned;
  `v7-health.service` and `v7-admin-api.service` active.

## Next runtime evidence

The next real current source failure must originate in the live health caller.
V7, not Codex, will create the current Matrix scope and perform any admitted
recovery.  The enhanced receipt will measure T0, consumer start, consumer
completion, governed execution and required-service S11 against the active
7-second contract.
