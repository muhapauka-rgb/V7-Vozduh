# E24 Runtime / Repo Convergence Check

## VPS Tool Availability

```text
v7-users-autoswitch=/usr/local/bin/v7-users-autoswitch
v7-second-canary-target-readiness=missing
v7-restore-settle-gate=missing
v7-reconcile-check=/usr/local/bin/v7-reconcile-check
v7-user-route-check=/usr/local/bin/v7-user-route-check
v7-killswitch-check=/usr/local/bin/v7-killswitch-check
v7-provisioning-reconcile-check=/usr/local/bin/v7-provisioning-reconcile-check
v7-operator-execution-packet=missing
```

## VPS Tool Hashes

```text
v7-users-autoswitch=8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c
v7-reconcile-check=f8218d42abb8b71d878790a59919d880e3da510ddc615d9f8b6a78da130c0e7b
v7-user-route-check=d88435b6b309016840b07de608253d8bd5f8eee4b7eee9f1e2b52bcb4d4893bf
v7-killswitch-check=504a7c5f8b06846643c199cf6cd2087e55357c8db4ed19519662257f397165f9
v7-provisioning-reconcile-check=cd1c007e7d6f9830c54fd4713c862fe29e084dc4cd7106e1017dc987c7f547cf
```

Repo has `tools/v7-second-canary-target-readiness` and `tools/v7-restore-settle-gate`, but they are not installed on the VPS.

## Impact

Missing target-readiness and restore-settle helpers are not acceptable for direct execution of a movement-bearing action. They prevent a fully trusted live E25 runtime gate.

The current runtime truth is sufficient for a conditional approval packet because:

- registries are present and hashable;
- route and kill-switch checkers pass;
- candidate route table is sane;
- target interface is up and has zero users;
- selected moves are zero;
- hidden movers are absent.

But it is not sufficient for execution because the next block must independently prove:

- `v7-second-canary-target-readiness --json` or equivalent installed and passing on VPS;
- `v7-restore-settle-gate --pre-restore --json` or equivalent installed and passing on VPS;
- CLI packet consumer installed or a governed no-deploy execution method explicitly approved.

## Required Answers

```text
runtime_repo_convergence_sufficient_for_approval_packet=true
runtime_repo_convergence_sufficient_for_execution_next=false
bounded_sync_required_before_execution=true
```
