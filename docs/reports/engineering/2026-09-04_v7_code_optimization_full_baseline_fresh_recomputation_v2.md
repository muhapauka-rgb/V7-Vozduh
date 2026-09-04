# V7 CODE_OPTIMIZATION FULL_BASELINE Fresh Recomputation V2

- Date: `2026-09-04`
- Intent: `CODE_OPTIMIZATION FULL_BASELINE`
- Mission: `V7_CODE_OPTIMIZATION_OPERATIONAL_FULL_BASELINE_SEMANTIC_CAMPAIGN_V1`
- Existing owner / profile / consumer: `OMP` / `CODE_OPTIMIZATION` / `mission_completion_evidence_gate`
- Mission intent fingerprint: `da82b2378ffbde81793c0fa2345b28ca981ddcea80be336de54214413991f289`
- Fresh campaign fingerprint: `513d2f6e250fbcd952f846c514289a2ad48c5c5e05b9eab5b16d2a021563c5a3`
- Source identity inspected: commit `ce0a8e52f64be42d8bb87e86df49106e3d8bd732`
  plus the preserved concurrent zero-or-one-cleanup contract change in
  `tools/v7_sync_lib.py` and its focused test
- Product frontier: unchanged, `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`
- Effects: CPS `NONE`; Runtime `NONE`; Production `NONE`; Authority `NONE`

## Outcome

The fresh compact caller produced three immutable executor packets and correctly
returned `CONTINUE_SAME_MISSION / SEMANTIC_EXECUTOR_REQUIRED`. The current Codex
executor inspected the packet-bounded source and current callers/consumers,
submitted three immutable results, and the existing completion consumer accepted
all three with `COMPLETE_WITH_LEGAL_TERMINAL`.

Final terminal:

```text
PASS
CODE_OPTIMIZATION_REAL_SEMANTIC_EXECUTOR_ACTIVE_AND_COMPACT_COMMAND_ACCEPTED
```

## Coverage and semantic classification

Coverage is `PARTIAL_OWNER_BACKED_COVERAGE`. All three currently admitted
owner-backed domains completed. Twenty-seven executable surfaces remain
localized `UNKNOWN` because the current owner/domain configuration does not
admit them into this bounded campaign; this is not repository-wide coverage.

| Domain | Inspected symbol and current consumer | Class | Removal or bypass result |
| --- | --- | --- | --- |
| `ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION` | `admin_core/operator_execution.py::execute_packet` and `runtime_recheck`; consumed by the current `tools/v7-users-autoswitch` packet/lease/barrier path and audit/lifecycle terminals | `SAFETY_ESSENTIAL` | replay, Runtime identity, lease/barrier, rollback and durable terminal equivalence is unproved |
| `OMP_EXECUTION_PROFILE_COMPLETION_LIFECYCLE` | `tools/v7_sync_lib.py::execution_profile_completion_binding`; consumed by `mission_completion_evidence_gate` | `SAFETY_ESSENTIAL` | fresh subgraph identity and immutable result/review identity are distinct safety facts |
| `OMP_CODE_OPTIMIZATION_MATERIAL_CHANGE_BRIDGE` | `code_optimization_material_change_admission`, owner resolver, anti-regrowth and `code_optimization_cleanup_proof_set_valid`; consumed by Continue OMP and the consolidated campaign | `SAFETY_ESSENTIAL`, `OBSERVABILITY_ESSENTIAL` | removal permits owner-mapping ambiguity, makes controlled private-allowlist recurrence invisible, or regresses the honest zero-or-one cleanup bound |

## Ranked hypotheses and counterfactuals

1. Narrow or bypass part of `execute_packet`: falsified because the current
   evidence does not preserve every deny path, barrier/lease identity, rollback,
   audit and S11-dependent terminal.
2. Collapse responsibility-subgraph and profile/result/review completion
   bindings: falsified because each rejects a different mismatch class.
3. Remove material-change anti-regrowth: falsified because the controlled private
   mapping recurrence would no longer reach `STOP_SAFE`.

No redundant link was proved. The campaign therefore consumed the honest result
`cleanup_count=0` and performed no physical cleanup. The current zero-or-one
validator rejects malformed or multiple cleanup proofs without forcing an
unproved cleanup.

Historical commit `6ca3395acc9e920b7b936b29923f88c5e5a86594` remains the
anti-regrowth baseline: it removed deterministic Python-authored semantic
classifications/PASS reviews and made fresh executor packets plus the external
Codex result mandatory. Current anti-regrowth confirms that neither the
hardcoded semantic helper nor a private FULL_BASELINE domain list has returned.

## Localized UNKNOWN and re-entry

- Recovery domain: fresh identity-bound Runtime/S11 behavioral equivalence is
  absent. Existing evidence owner is the normal V7 Runtime health caller with
  Matrix/S11 receipts. Re-enter on a matching real recovery event or material
  source/owner change.
- Completion lifecycle: the five immutable schema contexts are separate, but
  `model_level_independence_proven` remains `false`. Re-enter only if the owner
  contract requires and supplies externally executed reviewer receipts.
- Material-change bridge: a future unconfigured dependency has no current owner
  proof. Re-enter through `SYSTEM_MAP` and the existing OMP owner/domain
  configuration when such a path appears.

## Review separation and verification

- Domain submissions: `3/3 PASS`
- Completion verdicts: `3/3 COMPLETE_WITH_LEGAL_TERMINAL`
- Reviews per result: Architecture, Safety/Regression, Evidence,
  Quality/Complexity and Mission Integrity, all bound to the immutable output
  fingerprint and unable to modify the submission
- Review limitation: schema-context separation is proved; independent
  human/model judgment is not claimed
- Hypotheses / attempts: `3 / 3`
- Cleanup proof count / limit: `0 / 1`; source mutation by this invocation:
  `FALSE`
- Existing-owner material mapping anti-regrowth: `PASS`
- Owner-backed domain discovery anti-regrowth: `PASS`
- Focused regression: `79 tests`, `PASS`
- `tools/v7-truth-check --local --json`: `NO-GO` at the workspace gate with
  `branch_mismatch`, `workspace_mismatch`, `dirty_workspace` and
  `runtime_critical_dirty`. This task runs in a detached Codex worktree and two
  concurrent, non-campaign source/test changes remain preserved and uncommitted;
  Runtime/state truth was therefore `NOT_CHECKED`
- `git diff --check`: `PASS`
- Report publication: intentionally not committed or pushed in this task because
  doing so must not absorb or misrepresent those concurrent source/test changes

## Exact continuation

The bounded baseline Mission is complete. The smallest lawful next command is:

```text
CODE_OPTIMIZATION CHANGED <exact-material-path>
```

only after a material dependency changes. A deliberately requested fresh
recomputation may use `CODE_OPTIMIZATION FULL_BASELINE` again. The existing OMP
owner and current owner/domain configuration remain the only scope producer;
no Program, owner, queue, registry, planner, Runtime truth source or Authority
was added.
