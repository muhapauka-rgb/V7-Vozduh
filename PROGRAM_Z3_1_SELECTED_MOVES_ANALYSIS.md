# Program Z3.1 Selected Moves Analysis

Date: 2026-06-01

## Verdict

selected_moves_understood=true

## Why candidate_moves=12 But selected_moves=0

Unfiltered planner:

- candidate moves: `12`
- selected moves before guard: `3`
- clearance max selected moves: `0`
- selected moves after guard: `0`

The planner generated selected moves internally, then the restore barrier budget guard removed them.

## How Selected Moves Are Generated

The planner:

1. Computes decisions for active users.
2. Selects eligible switch decisions according to planner policy and limits.
3. Applies restore barrier clearance guard.
4. Emits `selected_moves`.

## Budget Interaction

With initial barrier:

`clearance_max_selected_moves=0`

Therefore any selected movement is denied.

With Z3.1 filtered clearance:

`clearance_max_selected_moves=1`

Filtered planner can pass one selected move only if generation, hash, count, and TTL match.

Unfiltered planner remains blocked:

- selected moves before guard: `3`
- max: `1`
- selected moves after guard: `0`

This proves scope did not expand.

