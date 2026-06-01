# PROGRAM Z3.2 Multi-Candidate Test

## Objective

Test multiple candidates, multiple targets, competing proposals, budget enforcement, and selection correctness.

## Live Evidence

The live Z3.2 apply was intentionally filtered:

- user filter: `10.7.0.16`
- target filter: `awg3`
- budget: `1`
- selected_moves: `1`

No cohort or batch movement was allowed.

Prior unfiltered governance evidence from Z3.1 showed the planner could see a larger candidate space while the governance gate still prevented unsafe apply:

- unfiltered candidates were not promoted to an apply.
- selected movement for Z3.2 remained exactly one user.

## Unit-Level Evidence

`tests/unit/test_v7_autoswitch_proposal_cap.py` verifies:

- raw candidate moves can exceed one.
- budget reduces proposal to the allowed count.
- held current egress candidates are excluded.
- unsafe shadow apply requests fail closed.

`tests/unit/test_v7_users_autoswitch_policy.py` verifies restore-stage approval limits selected moves.

## Verdict

- multiple_candidate_awareness=true
- budget_enforced=true
- selection_bounded_to_one=true
- competing_proposals_not_applied=true
- multi_candidate_handling_certified=true

