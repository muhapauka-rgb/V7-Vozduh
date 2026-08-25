# CT-M0F: dynamic target binding and frozen controlled sample

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Scope:** certification-only identity `10.7.0.124`; no ordinary-user scope

## Outcome

The controlled transaction can now keep its source and reservation protected
while allowing the existing Matrix/Planner owners to select the target *after*
T0.  This removed the prior false stop caused by a target selected before the
controlled failure no longer matching the target selected by the live Matrix.

One cold end-to-end sample completed automatically and was then safely reset.
It is functionally valid, but it **fails** the current hard-path performance
acceptance: `7,365.186 ms` total exceeds both the `3,000 ms` P95 objective and
the `5,000 ms` individual ceiling.  It must remain in the frozen distribution.

## Minimal implementation and deployment lineage

| Commit | Change | Verification |
|---|---|---|
| `15f8302f` | Added `POST_T0_OWNER_SELECTED` transaction binding.  The existing owner still binds and validates the exact post-T0 target; no target is manually chosen and no second owner exists. | CT-M0F focused 2 pass; service-failure CT-M0F 22 pass; policy 199 pass; governed CLI 141 pass. |
| `2b49ec66` | Passed the existing audit store into controlled reset reconciliation. | Focused suites passed; safe deploy passed. |
| `9b9fece7` | Propagated the same audit store to the existing apply child. | Focused suites passed; safe deploy passed. |
| `8b493852` | Reused the current bounded lineage checkpoint when historical audit segments had rotated.  This is an existing audit owner and checkpoint, not historical scanning or new persistence. | Governed CLI 141 pass; policy 199 pass; safe deploy passed. |

The current local commit is `8b493852a3be07c1a7907c4302a62d6e9b75350a`.
The safe-deploy gate had already verified publication and Runtime alignment for
that commit.  The deployed host does not retain a Git worktree, so its active
implementation was verified through the safe-deploy fingerprint, service state
and governed evidence rather than `git rev-parse` on the host.

## Controlled evidence

| Property | Evidence |
|---|---|
| Source baseline | `amneziawg-exec-20260528-10-8-1-14`, table `1122`, interface `v7execwg0` |
| Post-T0 target | Selected by existing Matrix/Planner owner; no manual substitution |
| Failure onset | monotonic `9619663961056564 ns` |
| T0 to decision | `5,637.899 ms` |
| Decision to Apply admission | `175.812 ms` |
| Assignment commit | `847.633 ms` |
| Kernel route visibility | `28.286 ms` |
| Route identity to required-service proof | `675.556 ms` |
| Total onset to control-plane/kernel S11 | `7,365.186 ms` |
| Evidence ID | `ctm0ffwd_2297edbce5baab4381c1ef57` |
| Sample terminal | `ctm0fsampleterm_8910369aa057897830942de9` |

The evidence records `FUNCTIONALLY_VALID_PERFORMANCE_FAIL` with the two exact
reasons: above `3,000 ms` and above `5,000 ms`.  Route assignment, kernel
visibility, target identity and required-service proof all passed.  This is
therefore a genuine functional sample, not an invalid measurement.

## Safety and cleanup

- Only the certification identity moved during the controlled transaction.
- The existing `v7-user-switch` remained the sole route writer.
- No new Matrix owner, Planner, timer, registry, queue, state source or
  Authority was added.
- The transaction terminal is `L3_PRODUCTION_PROVEN`; the sample terminal says
  `verified_cutover_and_baseline_reset_complete`.
- After reset, `10.7.0.124` is again assigned to its isolated source and its
  table `1122` has `default dev v7execwg0`.
- `v7-health.service` is `active/running` with main status `0`.
- Legacy standalone Matrix and Telegram timers remain inactive as intended.

## Interpretation and exact next frontier

The dynamic-target defect is closed.  The limiting interval is now the
post-failure decision path, not source binding, route application or
verification.  No further hard-path optimization is admitted by the current
owner decision.

The next Program action is a **frozen homogeneous evidence series** on this
same implementation: four further functionally valid certification-only
samples (at least two warm, across at least two owner-backed Matrix
generations), with no code, configuration, cadence or semantic changes.  The
current valid cold sample must be included.  Because it already exceeds the
individual `5,000 ms` ceiling, that series cannot pass the 3-second contract;
its purpose is to quantify the stable distribution and then emit the allowed
terminal `HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED` with the measured gain of
the persistent Matrix consumer.  It does not authorize another micro-patch.
