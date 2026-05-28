# E11.4 Diagnose Source Analysis

## Scope

Target:

```text
egress_id=wireguard-1779454504-c43409
interface=v7e06a394c478
mode=read-only source/runtime ownership analysis
```

## Runtime Ownership

E11.4 runtime evidence captured the production diagnose script metadata:

```text
runtime_path=/usr/local/bin/v7-egress-diagnose
owner_mode=root:root 755
runtime_sha256=35a8ef38c97be8f9aeb17b63e8f8c5ec429a8108783a796906fc65c7af7ed011
state_dir=/opt/v7/egress/state
input_registry=/opt/v7/egress/state/egress.registry
input_summary=/opt/v7/egress/state/summary.state
output=/opt/v7/egress/state/egress-diagnose.state
```

The local repository does not currently contain a first-class `tools/v7-egress-diagnose` source counterpart. The authoritative diagnose producer for this behavior is therefore runtime-owned until a dedicated source/lineage fix is prepared.

## Stale Handshake Logic

The runtime `handshake_age_seconds()` implementation reads the latest handshake with:

```text
awg show "$iface"
```

This call is unconditional. It does not branch by egress protocol and does not use `wg show` for the reserved WireGuard interface.

For an ordinary WireGuard interface, the expected live inspection command is `wg show <iface>`. If `awg show <iface>` returns no matching `latest handshake`, the function returns:

```text
handshake_age_seconds=999999
```

That value can produce:

```text
diagnose=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
```

even when live WireGuard evidence is fresh.

## Downstream Consumers

`tools/v7-second-canary-target-readiness` reads `egress-diagnose.state` and rejects every non-`OK` severity:

```text
if severity != "OK":
    reasons.append(f"diagnose {severity}")
```

`tools/v7-users-autoswitch` also treats non-`OK`/`WARN` diagnose severity as an eligibility blocker:

```text
severity_SUSPECT
```

E11.4 runtime planner evidence shows WireGuard rejected with:

```text
egress=wireguard-1779454504-c43409
eligible=false
blocked=["severity_SUSPECT"]
users=0
load.status=OK
avg_mbps=50.94
min_mbps=46.11
stability=0.905
```

## Ownership Conclusion

The root behavior is not in the target readiness checker alone. The strict checker is correctly consuming the persisted diagnose state. The production diagnose producer appears to compute WireGuard handshake freshness through an AWG-specific command path, which can make persisted diagnose stale relative to live WireGuard state.

Required future fix ownership:

```text
primary_runtime_file=/usr/local/bin/v7-egress-diagnose
future_repo_source_needed=true
lineage_update_needed=true
runtime_deploy_required=true
```

