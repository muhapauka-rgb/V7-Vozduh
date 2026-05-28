# E11.2 Stale Handshake Semantics Decision

Target:

```text
egress_id=wireguard-1779454504-c43409
interface=v7e06a394c478
```

Fresh read-only evidence from `current-wireguard-truth.txt`:

```text
diagnose_reason=curl_ok_but_handshake_stale
diagnose_severity=SUSPECT
diagnose_detail=handshake_age_seconds=999999
interface_state=UP,LOWER_UP
live_latest_handshake=1 minute, 47 seconds ago
transfer=6.87 GiB received, 277.58 MiB sent
route_get=8.8.8.8 dev v7e06a394c478 src 10.8.0.17
wireguard_registry_users=0
load_status=OK
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
planner_blocker=severity_SUSPECT
selected_moves=[]
apply_result.applied=false
runtime_checks=OK
```

## Classification

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
secondary_classification=STALE_HANDSHAKE_ONLY
real_datapath_failure_detected=false
route_issue_detected=false
quality_degraded=false
confidence=high
```

The persisted diagnose state says `handshake_age_seconds=999999`, but live
`wg show` contradicts that persisted value with a fresh handshake and growing
transfer counters. The route and NAT/MSS/allow evidence are present. The
planner excludes WireGuard only because diagnose severity remains `SUSPECT`.

## Semantics Decision

Stale persisted handshake alone should not permanently block a zero-user
reserved test target when all live datapath evidence is fresh and healthy.
For production autoswitch assignment, `SUSPECT` may remain conservative. For a
bounded canary target, the blocker can be accepted only under explicit waiver
or fixed by diagnose semantics that reconcile persisted state with live
WireGuard handshake evidence.

```text
should_stale_handshake_alone_block_clean_target=true_under_current_strict_rules
should_zero_user_reserved_targets_use_different_semantics=true
quality_route_runtime_evidence_sufficient_to_override_stale_diagnose=conditional_with_waiver
```
