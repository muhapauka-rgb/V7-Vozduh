# Controlled certification: scope separation and exact-source boundary

Date: 2026-08-01  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Verdict: `EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED`

## Reuse and semantic result

The existing controlled-certification path is already separate from the
natural service-failure incident path.  Its admission is based on the
approved controlled-substrate/campaign binding, certification pool, exact
source isolation, healthy baseline, target allocation and fresh live gates.
`CURRENT_SOURCE_SCOPE_EMPTY` therefore does **not** credit or close controlled
certification; nor does it by itself block an otherwise valid controlled
campaign.

Natural provenance remains separate.  A deliberate controlled condition is
classified `CONTROLLED_PRODUCTION`; it cannot create Natural L8 credit.

## Current live blocker

The exact currently approved controlled source has the owner-backed state
`STOP_SAFE_SOURCE_BASELINE_UNHEALTHY`.

- controlled-substrate decision is recorded as approved;
- certification pool readiness is not the limiting criterion;
- deliberate condition and campaign execution remain forbidden until a fresh
  healthy baseline exists on that exact source;
- the existing owner names the missing dependency as the remote peer or
  matching profile/key material for that source;
- moving the campaign to another source would be
  `REBIND_CONTROLLED_CERTIFICATION_SOURCE`, an independent Authority action.

Neither a natural incident, a manual Matrix call, a synthetic outage nor a
source replacement is an authorized substitute for this precondition.

## Effects and verification

No Candidate, Packet, lease, restore-barrier write, Runtime apply, route/user
mutation, rollback apply, policy write, Authority expansion, Production
Maturity change or Natural L8 classification occurred.

Focused existing contract test verified the controlled-substrate approval,
source-isolation and healthy-baseline gate ordering.  The existing preflight
remained `STOP_SAFE` and performed no mutation.

## Exact automatic re-entry

Existing source/Matrix baseline owner records a fresh healthy baseline for the
same Authority-bound source
→ existing controlled-condition owner may prepare the condition
→ existing T48-M8/T48-M9 campaign owners may re-enter progressively.

No CPS or OMP semantic update is made here because their current projection
already represents this exact boundary.
