# E30.3 Rollback Verification

date_utc=2026-05-29T17:07:23Z
candidate_10.7.0.2_row=ip=10.7.0.2 current=1 table=1000 enabled=1
route_table_1000=default dev v7e356a192b79 scope link ;
route_get_10.7.0.2=1.1.1.1 from 10.7.0.2 dev v7e356a192b79 table 1000 ;    cache iif lo ;
candidate_10.7.0.3_row=ip=10.7.0.3 current=1 table=1001 enabled=1
route_table_1001=default dev v7e356a192b79 scope link ;
route_get_10.7.0.3=1.1.1.1 from 10.7.0.3 dev v7e356a192b79 table 1001 ;    cache iif lo ;
candidate_10.7.0.4_row=ip=10.7.0.4 current=1 table=1002 enabled=1
route_table_1002=default dev v7e356a192b79 scope link ;
route_get_10.7.0.4=1.1.1.1 from 10.7.0.4 dev v7e356a192b79 table 1002 ;    cache iif lo ;
candidate_10.7.0.5_row=ip=10.7.0.5 current=1 table=1003 enabled=1
route_table_1003=default dev v7e356a192b79 scope link ;
route_get_10.7.0.5=1.1.1.1 from 10.7.0.5 dev v7e356a192b79 table 1003 ;    cache iif lo ;
candidate_10.7.0.6_row=ip=10.7.0.6 current=1 table=1004 enabled=1
route_table_1004=default dev v7e356a192b79 scope link ;
route_get_10.7.0.6=1.1.1.1 from 10.7.0.6 dev v7e356a192b79 table 1004 ;    cache iif lo ;
candidate_10.7.0.8_row=ip=10.7.0.8 current=1 table=1006 enabled=1
route_table_1006=default dev v7e356a192b79 scope link ;
route_get_10.7.0.8=1.1.1.1 from 10.7.0.8 dev v7e356a192b79 table 1006 ;    cache iif lo ;
candidate_10.7.0.11_row=ip=10.7.0.11 current=1 table=1009 enabled=1
route_table_1009=default dev v7e356a192b79 scope link ;
route_get_10.7.0.11=1.1.1.1 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif lo ;
candidate_10.7.0.12_row=ip=10.7.0.12 current=1 table=1010 enabled=1
route_table_1010=default dev v7e356a192b79 scope link ;
route_get_10.7.0.12=1.1.1.1 from 10.7.0.12 dev v7e356a192b79 table 1010 ;    cache iif lo ;
candidate_10.7.0.14_row=ip=10.7.0.14 current=1 table=1012 enabled=1
route_table_1012=default dev v7e356a192b79 scope link ;
route_get_10.7.0.14=1.1.1.1 from 10.7.0.14 dev v7e356a192b79 table 1012 ;    cache iif lo ;
candidate_10.7.0.15_row=ip=10.7.0.15 current=1 table=1013 enabled=1
route_table_1013=default dev v7e356a192b79 scope link ;
route_get_10.7.0.15=1.1.1.1 from 10.7.0.15 dev v7e356a192b79 table 1013 ;    cache iif lo ;
all_10_users_back_on_1=true
route_get_for_all_10_restored=true
no_other_users_changed=true
target_users_count=0
selected_moves_count=0
hidden_movers_absent=true
runtime_checkers_ok=true
rollback_success=true
