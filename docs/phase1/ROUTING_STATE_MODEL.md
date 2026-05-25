# V7 Phase 1 - Routing State Model

## Purpose

This document formalizes routing state ownership for V7 without changing runtime behavior.

Phase 1 treats routing as a reconciliation problem:

1. desired state declares what should exist;
2. runtime state shows what Linux is currently doing;
3. observed state summarizes measurements and diagnostics;
4. effective state proves what packets actually experience.

No observed metric or UI value is allowed to silently override policy. Runtime must be reconciled toward desired state, and effective datapath must be verified before trust.

## State Layers

### Desired State

Desired state is the operator/platform intent.

Primary sources:

- `/opt/v7/state/users.registry`
- `/opt/v7/state/egress.registry`
- `/opt/v7/policy.json`
- `/opt/v7/org-egress-policy.json`
- route-class domain/config files exposed through admin policy views
- identity SQLite database for user/org/device lifecycle ownership

Desired state answers:

- which user should exist;
- which egress a user is assigned to;
- which egresses are enabled, disabled, drained, or quarantined;
- which route class applies to a service or policy;
- which direct/RU routes are explicitly allowed;
- which organization policy bounds the decision.

Desired state is not proof that Linux runtime matches intent.

### Runtime State

Runtime state is what the host kernel and services currently hold.

Primary runtime surfaces:

- Linux interfaces: `wg0`, `awg*`, `tun*`, `sb-*`, egress devices;
- `ip rule`;
- route tables, including per-user tables and direct table `70`;
- nftables table `inet v7`;
- iptables NAT and TCPMSS rules where still used;
- dnsmasq/direct DNS capture runtime;
- systemd unit state;
- transport processes such as WireGuard, AmneziaWG, OpenVPN, and sing-box.

Runtime state answers:

- whether interfaces exist and are up;
- whether packet marks map to the intended tables;
- whether VPN client subnets are isolated from public leak paths;
- whether NAT/MSS behavior exists for expected egresses;
- whether direct/RU exception routes are constrained.

Runtime state is not automatically safe; it must be compared to desired state.

### Observed State

Observed state is diagnostic and measurement output.

Known observed files and tools:

- `/opt/v7/state/service-matrix.json`
- `/opt/v7/state/egress-quality-summary.json`
- `/opt/v7/state/autoswitch-safety.json`
- `/opt/v7/state/v7-state.json`
- `/opt/v7/state/direct-ru-diagnostics.json`
- Telegram sentinel outputs
- speed and quality summaries
- route check command output

Observed state answers:

- which services appear degraded;
- which egress appears unstable;
- whether autoswitch safety bounds are active;
- whether direct/RU diagnostics found blockers;
- whether health signals indicate drift.

Observed state may be stale or partial. It can recommend investigation, but it cannot silently change policy.

### Effective State

Effective state is the verified packet outcome.

Effective state is derived from controlled read-only checks such as:

- `ip route get`;
- `ip rule show`;
- `ip route show table <id>`;
- `nft list table inet v7`;
- interface state inspection;
- DNS path checks;
- route verification helpers.

Effective state answers:

- which interface traffic would actually use;
- which route table is selected;
- which mark is expected;
- whether DNS follows the policy path;
- whether direct/RU routes stay inside the explicit exception;
- whether VPN subnets can leak through public interface.

Effective state is the final verification surface for datapath safety.

## Source Of Truth Hierarchy

The Phase 1 hierarchy is:

1. Governance invariants and route-class policy.
2. Desired state registries and policy files.
3. Runtime Linux/networking state reconciled toward desired state.
4. Observed diagnostics used to explain health and risk.
5. Effective datapath checks used to verify safety.

If layers disagree:

- desired state must not be mutated implicitly;
- runtime mismatch must be reported;
- observed state must be marked stale or degraded when not reconcilable;
- effective unsafe behavior must become a blocker;
- repair must be bounded, audited, and verified after action.

## State Transition Rules

Allowed Phase 1 transition pattern:

1. parse desired state safely;
2. inspect runtime state read-only;
3. compare expected vs actual;
4. classify mismatch severity;
5. propose or perform bounded repair only through existing safe tooling;
6. verify effective datapath;
7. write audit event for risky action.

Forbidden transition pattern:

1. observe latency spike;
2. silently change route;
3. update UI as if policy changed;
4. skip kill switch verification.

## Runtime/UI Consistency Rule

UI state must describe either:

- desired state;
- observed state with timestamp;
- effective verified state;
- explicit mismatch state.

UI must not present stale observed state as runtime truth.

## Phase 1 Boundary

This model does not move files, change registries, or alter runtime routing. It defines how future checks and repair actions must reason about state.
