# E9.3.8 Runtime Deploy Readiness

Status: planning only.
Runtime deploy performed: no.

## Runtime Files Affected By Future Deploy

Only this runtime executable should be updated:

```text
/usr/local/bin/v7-users-autoswitch
```

Do not modify in the same deploy:

```text
/etc/systemd/system/v7-users-autoswitch.timer
/etc/systemd/system/v7-users-autoswitch.service
/etc/systemd/system/v7-autoswitch-planner.timer
/etc/systemd/system/v7-autoswitch-planner.service
/etc/systemd/system/v7-health.service
/opt/v7/egress/state/users.registry
/opt/v7/egress/state/egress.registry
routes/ip rules/nftables
```

## Future Backup Commands

Not executed in E9.3.8.

```bash
ts="$(date -u +%Y%m%dT%H%M%SZ)"
cp -a /usr/local/bin/v7-users-autoswitch "/usr/local/bin/v7-users-autoswitch.backup.e9_3_8.${ts}"
sha256sum /usr/local/bin/v7-users-autoswitch "/usr/local/bin/v7-users-autoswitch.backup.e9_3_8.${ts}"
```

## Future Deploy Command

Not executed in E9.3.8.

```bash
install -m 0755 tools/v7-users-autoswitch /usr/local/bin/v7-users-autoswitch
```

Owner/mode should preserve executable semantics. If runtime owner differs from root, capture it before deploy and preserve it explicitly.

## Timer Requirements During Future Deploy

Required:

```text
v7-users-autoswitch.timer must remain held/inactive
v7-users-autoswitch.service must not be running
```

Recommended:

```text
v7-autoswitch-planner.timer can remain active only if deploy is atomic and no planner run is active.
If an active planner process exists, abort and wait for inactive state.
```

Safer deploy window:

```text
planner timer held
apply timer held
v7-health.service active
```

## Future Verification Commands

Read-only:

```bash
sha256sum /usr/local/bin/v7-users-autoswitch
v7-users-autoswitch --help
v7-reconcile-check
v7-user-route-check
v7-killswitch-check
v7-provisioning-reconcile-check
```

Planner dry-run after deploy should be a separate bounded step because planning may write load/reconnect summary state:

```bash
v7-users-autoswitch --pretty
```

Do not include `--apply`.

## Future Rollback Commands

Not executed in E9.3.8.

```bash
cp -a "/usr/local/bin/v7-users-autoswitch.backup.e9_3_8.${ts}" /usr/local/bin/v7-users-autoswitch
sha256sum /usr/local/bin/v7-users-autoswitch
v7-users-autoswitch --help
```

## Deploy Readiness Verdict

```text
repo_policy_fix_implemented=true
runtime_policy_deployed=false
code_fix_ready_for_runtime_deploy=true
apply_timer_should_remain_held=true
planner_dry_run_required_after_deploy=true
execution_allowed_now=false
```

