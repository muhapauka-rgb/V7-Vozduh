# Block A Rollback Certification

Project: V7 Vozduh

Block: A - Single User Completion Program

## Delayed Final Observation

Final delayed observation:

- `final_current=1`
- `final_source_count=10`
- `final_target_count=0`
- `final_outside_users_hash=d4a727db73f70e6f5a2a98747ed640c9a4c3edf6c1f0a9c89363c4499487ad8e`
- `final_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `final_selected_count=0`
- `final_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `final_routes_outside_hash=eeb83c6bc224a46f8682821148b360a2e76234e7587e023a050ae82103604eef`
- `final_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`
- `final_route_table=default dev v7e356a192b79 scope link`
- `final_autoswitch_timer=inactive`
- `audit_count=13`
- `switch_history_count=2740`

## Certification

Rollback is certified because:

- The approved user returned to egress `1`.
- Execution egress user count returned to `0`.
- Egress `1` count returned to `10`.
- Route table `1009` points to `v7e356a192b79`.
- Outside users remained unchanged.
- Egress registry remained unchanged.
- IP rules remained unchanged.
- Routes outside table `1009` remained unchanged.
- Autoswitch remained inactive.

## Verdict

`rollback_certified=true`

