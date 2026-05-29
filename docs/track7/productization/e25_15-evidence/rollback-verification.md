# E25.15 Rollback Verification

date_utc=2026-05-28T20:57:53Z
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
drift_row=ip=10.7.0.16 current=vless table=1014 enabled=1
target_users=0
route_table_1009=default dev v7e356a192b79 scope link  
route_get_10_7_0_11=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
route_get_10_7_0_16=8.8.8.8 from 10.7.0.16 dev tun0 table 1014      cache iif wg0  
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true

rollback_success=true
out_of_scope_user_10_7_0_16_unchanged=true
target_users_restored=true
route_table_1009_restored=true
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
