# E28 Blast Radius Model

date_utc=2026-05-29T06:18:00Z

## Four User Blast Radius

blast_radius=4
allowed_users=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15
allowed_target=amneziawg-exec-20260528-10-8-1-14
rollback_target=1
allowed_route_tables=1009,1010,1012,1013
unrelated_users_touched=false
bounded_scope_model=true

## Five User Blast Radius

blast_radius=5
allowed_users=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15
candidate_user_5=NONE
five_user_model_executable=false
reason=no_fifth_enabled_user_on_rollback_target_1_selected_for_clean_small_cohort

blast_radius_model_safe=true
blast_radius_execution_blocked_by_capacity=true

