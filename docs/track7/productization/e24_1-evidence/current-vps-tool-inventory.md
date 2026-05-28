# E24.1 Current VPS Tool Inventory

Collected: 2026-05-28T08:37:12Z on `v3119922.hosted-by-vdsina.ru`.

## Runtime Identity

- `pwd=/root`
- `hostname=v3119922.hosted-by-vdsina.ru`
- `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin`
- `python3=/usr/bin/python3`
- `python3_version=Python 3.14.4`
- `bash=/usr/bin/bash`
- `bash_version=GNU bash, version 5.3.9(1)-release`

## Existing Critical Tools Before E24.1 Deploy

Present:

- `/usr/local/bin/v7-users-autoswitch`
  - sha256=`8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c`
- `/usr/local/bin/v7-reconcile-check`
  - sha256=`f8218d42abb8b71d878790a59919d880e3da510ddc615d9f8b6a78da130c0e7b`
- `/usr/local/bin/v7-user-route-check`
  - sha256=`d88435b6b309016840b07de608253d8bd5f8eee4b7eee9f1e2b52bcb4d4893bf`
- `/usr/local/bin/v7-killswitch-check`
  - sha256=`504a7c5f8b06846643c199cf6cd2087e55357c8db4ed19519662257f397165f9`
- `/usr/local/bin/v7-provisioning-reconcile-check`
  - sha256=`cd1c007e7d6f9830c54fd4713c862fe29e084dc4cd7106e1017dc987c7f547cf`

Missing before E24.1 deploy:

- `v7-second-canary-target-readiness`
- `v7-restore-settle-gate`
- `v7-operator-execution-packet`

Only the two E24.1 movement-critical helpers were in scope for deploy:

- `v7-second-canary-target-readiness`
- `v7-restore-settle-gate`

## Runtime State

- `/opt/v7/egress/state/users.registry`
  - mode/owner: `-rw-r--r-- root root`
  - sha256=`bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `/opt/v7/egress/state/egress.registry`
  - mode/owner: `-rw-r--r-- root root`
  - sha256=`a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Selected-move files:

- No `/opt/v7/egress/state/*selected*` files present.
- Runtime interpretation for E24.1: `selected_moves=0`.

Autoswitch state files:

- `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- `/opt/v7/egress/state/autoswitch-safety.json`

Planner/apply timers:

- `v7-users-autoswitch-planner.timer=inactive`
- `v7-users-autoswitch-apply.timer=inactive`

Hidden mover scan:

- No `v7-user-switch`
- No `v7-routing-sync`
- No `v7-users-autoswitch --apply`

## Inventory Verdict

- Runtime registries are present.
- Missing movement-critical helpers were confirmed absent before E24.1.
- No hidden mover was active.
- No selected-move state was present.
