Mission ID: `V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`
Run Nonce: `v53_fast_subset_wiring_20260820`

# V5.3 Matrix exact subset wiring implementation

Status: `IMPLEMENTATION_DEPLOYED_PRODUCTION_FAIL_CLOSED_OBSERVED`

## Admission

The completed read-only Mission selected `TARGET_ARCHITECTURE_MODEL_B_PLUS_C`
and confirmed the smallest residual as
`CONNECT_EXISTING_EXACT_SERVICE_SUBSET_AND_EXACT_EGRESS_SELECTION_TO_REFRESH_ALL_FAST_SOURCE_TARGET_PATH`.
The existing atomic CPS owner admitted this Mission as
`cpsgen_SFA_V53_FAST_SUBSET_ADMITTED_1`; the existing V5.3 lifecycle binding
returned `MISSION_EXECUTION_ALLOWED`. Admission itself had no Runtime,
Production or Authority effect.

## Change

`tools/v7-service-matrix-refresh-all` now accepts two optional, fail-closed
selectors:

- `--egresses`: exact comma-separated identities resolved only against the
  existing enabled `egress.registry` owner; unknown, disabled or malformed
  identities stop before probes;
- `--services`: exact comma-separated subset forwarded to the existing
  `v7-service-matrix-test --services` mechanism.

Empty selectors retain the previous full refresh byte-for-byte at the command
boundary. Bounded mode still uses the existing per-egress tester, Matrix writer
lock, atomic row update, persistence, event producer and downstream consumer
chain. `probe_selection` records the bounded selection and explicitly names
the full Matrix fallback. Event-consumption-only mode rejects probe selectors.
Role selection remains with the existing caller/Matrix/Planner boundary; this
Mission does not infer roles or create another registry, writer, state store,
event system, route action or user loop.

The OMP/CPS lifecycle repair adds only V5.3 specializations of the existing
pure lifecycle validator. Prepared read-only state cannot execute; atomic
`MISSION_ADMITTED` is required. The implementation Mission likewise requires
the consumed Phase C/D/E terminals and exact CPS identity before returning
`MISSION_EXECUTION_ALLOWED`.

## Validation

- Python compilation: PASS (isolated bytecode cache).
- 17 focused tests: PASS.
- Exact service subset reaches the existing checker command: PASS.
- Exact enabled egress selection: PASS.
- Disabled/unknown and malformed egress fail closed: PASS.
- Default full-refresh path preserved: PASS by unchanged empty-selector
  command construction and existing lock-owner regression test.
- Event-only plus probe selector rejected: PASS by code contract.
- Existing RS7 lifecycle isolation regressions: PASS.
- Production binary hashes equal the canonical local hashes: PASS.
- Canonical safe-deploy post-check invokes an unknown exact egress and requires
  return code `2` plus `exact_egress_subset_not_enabled`: PASS; the command
  terminates before any service probe or Matrix write.
- Runtime mutation, route change, user movement and Authority expansion during
  validation: NONE.

## Current-to-target and residue

```text
CURRENT full enabled-egress/all-service refresh
-> optional exact egress + existing exact service subset
-> unchanged Matrix writer/state/event consumer chain
-> full refresh fallback when selectors are empty
```

No duplicate Matrix writer, health truth, queue, watcher, Runtime or Planner
was added. The bounded primitive and its fail-closed production boundary are
deployed. No synchronous full work is removed yet: the next exact step is to
connect the existing role-selection consumer, then run an authoritative valid
bounded source/hot-target invocation and compare elapsed time and probe count
against the full fallback. Automatic role-aware scheduling is not claimed by
this Mission; it remains the next bounded consumer-wiring residual.

## Effects

- Source behavior: changed, opt-in bounded selector mode added.
- Default Runtime behavior: unchanged when selectors are empty.
- Production effect: opt-in bounded selectors deployed; production hash
  convergence and no-probe fail-closed post-check observed under the existing
  safe-deploy owner.
- Routing/user/apply/policy/Authority effect: none.
- Rollback: deploy previous canonical tool version or invoke with empty
  selectors to use the existing full Matrix path.

## Deployment evidence

- Initial implementation commit: `0d546abd92fde5e1544a07f712c29929aded6ab8`.
- Initial deploy: `deploy-z8-14-Updatesystem-0d546ab-20260820T134716`.
- Production `v7-service-matrix-refresh-all` SHA-256:
  `9e2b078a0bcaee973c51728c114971008241d1653bfc056b7174153ae5936379`.
- Production `v7_sync_lib.py` SHA-256 before durable post-check addition:
  `18a91430bdf9be5fa295d573973bca1c75f5fb32c620ba8ee0368ef36a008573`.
- Safe-deploy convergence: `PASS`, blockers `[]`, GitHub `GITHUB_ALIGNED`.
