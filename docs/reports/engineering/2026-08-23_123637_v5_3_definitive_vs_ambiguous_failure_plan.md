# V5.3 — definitive vs ambiguous failure plan correction

**Date:** 2026-08-23 12:36 MSK  
**Mission effect:** existing Service Failure Program contract correction only.

## Summary

The current `V5.3 N0–N11 ROLE-BASED FAST RECOVERY ARCHITECTURE` now requires
an evidence-class tournament instead of forcing every hard-failure signal
through the same repeated source probe.

## Before

The active Program stated that all L0/L1/L2 signals created `SUSPECT` and every
hard/path signal required independent targeted Matrix corroboration before T0.
That preserved safety but could repeat a network probe after an exact fresh
owner-backed local fact had already proved interface, process, tunnel or route
failure.

## Program correction

The Program now distinguishes:

- `DEFINITIVE_LOCAL_HARD_FAILURE`: exact owner-backed, fresh, identity- and
  generation-bound local proof;
- `AMBIGUOUS_OR_REMOTE_FAILURE_EVIDENCE`: timeout, loss, generic liveness,
  Telegram/DNS/application/partial/quality evidence;
- `STALE / UNKNOWN / CONFLICTING / CORRELATED`: fail-closed revalidation or
  Full fallback, with no user movement.

N1 defines the exact predicates. N4 compares two modes on the same evidence:

- `MODE A`: repeat the source probe before Matrix T0;
- `MODE B`: Matrix validates exact definitive evidence and atomically records
  T0 without a redundant source network probe, while target readiness is
  checked independently and in parallel.

N7 must falsify both modes across real failure, transient, wrong-generation,
stale, replay, restart, correlated and recovery scenarios. Every hard-failure
class must finish with an explicit `MODE_A_RETAINED` or
`MODE_B_DIRECT_T0_ADMITTED` disposition.

## Ownership and safety

Matrix remains the only canonical health/state/T0 writer. L0 does not write
T0, select a target, grant Authority or apply a route. Direct T0 may skip only
the redundant source network probe; it cannot bypass target readiness,
Planner, Candidate, Packet, Lease, Barrier, Apply, verification or rollback.

Missing provenance, incomplete identity, stale/conflicting evidence or a
failed safety/equivalence result always returns the exact class to `MODE A` or
`SUSPECT` confirmation. No vendor default is adopted as a V7 setting.

## Evidence basis

- Existing V7 mature-system synthesis:
  `docs/reports/engineering/2026-08-21_100109_v5_3_bottleneck_to_mature_pattern_synthesis.md`.
- Existing Phase C/D/E decision:
  `docs/reports/engineering/2026-08-20_130000_v5_3_matrix_health_phase_c_d_e_decision.md`.
- Envoy active health supports immediate failure for an explicit owner signal:
  <https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking>.
- BFD defines low-overhead forwarding-path failure evidence consumed by a
  separate routing application:
  <https://www.rfc-editor.org/rfc/rfc5880.html>.

## Runtime and production effect

None. No Runtime, Matrix implementation, timer, cadence, route, client, state,
owner, Authority, CPS or OMP value changed. The correction adds a mandatory
future Polygon decision gate; it does not preselect direct T0.

## Validation and publication

- `git diff --check`: PASS before publication.
- Program contradiction scan: the former blanket `L0/L1/L2 -> SUSPECT only`
  rule is replaced by the gated certainty split; Telegram and all other
  ambiguous evidence still require independent confirmation.
- `tools/v7-truth-check --all --json`: CPS, OMP, local workspace and Runtime
  consistency PASS; zero internal contradictions; documentation-only Runtime
  mismatch accepted and no deploy required.
- Commit `83a02aad838200906127012f6863e78e5752e596` was pushed to
  `origin/Updatesystem` and independently resolved through the GitHub API.
- The truth-check GitHub sub-check remained `GITHUB_NO_GO` only because its own
  sandboxed remote read could not reach GitHub; the independent authenticated
  API read proved the exact published branch commit.

## Exact next step

The current Program frontier remains N0a. In the admitted N1/N4 work, inventory
the existing L0 producers and classify each observable fact by provenance,
freshness, source identity, generation continuity and conflict behavior; then
build the shared `MODE A` versus `MODE B` Polygon cases before changing Runtime.
