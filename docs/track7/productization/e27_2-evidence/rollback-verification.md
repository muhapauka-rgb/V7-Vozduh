# E27.2 Rollback Verification

date_utc=2026-05-28T22:49:39Z
candidate_user_A_current=1
candidate_user_B_current=1
target_users=0
route_table_1009=default dev v7e356a192b79 scope link ;
route_table_1010=default dev v7e356a192b79 scope link ;
route_get_A=1.1.1.1 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif lo ;
route_get_B=1.1.1.1 from 10.7.0.12 dev v7e356a192b79 table 1010 ;    cache iif lo ;
selected_moves_count=0
hidden_movers_present=false
runtime_checkers_ok=true
rollback_success=true
