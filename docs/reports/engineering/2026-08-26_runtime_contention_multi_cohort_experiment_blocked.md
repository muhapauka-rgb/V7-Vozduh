# Runtime contention and multi-cohort failover experiment: safe precondition block

**Mission:** `V7_RUNTIME_CONTENTION_AND_MULTI_COHORT_FAILOVER_EXPERIMENT`  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Status:** `STOP_SAFE_PRECONDITION_BLOCKED`  
**Date:** 2026-08-26

## What was reconciled

The current Runtime is unchanged from the frozen HARD_PATH campaign:

- local repository is clean at `1e517bfa` (documentation-only commit after the
  frozen implementation);
- the performance implementation fingerprint remains
  `4b13e1475addd1a9a94a7edbf2736e45fb72c99c86ad91be7debd39c968a0eb1`;
- `v7-health.service` is active with exit status 0;
- the standalone Matrix and Telegram timers are inactive as intended;
- the only exact isolated CT-M0F identity, `10.7.0.124`, is back on
  `amneziawg-exec-20260528-10-8-1-14`, table `1122`,
  `default dev v7execwg0`;
- no CT-M0F reservation remains active.

No code, configuration, cadence, priority, verifier, Planner, Matrix,
Authority or route semantics were changed while evaluating this mission.

## Blocking facts

### 1. The frozen CT-M0F evidence budget is exhausted

The current owner-backed policy reports:

- 5 valid samples;
- 1 cold and 4 warm;
- 5 owner-backed Matrix generations;
- 0 invalid or safety-stopped attempts;
- 0 active reservations;
- `valid_sample_budget_exhausted = true`;
- next sample kind would be warm.

Starting Phase A's required 15 additional samples would therefore require a
new policy admission or a changed contract. That would no longer be the frozen
campaign requested by the prompt.

### 2. The current substrate has only one safe isolated failure source

`amneziawg-exec-20260528-10-8-1-14` is the only source currently bound as an
isolated `EXECUTION_ONLY` CT-M0F source with the exact one-user reservation.
The other certification identities are distributed over shared channels:

- `wireguard-1779454504-c43409` contains certification identities and other
  non-certification users;
- `vless` contains a non-certification identity;
- the remaining `awg0`/`awg3` certification pool is shared with the normal
  routing population.

Injecting a failure into those shared sources would violate the mission's
  explicit no-ordinary-user-effect requirement. Treating them as isolated by
  label would be unsafe and would not be evidence of a valid multi-cohort
  failover.

## Consequence for the requested phases

- Phase A quiet/moderate/back-to-back cannot be completed under the current
  CT-M0F contract because its valid-sample budget is exhausted.
- Phase B B1 can be represented by the already completed one-source evidence,
  but B2 and B3 cannot be run safely because there are not two or three
  independent isolated failed sources.
- The 2x300 and 3x300 cells cannot be credited by multiplying identities on
  shared sources; that would test ordinary-user impact and violate the
  controlled-failure contract.
- No conclusion about spacing correlation, scheduler contention, or
  multi-cohort serialization is claimed from this blocked state.

## Exact next action required

The smallest safe continuation is an owner-level precondition decision, not a
performance patch:

1. admit a new bounded diagnostic policy/campaign budget for the frozen
   implementation, and
2. provide at least two additional isolated certification-only source
   reservations (or an existing equivalent multi-source Polygon fixture), with
   no ordinary users on those sources.

After that external precondition exists, restart the affected comparison set
from Phase A on one immutable fingerprint, then proceed to B1/B2/B3. Until
then, continuing would either exceed the current Authority/contract or inject
failures into shared channels, so the mission remains safely stopped.
