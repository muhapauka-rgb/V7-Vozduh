# V7 Phase 2 - Import Pipeline

## Purpose

The import pipeline must safely transform unknown input into a disabled, verified, operator-visible egress candidate.

It must never silently enable production routing.

## Supported Inputs

- config file;
- subscription URL;
- subscription text/list;
- URI;
- QR payload;
- sing-box/Xray outbound fragment;
- Clash YAML;
- provider bundle.

## Pipeline Stages

### 1. import

Receive raw source and store it as root-only draft input.

No runtime impact.

### 2. normalize

Normalize the input into V7-managed runtime semantics.

Examples:

- WireGuard/AmneziaWG: force `Table = off`;
- OpenVPN: force route-nopull and V7-managed interface;
- proxy sources: produce one managed sing-box outbound.

### 3. validate

Run static checks:

- required fields;
- unsafe hook detection;
- dependency availability;
- supported adapter;
- route ownership compatibility.

### 4. fingerprint

Compute stable fingerprint from endpoint and driver-specific identity:

- endpoint host/port;
- peer/public key or UUID where applicable;
- outbound type;
- selected provider endpoint.

### 5. duplicate detection

Compare fingerprint against active registry and runtime profiles.

Default action:

- block duplicate and ask operator.

Allowed actions:

- update existing when exact target is confirmed;
- create duplicate only with explicit operator override.

### 6. draft create

Create draft metadata and raw input under draft storage.

No production impact.

### 7. quarantine

Run isolated runtime and service checks.

No users. No route-class eligibility. No autoswitch participation.

### 8. runtime test

Verify temporary runtime can start, reach external IP, and clean up.

Failure leaves draft blocked.

### 9. staging

Add to egress pool only as disabled:

- `enabled=0`;
- users not moved;
- routes not changed;
- services not restarted unless explicitly part of isolated test cleanup.

### 10. enable proposal

Show readiness and blockers before explicit enable.

Enable must still be guarded and must not migrate users by itself.

## Current Implementation Alignment

Current admin API already exposes:

- `egress_config_preview`;
- `egress_draft_create`;
- `egress_draft_preflight_run`;
- `egress_draft_runtime_run`;
- quarantine mode;
- `egress_draft_pool_preview`;
- `egress_draft_pool_apply`;
- `egress_draft_runtime_provision`;
- `egress_draft_enable_preview`;
- `egress_draft_enable_apply`;
- post-enable validation.

## Pipeline Output

Operator summary should show:

- stage;
- status;
- blocker;
- safe next action;
- whether production was affected.

Raw config, secrets, and full command output stay hidden unless drill-down is needed.
