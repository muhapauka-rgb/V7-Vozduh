# E9.2.5 OpenVPN Idle-SUSPECT Waiver Definition

```text
waiver_name=openvpn_idle_suspect_mechanics_canary
waiver_scope=one_user_only
candidate_user=10.7.0.14
target=openvpn-1779388847-d2ad7c
rollback_target=vless
accepted_risk=diagnose SUSPECT caused by idle/stale handshake, not proven live failure
approval_status=CONDITIONAL
execution_allowed_now=false
```

## Meaning

This is not a clean target canary. This is a mechanics + target-diversity canary under explicit idle-SUSPECT waiver.

The waiver accepts only this known condition:

```text
target_diagnose_status=SUSPECT
target_diagnose_detail=handshake_age_seconds=999999
target_zero_user=true
interface_state=UP,LOWER_UP
quality_floor=acceptable
```

## Not Waived

The waiver does not waive:

- `v7-killswitch-check` failure;
- `v7-reconcile-check` failure;
- `v7-provisioning-reconcile-check` failure;
- `v7-user-route-check` failure;
- hidden `v7-routing-sync`;
- hidden `v7-user-switch`;
- autoswitch planner/apply process during canary window;
- target interface missing/down;
- `users.registry` drift before canary;
- any other user movement;
- OpenVPN route table preview mismatch;
- rollback uncertainty;
- Direct/RU or Trusted RU mutation;
- policy/proxy/killswitch mutation;
- any target diagnose change from idle `SUSPECT` to `FAIL` or non-stale failure.

## Future Execution Gates

Before any live E9.3 switch:

- `v7-reconcile-check OK`;
- `v7-user-route-check OK`;
- `v7-killswitch-check OK`;
- `v7-provisioning-reconcile-check OK`;
- candidate still `current=vless table=1012 enabled=1`;
- target OpenVPN zero-user by registry/load-state;
- target interface present and `UP,LOWER_UP`;
- target route table preview still maps table `1012` to `v7edb0c189291`;
- OpenVPN diagnose may remain `SUSPECT` only if stale-idle reason is unchanged;
- autoswitch planner/apply authority held;
- no `v7-user-switch` / `v7-routing-sync` process;
- rollback command copied and ready;
- operator explicitly accepts `openvpn_idle_suspect_mechanics_canary`.
