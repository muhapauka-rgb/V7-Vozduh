# V7 Code Optimization V1 Phase 3 — repeatable profile and anti-regrowth acceptance

Date: 2026-09-04
Terminal: `CODE_OPTIMIZATION_V1_REPEATABLE_AND_ANTI_REGROWTH_ACTIVE`

## Outcome

Phase 3 is complete. OMP now owns a repeatable material-change path into the
existing bounded `CODE_OPTIMIZATION` profile. The implementation reuses the
current subgraph producer, external Codex reasoning boundary, immutable submit
CLI, independent review binding and `mission_completion_evidence_gate`. No new
Agent System, owner, coordinator, queue, daemon, registry, Runtime, Planner,
truth source, Authority or product frontier was created.

The durable contract is section 28 of
`docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md`. It defines owner/model
boundaries, responsibility and semantic classifications, bounded hypothesis
generation, ranking, CONTROL/counterfactual proof, four reviews, anti-regrowth
and exact terminal consumption.

## Second substantive domain and cleanup

The accepted second responsibility domain is
`OMP_CODE_OPTIMIZATION_MATERIAL_CHANGE_BRIDGE`, entered only by
`CLI_FLAG:--continue-omp-change`. Its real caller is
`tools/v7-truth-check --continue-omp --continue-omp-change …`; its OMP consumer
is `continue_omp_engineering_control_loop`; its immutable result consumer is
`tools/v7-truth-check --omp-code-optimization-submit - --json` followed by
`mission_completion_evidence_gate`.

CONTROL found a private hardcoded material-path allowlist inside
`code_optimization_material_change_admission`. The counterfactual reused
`_responsibility_subgraph_domain_config` as the current owner/domain mapping.
The hardcoded allowlist was removed. Report/prompt/test-only paths remain
non-material; ownerless or ambiguous material input remains local `STOP_SAFE`.
The cleanup changes no production behavior, Runtime route, CPS, user or
Authority state.

## Continuous anti-regrowth

`code_optimization_bridge_anti_regrowth` is consumed by the real material-change
admission before profile admission. It structurally rejects recurrence of the
removed private allowlist and also rejects bypass of the existing owner/domain
resolver. `continue_omp_engineering_control_loop` has an exact fail-closed
terminal `CODE_OPTIMIZATION_ANTI_REGROWTH_VIOLATION` for this rule.

Controlled recurrence evidence uses a synthetic admission function containing
the removed `allowed = {...}` mechanism. Result: `STOP_SAFE`, recurrence true,
private allowlist true. Current-source evidence: `PASS`, private allowlist false,
existing resolver consumed true. No persistent anti-regrowth store was added.

## Actual end-to-end evidence

Actual caller run:

```text
tools/v7-truth-check --continue-omp --continue-omp-change tools/v7_sync_lib.py --json
```

Result: `PASS`; program terminal
`CODE_OPTIMIZATION_READ_ONLY_ADMISSION_READY`; fresh second-domain subgraph;
anti-regrowth `PASS`; exact submit consumer returned; four-review profile
admitted. Change fingerprint:
`aa22d547b2b7b122f1cc169e75137c5ef23e8495f818ccbfedddb88767150065`.

Actual immutable submit used the existing CLI with the disposable evidence
package. Result: `PASS`; completion
`COMPLETE_WITH_LEGAL_TERMINAL`; responsibility-subgraph and execution-profile
bindings consumed; Architecture, Safety Regression, Evidence and
Quality/Complexity reviews all `PASS`. Result fingerprint:
`c162dc38bc9dd6509aec31fc33537c24a74d4c9f67e6916a78edccf2919d6452`.

The post-cleanup semantic terminal was honestly
`NO_SAFE_COUNTERFACTUAL_CANDIDATE`: the proven cleanup was already applied and
no further evidence-backed removal was claimed.

## Verification and boundary

- Focused Code Optimization/profile/subgraph tests: 18/18 PASS, including the
  second domain, four-review admission and controlled recurrence consumption.
- Expanded adjacent OMP/Polygon regression: 110/110 PASS before the final
  recurrence-consumer assertion; no responsibility-path interception found.
- Existing actual OMP caller: PASS.
- Existing actual submit/completion consumer: PASS.
- `git diff --check`: PASS.
- CPS, Runtime, production, routing, user movement and Authority impact: NONE.

The active product frontier remains
`V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`; it was neither executed
nor displaced. Unrelated dirty worktree changes are not claimed by this report.

## Exact successor

No Phase-3 implementation residue remains. Future OMP-owned material changes
re-enter through the existing material-change bridge; recurrence of the removed
mapping stops safely at its existing consumer. Product execution continues only
through the already-active product frontier and its existing owner.
