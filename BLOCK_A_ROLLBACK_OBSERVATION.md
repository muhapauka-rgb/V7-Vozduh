# Block A Rollback Observation

Project: V7 Vozduh

Block: A - Single User Completion Program

Observation source:

- `/tmp/block-a-single-user-completion-20260601T104148Z/after_observation.env`

## Immediate Post-Rollback Observation

- `after_current=1`
- `after_source_count=10`
- `after_target_count=0`
- `after_users_hash=f00a0956230b4f9e7484b5487f1ec5307edda2e1badca99afee6e3c1940fcbf5`
- `after_outside_users_hash=d4a727db73f70e6f5a2a98747ed640c9a4c3edf6c1f0a9c89363c4499487ad8e`
- `after_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `after_selected_count=0`
- `after_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `after_routes_outside_hash=eeb83c6bc224a46f8682821148b360a2e76234e7587e023a050ae82103604eef`
- `after_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`
- `exec_rc=0`

Route table `1009` after rollback:

```text
default dev v7e356a192b79 scope link
```

## Checker Commands

The existing checker commands were run directly:

- `v7-user-route-check`: `V7_USER_ROUTE_CHECK=OK`
- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-provisioning-reconcile-check`: `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Observation Verdict

`rollback_observed=true`

