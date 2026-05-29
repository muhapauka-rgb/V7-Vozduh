# E30 Ten User Rollback Model

rollback_candidate_count=4
rollback_target=1
- 10.7.0.11 -> 1 / table 1009
- 10.7.0.12 -> 1 / table 1010
- 10.7.0.14 -> 1 / table 1012
- 10.7.0.15 -> 1 / table 1013

ten_user_rollback_safe=false
reason=insufficient users currently on rollback target 1 for deterministic 10-user rollback manifest
