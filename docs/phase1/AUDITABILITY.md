# V7 Phase 1 - Auditability

## Purpose

Every risky routing or runtime action must be attributable, explainable, bounded, and reversible where possible.

Phase 1 does not add new dangerous actions. It defines the audit contract for future repair and reconciliation work.

## Dangerous Action Definition

An action is dangerous when it can affect:

- kill switch;
- nftables;
- route tables;
- direct/RU behavior;
- user egress assignment;
- egress enabled/quarantine/maintenance state;
- autoswitch apply behavior;
- provisioning activation;
- transport interface restart.

## Required Audit Fields

Every dangerous action must capture:

- timestamp;
- actor;
- reason;
- command/tool;
- target user/egress/service;
- before state;
- after state;
- rollback context;
- verification result;
- correlation id when part of a multi-step operation.

## Reason Quality

Good reasons:

- `repair missing ip rule for user table 1007 after reconcile mismatch`
- `quarantine egress awg3 after persistent blocked health state`
- `rebuild kill switch after nft table missing verification`

Bad reasons:

- `fix`
- `auto`
- `AI said so`
- empty reason.

## Repair Audit Flow

Required flow:

1. detect mismatch;
2. create proposed action;
3. capture before state;
4. apply bounded action;
5. verify effective datapath;
6. capture after state;
7. write audit event;
8. show operator result.

If verification fails after action, audit must include failure and recommended rollback/manual intervention.

## Read-Only Diagnostics

Read-only diagnostics do not require full dangerous-action audit, but should still expose:

- timestamp;
- source;
- state files inspected;
- runtime commands inspected;
- findings.

## Phase 1 Boundary

This file defines the audit contract. It does not change existing audit log behavior.
