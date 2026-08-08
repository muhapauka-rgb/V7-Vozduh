# CT-M0F: Packet forwarding of active-incident binding

## Production fact

The ordinary `v7-service-matrix-refresh.timer` generation started at
`2026-08-08T20:36:52+03:00` and completed successfully. It created fresh
Candidate/Packet/lease lineage and performed a real one-user route cutover to
a healthy target, but CT-M0F correctly recorded the sample as invalid:
`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID / incident_id_missing`.

The active Matrix obligation, incident and scope had been validated before the
Packet was materialized. The governed executor then rebuilt the Packet binding
only from the availability-first admission payload, where the passive event is
not repeated. Consequently the Packet and Outcome lost the already-validated
causal binding. The move is immutable historical evidence, but it cannot be
credited to the live incident or to the CT-M0F timing ledger.

## Minimal existing-owner repair

`v7-governed-canary-dry-run-cycle` now preserves the already-validated
Matrix/OMP binding as the authoritative Packet binding. Only when that binding
does not exist does it retain the existing delegated-admission event fallback.
No new owner, policy, Authority, scheduler, Packet reuse or execution path was
introduced.

The regression test proves that an exact prevalidated active-incident binding
survives a delegated admission payload that has no duplicate event object.

## Verification and successor

Focused tests: `181 PASS` (`test_governed_canary_cli` and
`test_service_failure_episode`). The next required verification is a new
ordinary timer-owned Matrix generation after deployment. It must create a
fresh Packet with the current binding, then either produce the first valid
CT-M0F user-path sample or emit one exact live STOP_SAFE terminal. Manual
Matrix execution is not evidence and is not used.

No claim of CT-M0F completion, timing-SLO compliance, Authority expansion or
Production Maturity change is made by this repair.
