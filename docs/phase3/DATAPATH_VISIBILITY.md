# V7 Phase 3 - Datapath Visibility

## Purpose

Operator must see actual datapath, not just "tunnel alive".

## Required Datapath Fields

Show:

- user;
- route class;
- assigned egress;
- effective interface;
- DNS path;
- direct route usage;
- trusted RU usage;
- active degradation;
- verification status.

## Datapath Evidence

Evidence sources:

- `users.registry`;
- `egress.registry`;
- route class registry/policy;
- `ip route get`;
- `ip rule`;
- nftables checks;
- kill switch check;
- provisioning reconcile check;
- service matrix;
- direct/RU diagnostics.

## Display Rule

Default view:

- verified/mismatch/unknown count;
- affected users;
- highest risk.

Drill-down:

- route table;
- selected interface;
- DNS capture status;
- direct mark/table evidence;
- raw checks.

## Trusted RU Rule

If trusted RU cannot be verified, show degraded/blocker state.

Never display unsafe fallback as healthy.
