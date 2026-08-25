# Persistent owner evidence baseline: authority terminal

Date: 2026-08-25 (MSK)  
Scope: `PERSISTENT_EXISTING_OWNER_PREPARED_VALIDATION_RUNTIME` evidence block.  
Result: `STOP_SAFE_AUTHORITY_BOUNDARY_NO_CREDITED_HARD_SAMPLE`.

## Objective and outcome

The task was to restore one lawful synthetic source-to-distinct-target baseline,
then collect the frozen persistent-Matrix HARD-path evidence.  The source,
Matrix, prepared-target observations, service process, and isolated synthetic
identity were made current.  The exact target-selection owner nevertheless
returned no admitted target.  A fresh controlled source failure proved that
this is not stale state: the active policy has no authority for
`ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET` and explicitly reports
`GENUINE_AUTHORITY_EXPANSION_REQUIRED`.

No credited HARD-path sample exists for this block.  No ordinary user was
moved, no ordinary route changed, and the synthetic source was restored.

## Bounded repairs made

1. `2d4606e6` — the persistent Matrix consumer now consumes one canonical T0
   at most once per health-process invocation.  This prevents a continuing
   incident from creating repeated certification attempts without a new
   failure generation.
2. `64a759f9` — the existing safe-deploy owner now requires an explicit
   health-service restart whenever its in-process dependency set changes.
3. `1b6141ef` — a performance fingerprint now includes the systemd health
   invocation identifier when Matrix runs inside that owner.  A copied file
   cannot be confused with an older in-memory process image.

Focused verification passed: 14 health-loop tests, 257 service-failure and
governed-cycle tests, and 232 operator-execution tests.  Deploys passed their
existing safe-deploy and GitHub-alignment gates.  Final deployed commit:
`1b6141efd031f10e61c6d946c52511c684dcbbf9`; deploy:
`deploy-z8-14-Updatesystem-1b6141e-20260825T232145`.

## Runtime evidence

- `v7-health.service`: active after the deploy; systemd invocation
  `b3fd30098abd4a09af4d16a4d524426d`.
- Old standalone Matrix and Telegram timers: inactive as intended.
- Synthetic identity: `10.7.0.124`, certification-only group
  `ctm0f-9765f296cbe9`.
- Isolated source: `amneziawg-exec-20260528-10-8-1-14` / `v7execwg0`.
- Prepared target observation (owner-selected): `awg0`, `awg3`; both Matrix
  observation results were OK.  This observation had no downstream consumer,
  routing mutation, or user movement.
- Exact fresh failure was injected only through `v7-egress-set-state` with the
  existing source reservation `n10-20260823-1508`.  Matrix produced fresh
  incident `sfinc_9db8508a4bbb13bda78fd5bcf7fdfe18`.
- Selection then returned
  `STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED` with
  `no_distinct_controlled_contract_admitted_target`; its policy projection
  states `GENUINE_AUTHORITY_EXPANSION_REQUIRED`.
- Cleanup restored `v7execwg0` and wrote canonical recovery
  `sre_4032e090cfb4773f6e18e2cacb09f679`; final interface state was UP and
  health service active.

## Why this is a real boundary

The owner has fresh health and capacity evidence for targets, but its current
policy permits no certification-only assignment to either.  Selecting `awg3`
manually, widening eligibility, or rewriting the action policy would violate
the current Mission.  This is therefore not a performance failure and not a
reason to produce a synthetic SLO result.

## Exact next action

An owner must either:

1. issue a bounded, expiry-backed authority contract for exactly one
   certification-only identity and an owner-selected healthy target with zero
   ordinary-user effect; or
2. explicitly retain the present policy, which leaves the persistent-owner
   HARD-path evidence block unmeasurable.

After option 1, re-run fresh Matrix prepared-target observation, one cold
sample, and only then the frozen five-sample series.  Do not start Telegram,
N10, or N11 from this terminal.
