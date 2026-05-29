# E27.2 Forward Verification

date_utc=2026-05-28T22:34:40Z
candidate_user_A_current=amneziawg-exec-20260528-10-8-1-14
candidate_user_B_current=amneziawg-exec-20260528-10-8-1-14
target_users=2
route_table_1009=default dev v7execwg0 scope link ;
route_table_1010=default dev v7execwg0 scope link ;
route_get_A=1.1.1.1 from 10.7.0.11 dev v7execwg0 table 1009 ;    cache iif lo ;
route_get_B=1.1.1.1 from 10.7.0.12 dev v7execwg0 table 1010 ;    cache iif lo ;
selected_moves_count=0
hidden_movers_present=false
runtime_checkers_ok=true
forward_success=true
