# E30.1 Candidate Classification

candidate_pool_possible=true
already_eligible_on_1:
- ip=10.7.0.11 current=1 table=1009 enabled=1
- ip=10.7.0.12 current=1 table=1010 enabled=1
- ip=10.7.0.14 current=1 table=1012 enabled=1
- ip=10.7.0.15 current=1 table=1013 enabled=1

eligible_for_normalization_to_1:
- ip=10.7.0.2 current=awg3 table=1000 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required
- ip=10.7.0.3 current=awg3 table=1001 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required
- ip=10.7.0.4 current=awg3 table=1002 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required
- ip=10.7.0.5 current=awg3 table=1003 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required
- ip=10.7.0.6 current=awg3 table=1004 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required
- ip=10.7.0.8 current=awg3 table=1006 enabled=1 reason=enabled_known_route_table_awg3_pool_minimum_required

not_selected_or_not_safe_for_candidate_pool:
- ip=10.7.0.7 reason=disabled
- ip=10.7.0.16 reason=vless_special_path_and_not_required
- ip=10.0.0.2,10.0.0.3,10.0.0.6 reason=older_10.0_subnet_not_required_for_10.7_candidate_pool
- ip=10.7.0.9,10.7.0.10,10.7.0.13 reason=awg0_pool_not_required_because_awg3_pool_has_minimum_six_candidates
