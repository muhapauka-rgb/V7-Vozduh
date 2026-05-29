# E28 Cohort Rollback Model

date_utc=2026-05-29T06:18:00Z

rollback_target=1

rollback_manifest:
- 10.7.0.11 -> 1 / table 1009 / expected_dev=v7e356a192b79
- 10.7.0.12 -> 1 / table 1010 / expected_dev=v7e356a192b79
- 10.7.0.14 -> 1 / table 1012 / expected_dev=v7e356a192b79
- 10.7.0.15 -> 1 / table 1013 / expected_dev=v7e356a192b79

rollback_order=sequential_exact_user_order
rollback_completeness=all_selected_users_have_current_rollback_target_1
route_restoration_model=restore_each_user_route_table_to_default_dev_v7e356a192b79
rollback_audit_required=true
rollback_verification_required=true

cohort_rollback_safe=true
notes=rollback is model-safe for four selected users; execution remains blocked until capacity is requalified.

