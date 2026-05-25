# V7 Phase 1 - Reconciliation Plan

## Purpose

V7 routing must be reconciliation-first. The platform should continuously compare desired state, runtime state, observed diagnostics, and effective datapath without rewriting routing behavior during Phase 1.

This plan defines mismatch categories and repair policy.

## Reconciliation Loop

Safe reconciliation order:

1. Load desired state with corruption-safe parsing.
2. Inspect runtime state read-only.
3. Inspect observed state with timestamps.
4. Derive expected runtime from desired state.
5. Compare actual runtime to expected runtime.
6. Classify mismatches by safety impact.
7. Report summary first, details on drill-down.
8. Repair only when action is bounded, reversible, audited, and followed by verification.

## Mismatch Categories

### Registry and Assignment

- `USERS_REGISTRY_MISSING`: users registry is absent.
- `USERS_REGISTRY_CORRUPT`: users registry cannot be parsed safely.
- `USER_DUPLICATE_IP`: multiple users claim one client IP.
- `USER_ENABLED_WITHOUT_EGRESS`: enabled user has no assigned egress.
- `USER_ASSIGNED_UNKNOWN_EGRESS`: user references an egress missing from egress registry.
- `USER_ROUTE_TABLE_INVALID`: user table id is missing or not numeric when required.
- `EGRESS_REGISTRY_MISSING`: egress registry is absent.
- `EGRESS_REGISTRY_CORRUPT`: egress registry cannot be parsed safely.
- `EGRESS_DUPLICATE_ID`: duplicate egress id exists.
- `EGRESS_ENABLED_WITHOUT_INTERFACE`: enabled interface-backed egress has no interface.

### Interface and Process Runtime

- `EGRESS_INTERFACE_MISSING`: desired enabled egress interface does not exist.
- `INTERFACE_DEAD_REGISTRY_ENABLED`: registry marks egress enabled but interface is down or absent.
- `INTERFACE_LIVE_REGISTRY_DISABLED`: interface is live but registry says disabled/drained/quarantined.
- `TRANSPORT_PROCESS_MISSING`: required transport process or unit is absent for enabled egress.
- `DEAD_INTERFACE_WITH_ALIVE_REGISTRY`: interface cannot carry traffic while registry says usable.

### Policy Routing

- `IP_RULE_MISSING`: expected per-user or mark rule is absent.
- `IP_RULE_WRONG_PRIORITY`: required rule exists at wrong priority or with ambiguous order.
- `ROUTE_TABLE_MISSING`: expected route table is absent.
- `ROUTE_TABLE_WRONG_DEFAULT`: expected table default does not point to assigned egress.
- `WRONG_EGRESS_ASSIGNMENT_RUNTIME`: runtime table routes user to a different egress than registry.

### Kill Switch and Leak Safety

- `NFT_TABLE_MISSING`: `inet v7` table is absent.
- `NFT_CLIENT_SRC_MISSING`: VPN client source subnet protection is absent.
- `NFT_FORWARD_POLICY_UNSAFE`: forward chain policy or rules allow unbounded leak path.
- `VPN_SUBNET_PUBLIC_LEAK_RISK`: `10.0.0.0/24` or `10.7.0.0/22` can route to public interface without explicit policy.
- `NAT_MISSING`: expected NAT for egress path is absent.
- `MSS_CLAMP_MISSING`: expected MSS clamp is absent where runtime requires it.

### Direct/RU Exception

- `DIRECT_FWMARK_RULE_MISSING`: fwmark rule for direct path is absent.
- `DIRECT_TABLE_MISSING`: direct table `70` is absent.
- `DIRECT_TABLE_WRONG_DEFAULT`: direct table does not point to expected public interface.
- `NFT_DIRECT_SET_MISSING`: direct allow set is missing.
- `DNS_CAPTURE_MISSING`: direct/RU DNS capture is missing.
- `TRUSTED_RU_UNSAFE_FALLBACK`: trusted RU path would silently fallback to unsafe routing.

### Observability and Safety Files

- `SERVICE_MATRIX_STALE`: service matrix timestamp is stale.
- `SERVICE_MATRIX_CORRUPT`: service matrix cannot be parsed.
- `QUALITY_SUMMARY_CORRUPT`: quality summary cannot be parsed.
- `AUTOSWITCH_SAFETY_CORRUPT`: autoswitch safety file cannot be parsed.
- `POLICY_CORRUPT`: policy file cannot be parsed.
- `OBSERVED_RUNTIME_MISMATCH`: observed status claims healthy while runtime/effective state is degraded.

## Severity Model

- `blocker`: possible traffic leak, kill switch bypass, unsafe direct fallback, corrupted critical policy.
- `critical`: user path broken or runtime contradicts desired routing assignment.
- `warning`: degraded/partial mismatch with bounded impact.
- `info`: stale optional diagnostic or non-critical missing optional component.

Blockers must be surfaced before metrics.

## Repair Strategy

### Tier 0 - Read-Only Detection

Allowed:

- parse files;
- inspect `ip`, `nft`, `wg`, `systemctl` state;
- compare registries to runtime;
- emit diagnostics.

No runtime mutation.

### Tier 1 - Dry-Run Repair Plan

Allowed:

- explain exact command or existing tool action that would repair mismatch;
- show before/after intent;
- show rollback context;
- require explicit operator action for dangerous operations.

No runtime mutation.

### Tier 2 - Bounded Repair

Allowed only through existing safe operational tools:

- rebuild kill switch from current desired state;
- restore missing route rule/table;
- restart a degraded interface;
- put unstable egress into quarantine;
- reconcile registry/runtime when source of truth is unambiguous.

Required:

- actor;
- reason;
- before/after snapshot;
- audit event;
- post-repair verification.

### Tier 3 - Manual Intervention

Required when:

- source of truth is ambiguous;
- trusted RU would need unsafe fallback;
- policy files are corrupt;
- identity DB and registries conflict;
- repair would migrate many users;
- kill switch safety cannot be verified.

## Operator Output Shape

Summary-first:

- overall routing health;
- number of blockers;
- impacted users/egresses;
- recommended bounded action.

Details only on drill-down:

- raw command output;
- per-rule mismatch;
- registry row diagnostics;
- exact runtime table data.

## Phase 1 Boundary

This plan defines reconciliation logic and repair guardrails. It does not enable automatic runtime repair by itself.
