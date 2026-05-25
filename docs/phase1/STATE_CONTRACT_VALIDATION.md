# V7 Phase 1 - State Contract Validation

## Purpose

Runtime contracts must be parsed safely before any routing, reconcile, autoswitch, or repair action trusts them.

Phase 1 adds a read-only validator and formalizes minimum contract checks. It does not migrate or rewrite existing state files.

## Registry Format

Current runtime registries use whitespace-separated `key=value` rows.

Example:

```text
id=egress1 type=interface protocol=wireguard interface=wg1 enabled=1
id=user1 ip=10.7.0.2 current=egress1 table=1001 enabled=1
```

Rules:

- blank lines are ignored;
- lines starting with `#` are ignored;
- unknown keys are preserved by runtime tools and should not fail validation by default;
- validation should report missing or unsafe critical keys.

## users.registry Minimum Contract

Required for active routing:

- `ip`: user VPN client address;
- `current`: assigned egress id;
- `table`: route table id when per-user routing is used;
- `enabled` or equivalent status when present.

Validation:

- IP must parse;
- IP should belong to `10.0.0.0/24` or `10.7.0.0/22`;
- duplicate IP is critical;
- enabled user without egress is critical;
- assigned egress missing from egress registry is critical;
- route table must be numeric when present.

## egress.registry Minimum Contract

Required for production egress:

- `id`: stable egress identifier;
- `type`: runtime mode such as interface/direct/proxy;
- `protocol`: transport/driver family;
- `interface`: runtime interface for interface-backed egress;
- `enabled`: production eligibility flag when present.

Validation:

- duplicate id is critical;
- invalid id characters are critical;
- enabled interface-backed egress without interface is critical;
- unknown protocol is warning unless the platform explicitly depends on it;
- disabled/quarantine/maintenance semantics must be preserved by future tools.

## JSON State Contracts

Files:

- `service-matrix.json`
- `egress-quality-summary.json`
- `autoswitch-safety.json`
- `v7-state.json`
- `direct-ru-diagnostics.json`

Validation:

- invalid JSON is critical;
- top-level non-object is warning unless the consuming runtime requires stricter schema;
- stale timestamps should be surfaced by observability, not silently treated as healthy.

## Policy Contracts

Files:

- `/opt/v7/policy.json`
- `/opt/v7/org-egress-policy.json`
- route-class policy/registry files.

Validation:

- invalid JSON is critical;
- top-level policy JSON should be an object;
- unknown policy keys should not fail validation unless they create unsafe routing ambiguity;
- route classes must map to documented semantics before they are used for safety decisions.

## Identity DB Contract

Identity DB is lifecycle authority for users/orgs/devices. It is not direct proof of Linux datapath state.

Validation:

- DB presence should be visible;
- missing DB in a local/sandbox environment is warning;
- missing DB in production may become critical depending on active identity features.

## Read-Only Validator

Tool:

- `tools/v7-runtime-contract-validate`

Properties:

- read-only;
- no networking mutation;
- no registry writes;
- no route/nft/systemd changes;
- JSON output for operator tooling;
- exit `1` on critical findings.

## Phase 1 Boundary

This document and validator detect contract problems. They do not change existing registry format or runtime assumptions.
