# V7 Phase 7 Capacity And Resource Model

## Purpose

Capacity awareness prevents silent overload and unsafe autoswitch/provisioning decisions.

## Capacity Signals

Track compactly:

- users per egress;
- active users per egress;
- service quality per egress;
- reconnect pressure;
- throughput trend;
- degradation frequency;
- maintenance/quarantine availability;
- route class eligibility.

## Resource Signals

Track as operator summaries:

- CPU pressure;
- RAM pressure;
- conntrack pressure;
- nftables size/growth;
- routing table size/growth;
- file descriptor pressure;
- process health;
- disk space for state, events, audit, backups.

## Decision Rules

Autoswitch should avoid targets when:

- target is overloaded;
- target is quarantined;
- target is in maintenance;
- target has chronic instability;
- target lacks route class eligibility;
- alternate capacity is not verified.

Provisioning should block enable when:

- dependencies are missing;
- runtime test fails;
- kill switch compatibility is unknown;
- state writes cannot be backed up;
- disk pressure threatens state persistence.

## UI Rule

Resource data must appear as:

- `capacity ok`;
- `capacity warning`;
- `resource pressure`;
- `operator action required`.

Raw metrics belong in drill-down only.

