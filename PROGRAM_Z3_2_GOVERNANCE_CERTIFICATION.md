# PROGRAM Z3.2 Governance Certification

## Governance Chain

1. Live planner selected the candidate.
2. Runtime generation and selected move hash were captured.
3. Clearance was bound to exact user, exact target, exact selected hash, exact generation, and budget `1`.
4. Fresh recheck verified generation and budget.
5. Existing autoswitch apply authority executed the one selected movement.
6. Existing route verification checked the movement.
7. Existing rollback authority restored the user.
8. Existing runtime checks verified final state.
9. Replay was blocked by generation mismatch and cooldown.

## Evidence

- pre_generation_id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- pre_selected_hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- guard: `restore_barrier_clearance_budget_and_generation_ok`
- apply selected_moves: `1`
- rollback restored users hash to pre-move hash
- final route/reconcile/killswitch rc: `0`, `0`, `0`

## Governance Caveat

The repo hybrid approval contract is present and tested, but Z3.2 did not add a new runtime integration between that Python validator and live movement. The live certification used the existing generation-bound clearance mechanism and existing planner/apply authority.

## Verdict

- planner_certified=true
- proposal_certified=true
- approval_generation_binding_certified=true
- runtime_recheck_certified=true
- execution_certified=true
- rollback_certified=true
- observation_certified=true
- replay_block_certified=true
- governance_certified=true

