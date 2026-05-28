# E9.2 Future Hold Model

Mode: planning only. Do not execute during E9.2.

## Future Canary Window Sequence

1. Capture pre-canary evidence:
   - `date -u`
   - `systemctl is-active/is-enabled v7-health.service`
   - `systemctl is-active/is-enabled v7-autoswitch-planner.timer`
   - `systemctl is-active/is-enabled v7-users-autoswitch.timer`
   - `pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync' || true`
   - registry hashes
   - candidate row
   - table `1012`
   - `ip route get 8.8.8.8 from 10.7.0.14 iif wg0`
   - `v7-reconcile-check`
   - `v7-user-route-check`
   - `v7-killswitch-check`
   - `v7-provisioning-reconcile-check`

2. Hold planner/apply authority:
   - `systemctl stop v7-autoswitch-planner.timer`
   - `systemctl stop v7-autoswitch-planner.service`
   - `systemctl stop v7-users-autoswitch.timer`
   - `systemctl stop v7-users-autoswitch.service`

3. Keep health active:
   - `v7-health.service` must remain active.

4. Confirm quiet:
   - no `v7-users-autoswitch` process;
   - no `v7-user-switch` process;
   - no `v7-routing-sync` process;
   - registry hash stable before execution.

5. Execute only if separately approved:
   - forward would be `v7-user-switch 10.7.0.14 1`;
   - rollback would be `v7-user-switch 10.7.0.14 vless`.

6. Restore after evidence:
   - `systemctl start v7-autoswitch-planner.timer`
   - `systemctl start v7-users-autoswitch.timer`

## Abort Conditions

- any checker fails before hold;
- target `1` remains unexplained `SOFT_FULL` and no explicit one-user mechanics waiver exists;
- any hidden `v7-user-switch` or `v7-routing-sync` appears;
- planner/apply hold is not clean;
- `v7-health.service` is inactive;
- target interface `v7e356a192b79` is not `UP,LOWER_UP`;
- rollback command no longer matches current baseline.

## E9.2 Verdict

This hold model is suitable for a future E9.3 bounded live request, but E9.2 does not execute it.
