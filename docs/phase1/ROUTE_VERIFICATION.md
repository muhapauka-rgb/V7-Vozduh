# V7 Phase 1 - Unified Route Verification

## Purpose

Route verification must prove that datapath matches policy. A live tunnel is not enough.

The verification target is:

`user -> route class -> assigned egress -> Linux runtime -> effective packet path`

## Verification Dimensions

### User Assignment

Verify:

- user exists in `users.registry`;
- user client IP is unique;
- user is assigned to a known egress;
- user table id is valid;
- disabled users are not treated as active routing targets.

### Egress Runtime

Verify:

- egress exists in `egress.registry`;
- enabled egress has expected interface/process;
- interface is up when registry says usable;
- interface is not silently production-active when registry says quarantine/maintenance/disabled.

### Route Class

Verify:

- service/domain maps to an authoritative route class;
- route class allows the selected egress type;
- route class failover rules are respected;
- direct/RU route class is not used as general bypass.

### Linux Policy Routing

Verify:

- required `ip rule` exists;
- rule priority is unambiguous;
- expected table exists;
- table default route points to assigned egress;
- direct mark rule does not catch unmarked VPN client traffic.

### Effective Interface

Verify with read-only route checks:

- expected client source selects expected route table;
- expected destination selects assigned egress;
- direct destinations use direct exception only when policy allows it;
- non-direct destinations do not leak to public interface.

### DNS Path

Verify:

- DNS capture exists when required;
- DNS for direct/RU policy does not bypass safety model;
- DNS path does not contradict route class.

### MTU and MSS

Verify:

- transport MTU is sane for assigned egress;
- MSS clamp exists where required;
- MTU instability is reported as degraded, not hidden as healthy.

### NAT

Verify:

- expected NAT is present for egress path;
- NAT does not create a public leak path for protected VPN subnets;
- direct NAT behavior is explicit.

### Trusted RU

Verify:

- trusted RU policy has explicit route/domain basis;
- trusted RU degradation is visible;
- trusted RU does not silently fallback to unsafe routing.

## Result Categories

- `verified`: effective datapath matches desired policy.
- `degraded`: datapath is available but has safety/performance warnings.
- `mismatch`: runtime contradicts desired state.
- `blocked`: safety invariant cannot be verified.
- `unknown`: insufficient information; must not be shown as healthy.

## Operator Presentation

Summary first:

- verified users;
- impacted users;
- blocker count;
- highest-risk mismatch;
- suggested bounded action.

Details on drill-down:

- selected route table;
- selected interface;
- relevant nft/ip rule snippets;
- registry row references;
- timestamps.

## Phase 1 Boundary

This document defines route verification requirements. It does not add active traffic migration or modify route selection.
