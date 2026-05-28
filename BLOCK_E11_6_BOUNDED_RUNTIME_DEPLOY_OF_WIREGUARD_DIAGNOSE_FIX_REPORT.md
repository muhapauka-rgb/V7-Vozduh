# Block E11.6 - Bounded Runtime Deploy Of WireGuard Diagnose Fix Report

Mode: bounded live tooling deploy.

Mutation boundary:

```text
allowed_runtime_mutation=/usr/local/bin/v7-egress-diagnose only
canary_execution=false
user_movement=false
routing_mutation=false
autoswitch_apply_manual=false
systemd_restart=false
```

## Summary

E11.6 deployed the protocol-aware `v7-egress-diagnose` fix to runtime.

The old runtime tool always used `awg show "$iface"` for handshake freshness.
That produced a false stale-handshake result for the reserved regular
WireGuard target:

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
pre_deploy_diagnose=SUSPECT
pre_deploy_reason=curl_ok_but_handshake_stale
pre_deploy_detail=handshake_age_seconds=999999
```

After deploy, the runtime tool uses:

```text
WireGuard -> wg show "$iface"
AWG/AmneziaWG -> awg show "$iface"
```

Post-deploy evidence shows:

```text
wireguard_diagnose_after=OK
wireguard_blocker_after=NONE
wireguard_users_after=0
wireguard_reserved_after=true
wireguard_quality_ok=true
wireguard_route_get_ok=true
wireguard_interface_up_lower_up=true
```

## Runtime Deploy

Runtime ownership was clear:

```text
runtime_path=/usr/local/bin/v7-egress-diagnose
owner=root
group=root
mode=755
pre_deploy_hash=35a8ef38c97be8f9aeb17b63e8f8c5ec429a8108783a796906fc65c7af7ed011
post_deploy_hash=8617466dcf21ccdc3ded3f1ee0cfee7ae7e3ecc9d80d7e85c8d084df4267784e
```

Backup:

```text
backup_path=/opt/v7/backups/e11_6-diagnose/v7-egress-diagnose.20260526T205537Z.bak
backup_hash=35a8ef38c97be8f9aeb17b63e8f8c5ec429a8108783a796906fc65c7af7ed011
rollback_command=cp -p /opt/v7/backups/e11_6-diagnose/v7-egress-diagnose.20260526T205537Z.bak /usr/local/bin/v7-egress-diagnose
rollback_performed=false
```

## Post-Deploy Verification

WireGuard:

```text
wireguard-1779454504-c43409_diagnose_reason=OK
wireguard-1779454504-c43409_diagnose_severity=OK
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=60
```

AWG/AmneziaWG regression check:

```text
awg0_diagnose_reason=OK
awg3_diagnose_reason=OK
target_1_protocol=amneziawg
target_1_diagnose_reason=OK
target_1_diagnose_detail=handshake_age_seconds=8
awg_regression_observed=false
```

The focused target `1` check confirmed that `wg show v7e356a192b79` is
unsupported as expected, while `awg show v7e356a192b79` returns fresh handshake
data. A transient immediate post-refresh `SUSPECT` line for target `1` did not
persist and was not reproduced in the focused regression check.

Runtime checks:

```text
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
runtime_checks_ok=true
```

## Target Readiness

The strict runtime-state fixture with the old stale candidate expectation still
reports `NO-GO` because `10.7.0.14` is no longer on `vless`.

Current runtime truth for the same candidate is:

```text
candidate_user=10.7.0.14
current_egress=1
candidate_still_valid=true
selected_target_after=wireguard-1779454504-c43409
target_readiness_after=GO
second_canary_readiness_after=GO
waiver_required_after=false
```

This means the diagnose deploy cleared the WireGuard target blocker. The next
canary packet still must be fresh because old rollback/current-egress
assumptions are stale.

## Decision

```text
diagnose_fix_deployed=true
rollback_performed=false
backup_path=/opt/v7/backups/e11_6-diagnose/v7-egress-diagnose.20260526T205537Z.bak
wireguard_diagnose_after=OK
wireguard_blocker_after=NONE
awg_regression_observed=false
target_readiness_after=GO
selected_target_after=wireguard-1779454504-c43409
waiver_required_after=false
second_canary_readiness_after=GO
restore_settle_gate_status=GO_PREEXISTING_E9_4_6_NOT_RETESTED_BY_DEPLOY
runtime_checks_ok=true
recommended_next_block=E11.7_FRESH_SECOND_CANARY_APPROVAL_PACKET_AFTER_WIREGUARD_DIAGNOSE_FIX
execution_allowed_now=false
```

## Final Mutation Statement

```text
Runtime mutation performed: YES - limited to v7-egress-diagnose tooling only
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
