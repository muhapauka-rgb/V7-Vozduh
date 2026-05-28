# E24 Runtime Recheck Gates For E25

E25 must recheck all gates immediately before any movement.

## Approval Gates

- approval not expired;
- no replay by `approval_id`;
- two operator confirmations present;
- approval author and reviewer are distinct;
- UI execution remains disabled;
- CLI packet only.

## Runtime Hash Gates

- fresh `users.registry` hash captured;
- fresh `egress.registry` hash captured;
- packet hashes match or packet is regenerated from fresh state;
- selected-move hash equals `8e643a26d0645043a20c28a8037cef50416a48c3ae0587e8d0d2453fb822e785`;
- generation token equals `E24_FIRST_BOUNDED_USER_MOVE_10_7_0_11_TO_WIREGUARD_20260528`.

## Candidate Gates

- `10.7.0.11` still enabled;
- `10.7.0.11` still on current egress `1`;
- table is still `1009`;
- current route table uses `v7e356a192b79`;
- current route_get uses `v7e356a192b79`.

## Target Gates

- `wireguard-1779454504-c43409` still exists in `egress.registry`;
- target interface `v7e06a394c478` is UP/LOWER_UP;
- target users count is still 0 before movement;
- target hard_limit is still 2;
- target is still canary_reserved and explicitly approved for this packet;
- `v7-second-canary-target-readiness --json` or an explicitly approved equivalent is present and GO.

## Rollback Gates

- rollback target `1` still exists;
- rollback target interface `v7e356a192b79` is UP/LOWER_UP;
- route table can be restored to `default dev v7e356a192b79`;
- rollback command remains `v7-user-switch 10.7.0.11 1`.

## Runtime Safety Gates

- selected_moves remains zero before movement;
- no hidden `v7-user-switch`;
- no hidden `v7-routing-sync`;
- no hidden `v7-users-autoswitch --apply`;
- `v7-reconcile-check` OK;
- `v7-user-route-check` OK;
- `v7-killswitch-check` OK;
- `v7-provisioning-reconcile-check` OK;
- `v7-restore-settle-gate --pre-restore --json` or approved equivalent present and GO;
- planner/apply timers held before movement.

Any failed gate denies execution and appends a denial audit record.

runtime_recheck_gates_complete=true
