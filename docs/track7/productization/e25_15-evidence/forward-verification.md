# E25.15 Forward Verification

date_utc=2026-05-28T20:54:46Z
candidate_row=ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
drift_row=ip=10.7.0.16 current=vless table=1014 enabled=1
target_users=1
route_table_1009=default dev v7execwg0 scope link  
route_get_10_7_0_11=8.8.8.8 from 10.7.0.11 dev v7execwg0 table 1009      cache iif wg0  
route_get_10_7_0_16=8.8.8.8 from 10.7.0.16 dev tun0 table 1014      cache iif wg0  
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true

## Verdict
forward_success=true
out_of_scope_user_10_7_0_16_unchanged=true
target_users_increased_by_one=true
route_table_1009_uses_execution_target=true
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
