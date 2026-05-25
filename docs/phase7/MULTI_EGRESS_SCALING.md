# V7 Phase 7 Multi-Egress Scaling

## Purpose

V7 must remain predictable with dozens of egress channels, mixed transports, route classes, quarantine groups, and maintenance flows.

## Scaling Requirements

The platform must handle:

- dozens of egress;
- mixed transports;
- multiple route classes;
- quarantine and maintenance pools;
- organization-level eligibility;
- service-specific degradation.

## Scaling Rules

- autoswitch must remain bounded per run;
- service matrix checks must be rate-limited and summarized;
- UI must show grouped summaries before tables;
- route class eligibility must be computed from policy and lifecycle state;
- quarantined or maintenance egress must not participate in production routing.

## Bottleneck Watchlist

- full service matrix refresh across all egress;
- frequent Telegram sentinel checks;
- autoswitch timer frequency;
- large `users.registry`;
- large `egress.registry`;
- route reality table growth;
- event stream size.

## Operator View

Show:

- healthy/degraded/maintenance/quarantined counts;
- route class capacity;
- affected user/org count;
- top incidents.

Do not show:

- every probe;
- every route table row;
- every per-egress raw metric on the overview.

