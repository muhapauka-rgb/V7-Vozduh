# E28.1 Four User Rollback Model

rollback_manifest:
- 10.7.0.11 -> 1 / table 1009
- 10.7.0.12 -> 1 / table 1010
- 10.7.0.14 -> 1 / table 1012
- 10.7.0.15 -> 1 / table 1013

rollback_order=sequential_exact_user_order
rollback_target=1
four_user_rollback_safe=true
