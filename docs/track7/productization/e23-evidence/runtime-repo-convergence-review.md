# E23 Runtime / Repo Convergence Review

Collected: 2026-05-28T07:56:58Z on `v3119922.hosted-by-vdsina.ru`.

## VPS Runtime Tool Inventory

```text
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

v7-users-autoswitch=/usr/local/bin/v7-users-autoswitch
v7-second-canary-target-readiness=missing
v7-restore-settle-gate=missing
v7-reconcile-check=/usr/local/bin/v7-reconcile-check
v7-user-route-check=/usr/local/bin/v7-user-route-check
v7-killswitch-check=/usr/local/bin/v7-killswitch-check
v7-provisioning-reconcile-check=/usr/local/bin/v7-provisioning-reconcile-check
v7-operator-execution-packet=missing
```

## Runtime Hashes

```text
8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c  /usr/local/bin/v7-users-autoswitch
f8218d42abb8b71d878790a59919d880e3da510ddc615d9f8b6a78da130c0e7b  /usr/local/bin/v7-reconcile-check
d88435b6b309016840b07de608253d8bd5f8eee4b7eee9f1e2b52bcb4d4893bf  /usr/local/bin/v7-user-route-check
504a7c5f8b06846643c199cf6cd2087e55357c8db4ed19519662257f397165f9  /usr/local/bin/v7-killswitch-check
cd1c007e7d6f9830c54fd4713c862fe29e084dc4cd7106e1017dc987c7f547cf  /usr/local/bin/v7-provisioning-reconcile-check
f5f37e9595f87233939ed067ef25e58c500adae687de4090a8c1832140571079  /opt/v7/egress/state/autoswitch-restore-barrier.json
e13fcf81c723247ac0781c95206fc8fdc55bc5791ca696b39fb5aa5768d50083  /opt/v7/egress/state/autoswitch-safety.json
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
```

## Repo Tool Hashes

```text
8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c  tools/v7-users-autoswitch
75607c4e56740788cb8b1e160efa539059bcf4ca29f0d8978b8b6ae2b43aff8a  tools/v7-second-canary-target-readiness
eb74101dd44b0bfe8df106719602a8318ba7593149f6535f0ec0dcb9fc6dfbdc  tools/v7-restore-settle-gate
f8218d42abb8b71d878790a59919d880e3da510ddc615d9f8b6a78da130c0e7b  tools/runtime-support/v7-reconcile-check
f77b7bb318bf9e730c67c4a61e32bfda04f46630e5719553acba94441acb0ccd  admin_core/operator_execution.py before E23 edits
```

`v7-users-autoswitch` and `v7-reconcile-check` match the repo hashes. VPS lacks the repo-only target readiness and restore-settle helpers.

## Runtime State

```text
selected_move_files=missing
selected_moves=0 by zero-budget packet semantics
planner_timer=inactive
apply_timer=inactive
legacy_autoswitch_timer=inactive
hidden_movers=absent
audit_dir=/opt/v7/audit exists
governance_dir=/opt/v7/governance missing
```

Restore barrier:

```json
{
  "block": "E11.17",
  "enabled": true,
  "expires_at": "2000-01-01T00:00:00+00:00",
  "allow_post_ttl_apply": true,
  "generation_clearance": true,
  "clearance_max_selected_moves": 0
}
```

## Checkers

```text
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

## Convergence Verdict

runtime_repo_convergence_verified=true for the selected E23 action scope only.

Missing VPS helpers matter for actions that depend on target readiness or restore-settle semantics. They do not block the selected action because it does not:

- move users;
- mutate routes;
- restore planner/apply;
- run autoswitch apply;
- depend on target readiness;
- depend on restore-settle GO.

Bounded sync is not required before this specific E23 zero-move governance action. It is required before any future runtime action that claims target-readiness or restore-settle gates as live VPS checks.
