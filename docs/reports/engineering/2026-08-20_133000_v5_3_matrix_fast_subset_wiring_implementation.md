Mission ID: `V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`
Run Nonce: `v53_fast_subset_wiring_20260820`

# V5.3 Matrix exact subset wiring implementation

Status: `IMPLEMENTATION_COMPLETE_VALIDATED_DEPLOY_PENDING`

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
was added. No synchronous full work is removed yet: the next exact step is
safe deploy followed by a production read-only bounded invocation and
before/after timing/probe-count comparison. Automatic role-aware scheduling is
not claimed by this Mission; it remains the next bounded consumer-wiring
residual only after production observation validates this primitive.

## Effects

- Source behavior: changed, opt-in bounded selector mode added.
- Default Runtime behavior before deploy: unchanged.
- Production effect: pending safe deploy.
- Routing/user/apply/policy/Authority effect: none.
- Rollback: deploy previous canonical tool version or invoke with empty
  selectors to use the existing full Matrix path.

