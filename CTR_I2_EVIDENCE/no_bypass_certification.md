# CTR.I2 No-Bypass Certification

CTR.I2 implements review-required semantics as informational governance evidence only.

Certified:

- review semantics cannot approve packets
- review semantics cannot deny packets
- review semantics cannot change selected moves
- review semantics cannot change restore barrier
- review semantics cannot change routing
- review semantics cannot change planner ranking
- review semantics cannot change candidate score
- review semantics cannot change governance authority

Evidence:

- `tests/unit/test_ctr_i2_review_required.py`
- `tests/unit/test_operator_decision_surface.py`
- `tests/unit/test_operator_execution_pipeline.py`
- `tests/unit/test_operator_execution_feedback.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Authority flags remain:

- approval_authority=none
- denial_authority=none
- packet_authority_changed=false
- governance_authority_changed=false
- execution_authority_changed=false
- restore_barrier_write_authority=none

