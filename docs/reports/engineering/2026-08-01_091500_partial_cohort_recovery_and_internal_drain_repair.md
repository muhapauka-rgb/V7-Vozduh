# V7: восстановление неполной когорты и внутренний drain

Date: `2026-08-01`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Evidence class: production owner discovery plus local engineering verification. This report is historical evidence; CPS owns live state.

## Root cause

The current availability-first Stage 25 was not blocked by infrastructure or
Authority. Fresh production owners show `awg3` is `HEALTHY`, has an
ordinary-user-protected safe capacity of `112`, and the active standing
contract `sdpc_285af5fc6f4de20415c3e5b1` permits a scope through `48`.

The interrupted Stage 25 recorded 24 verified forward Packet terminals and
one `STOP_SAFE` member. The existing Matrix correctly refused to append a
Stage 25 receipt. Its recovery consumer then incorrectly required all 25
members to be successful before it would reset the members still outside the
baseline. This left the successful partial cohort unreconciled and prevented a
fresh Stage 25 plan.

## Repair

`tools/v7-governed-canary-dry-run-cycle` now recognizes
`PARTIAL_COHORT_BASELINE_PENDING`. It reuses only existing Matrix event,
Packet/audit, route, switch and Outcome/Replay/Learning owners to reset one
verified member at a time. It neither credits nor resets an unexecuted member.
After the successful partial members reach baseline, the same existing Matrix
invocation returns to fresh planning for Stage 25; a receipt remains forbidden
until a completely verified new cohort exists.

The existing bounded successor loop already drains a cohort internally. The
repair preserves the current one-at-a-time Packet/lease safety bound while
removing the artificial need for another Matrix wake between recovery members
or between recovery and a fresh plan.

## Verification before deploy

- targeted partial-cohort recovery regression: PASS;
- affected governed executor, service-failure and Packet policy suites:
  `222/222 PASS`;
- no production action occurred during discovery or testing;
- no Authority, policy, ordinary-user assignment, routing, L8 credit or
  Production Maturity change occurred.

## Production continuation contract

After safe deploy, only the existing Matrix-owned governed execution path may
consume this repair. It must first restore the currently owner-proven partial
members, then use a fresh Candidate/Packet/lease for Stage 25. No old Packet,
lease, allocation or receipt may be reused. Stage 48 is evaluated only after
the Stage 25 receipt is owner-backed and consumed.
