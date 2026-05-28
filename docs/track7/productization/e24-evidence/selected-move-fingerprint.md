# E24 Selected-Move Fingerprint

Canonical selected move payload:

```json
[{"candidate_user":"10.7.0.11","expected_current_dev":"v7e356a192b79","expected_target_dev":"v7e06a394c478","from_egress":"1","movement_budget":1,"rollback_target":"1","runtime_action":"BOUNDED_USER_MOVEMENT","table":"1009","to_egress":"wireguard-1779454504-c43409"}]
```

Fingerprint:

```text
selected_move_hash=8e643a26d0645043a20c28a8037cef50416a48c3ae0587e8d0d2453fb822e785
runtime_snapshot_hash=6455e711989502f6d4155225b4d56a1e8018bf7b10f0ce8669b423dca2f293e8
generation_id=E24_FIRST_BOUNDED_USER_MOVE_10_7_0_11_TO_WIREGUARD_20260528
```

The hash binds:

- candidate user;
- source egress;
- target egress;
- rollback target;
- route table;
- expected source device;
- expected target device;
- movement budget;
- runtime action.
