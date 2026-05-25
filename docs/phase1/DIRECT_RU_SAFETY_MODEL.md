# V7 Phase 1 - Direct/RU Safety Model

## Purpose

Direct routing is a controlled exception, not a bypass mode.

This model defines how direct/RU behavior must be reasoned about in Phase 1 without changing runtime behavior.

## Core Invariant

Protected VPN client subnets must not leak directly through the public interface:

- `10.0.0.0/24`
- `10.7.0.0/22`

Direct/RU routing is allowed only for explicitly marked and policy-approved traffic.

## Required Runtime Boundaries

Direct/RU safety depends on:

- explicit fwmark;
- direct policy rule;
- direct route table `70`;
- controlled destination/domain allow logic;
- DNS capture or equivalent explicit DNS policy;
- nftables protection for client subnets;
- no unmarked public forwarding path.

## Trusted RU Behavior

`TRUSTED_RU_SENSITIVE` must prefer visible degraded/blocker state over unsafe fallback.

Allowed:

- report direct/RU degraded;
- recommend operator action;
- quarantine affected direct/RU path;
- use explicit policy-approved fallback if verified.

Forbidden:

- silently route trusted RU sensitive traffic through unsafe public path;
- silently downgrade to general `DIRECT_RU`;
- treat missing DNS/direct rules as healthy;
- bypass route classes under failure.

## Verification Checklist

Read-only verification should confirm:

- fwmark rule exists and has expected priority;
- table `70` exists;
- table `70` default route is expected;
- nft direct allow set exists when policy uses it;
- DNS capture is present when direct/RU depends on it;
- unmarked traffic from protected VPN subnets cannot use public interface;
- trusted RU degradation is visible in diagnostics.

## Operator Output

Summary:

- direct/RU status;
- trusted RU status;
- blocker/degraded count;
- whether fallback is safe, unsafe, or unavailable.

Details:

- mark rule;
- table `70`;
- DNS capture state;
- matched policy file/domain source;
- effective route check.

## Phase 1 Boundary

This document formalizes safety. It does not enable, disable, or alter direct/RU routing.
