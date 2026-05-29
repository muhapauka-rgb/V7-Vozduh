# E30 Ten User Capacity Model

mode=read_only_model
target_name=amneziawg-exec-20260528-10-8-1-14
requested_cohort_size=10
candidate_count=4
soft_limit_current=4
hard_limit_current=4
throughput_model=requires_10_stream_target_local_validation
rollback_model=requires_10_users_currently_on_rollback_target_1
audit_model=packet must include exact 10-user set and 10 rollback entries
replay_model=must deny replay after one 10-user forward record
ten_user_capacity_model_safe=false
reason=Capacity probe can test target pressure, but full ten-user model is not safe while candidate_count<10 on rollback target 1.
