# V7 recovery-latency rewrite — execution report

Date: 2026-08-29  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_RECOVERY_LATENCY_REWRITE`

## Executed result

The current Program contract was corrected in place. No new Program, Runtime,
Matrix owner, Planner, timer, queue, registry or state source was created. No
production route, assignment, cadence or verifier was changed.

The correction adds an immutable incident clock and makes the product KPI span
the complete affected scope:

```text
T_FIRST_VALID_FAILURE_OBSERVATION
-> T0 (canonical Matrix ACTIONABLY_FAILED)
-> GLOBAL_ALL_AFFECTED_RECOVERED / last-member S11
```

The binding production target is now first-valid-observation to last-member
S11 P95 `<=7000 ms`, with an absolute ceiling of `8000 ms`. A later Matrix
regeneration, per-user retry, Packet creation or operator rerun cannot reset
the clock. The prior `T0 -> S11` clock remains decomposition evidence only.

## Why the correction was required

The latest live evidence showed that the first VLESS failure observation was
followed by completion at approximately 25 minutes for the first client and
1 hour 41 minutes for the second. The prior contract could measure from a
later actionable event and therefore did not bind the complete user-visible
delay. The new contract makes those outcomes unambiguously fail the production
recovery SLO.

## Program changes

- Added `T_FIRST_VALID_FAILURE_OBSERVATION`, `T0`, and `T_END` definitions.
- Defined `CURRENT_AFFECTED_SCOPE` from fresh current assignment and required
  service truth.
- Made the last affected member, not the first member, the product terminal.
- Added a separate observation-to-T0 budget and prohibited clock reset by
  regenerated events.
- Reconciled N0, N7, N8, N10 and the final N-terminal criteria.
- Required compatible members to use one bounded cohort operation; one-user
  serialization is allowed only for a proven safety conflict.
- Required recurring synchronous spans over 100 ms to be owner-classified or
  moved after the minimum durable recovery receipt.

## CPS/OMP and Runtime reconciliation

`tools/v7-truth-check --all --json` returned CPS/OMP consistency `PASS` and
local branch `Updatesystem` at `644f6a5a`. The check returned overall `NO-GO`
because the new Program edit is intentionally unstaged at this report point,
GitHub remote verification was unavailable, and the live Runtime remains at
the previously deployed commit `2b4e86896aab1a43b0399537b7f6c227e55fd26d`
while local runtime-relevant commits include an undeployed gate change. This
was not silently deployed or overridden.

## Current implementation gaps found

1. The live outcome records contain `observed_at`, operation and verification
   times, but do not persist individual Candidate/Packet/Lease/Barrier
   timestamps or one immutable incident-start-to-last-member receipt.
2. The observed production incident was executed one user per transaction;
   the Program now requires a bounded cohort transaction for compatible users.
3. The largest delay is before the governed operation becomes actionable
   (about 103–104 seconds after the latest bound event), followed by a
   4–5-second route-writer interval dominated by audit work. Kernel route
   mutation itself was only 70–100 ms.

## Ordered next frontier

1. Extend the existing Matrix/L3 incident projection and execution receipt to
   carry the immutable first-valid-observation timestamp and exact phase
   timestamps, without adding a state owner.
2. Prove the existing automatic consumer can reconcile the complete current
   affected scope as one bounded cohort and record first/last member times.
3. Move only non-safety audit work after the minimum durable recovery receipt;
   preserve rollback preimage and required S11 evidence before completion.
4. Run focused Polygon falsification, safe-deploy gate and one controlled
   end-to-end sample before any broader production claim.

This block is a contract correction plus read-only reconciliation. Runtime
implementation and deployment remain pending the existing owner-backed
frontier and safe-deploy evidence.

## Verification in this turn

- Markdown/program diff check: `PASS`.
- Python AST parse of `tools/v7-users-autoswitch` and
  `admin_core/operator_execution_pipeline.py`: `PASS`.
- The repository has no installed `pytest` command. The equivalent unittest
  profile started, but it was stopped after the legacy suite exceeded the
  bounded execution window and showed unrelated failures; it is not counted
  as a passing regression gate.
- No Runtime or production mutation was performed from this document-only
  correction.
