# V7 Admin Phase 49: Policy Rebuild Guard

Date: 2026-05-07

## Goal

Prevent short false alarms in the admin panel while policy domain changes rebuild DNS/IP sets, nft rules, service matrix state, and JSON state.

This matters because adding domains to permission groups can briefly make diagnostics observe an intermediate network state. That is not a real leak or routing failure; it is a controlled rebuild window.

## Implemented

- Added policy rebuild state:
  - `/opt/v7/egress/state/policy-rebuild.state`
- Added rebuild lock helpers in:
  - `/usr/local/lib/v7-policy-domain-lib`
- Added CLI status command:
  - `/usr/local/bin/v7-policy-rebuild-status`
- Wrapped domain add/remove apply flow with:
  - `REBUILDING` begin marker
  - policy resolve
  - policy apply
  - policy matrix state update
  - JSON state save
  - 10 second settle window
  - rebuild end marker
- Updated `v7-killswitch-check`:
  - returns `V7_KILLSWITCH_CHECK=REBUILDING` during active rebuild
  - exits `0` during active rebuild
  - returns normal `OK/FAIL` outside rebuild
  - verifies direct mark rule priority before user routing rules
- Updated JSON state:
  - `policy_rebuild.active`
  - `policy_rebuild.operation`
  - `policy_rebuild.updated`
  - `policy_rebuild.actor`
  - `policy_rebuild.expires_epoch`
- Updated admin dashboard:
  - top metric `Policy rebuild`
  - policy preview shows rebuild status and operation
  - Kill switch card treats `REBUILDING` as a controlled transitional state, not as a failure

## VPS Validation

Commands were installed on the VPS and tested live.

Admin service:

```text
systemctl is-active v7-admin-api
active

curl /login
LOGIN_HTTP=200
```

Manual rebuild guard:

```text
v7_policy_rebuild_begin manual_test
v7-policy-rebuild-status
V7_POLICY_REBUILD=REBUILDING

v7-killswitch-check
V7_KILLSWITCH_CHECK=REBUILDING

v7_policy_rebuild_end manual_test
v7-policy-rebuild-status
V7_POLICY_REBUILD=IDLE
```

Final network checks after rebuild:

```text
v7-killswitch-check
V7_KILLSWITCH_CHECK=OK

v7-system-check
V7_RESULT=OK
```

## Result

Admin domain edits are now safer operationally:

- transient policy rebuilds are visible;
- false red kill-switch alarms are avoided during the controlled rebuild window;
- real kill-switch failures are still reported after the rebuild ends;
- the current V7 routing model remains unchanged.

