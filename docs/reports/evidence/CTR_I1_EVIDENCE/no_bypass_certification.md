# CTR.I1 No-Bypass Certification Evidence

CTR.I1 adds advisory evidence only.

Certified by tests:

- `tests/unit/test_ctr_i1_no_bypass.py`
- `tests/unit/test_v7_users_autoswitch_policy.py::V7UsersAutoswitchPolicyTest::test_ctr_advisory_is_visible_without_changing_candidate_score_or_selected_moves`
- `tests/unit/test_operator_decision_surface.py`
- `tests/unit/test_operator_execution_pipeline.py`

No-bypass verdicts:

- CTR cannot create selected moves.
- CTR cannot approve packets.
- CTR cannot write restore barrier.
- CTR cannot mutate runtime.
- CTR cannot bypass planner.
- CTR cannot bypass governance.
- CTR cannot bypass capacity.
- CTR cannot bypass batch controls.

Key guard:

`ctr_advisory` is exposed on planner candidates, but `ctr` is not added to `score_parts`.

Therefore:

- candidate score remains unchanged;
- selected move hash remains unchanged;
- selected moves remain unchanged;
- CTR remains advisory.
