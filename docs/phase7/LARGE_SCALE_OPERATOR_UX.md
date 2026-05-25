# V7 Phase 7 Large-Scale Operator UX

## Purpose

The UI must stay calm with more channels, users, orgs, and incidents.

## Scaling Rules

- overview shows summaries, not full tables;
- lists need search/filter/grouping;
- incident-centric workflows remain primary;
- resource/capacity warnings are compressed;
- raw telemetry is drill-down only;
- route visualization remains simplified.

## Scale Targets

Usable with:

- 50 egress;
- 500 users;
- multiple organizations;
- large incident history;
- frequent diagnostics updates.

## Anti-Patterns

Do not solve scale by:

- showing bigger tables;
- adding more dashboard panels;
- adding more primary nav tabs;
- exposing every metric.

## Preferred Views

- `3 degraded channels`;
- `42 affected users`;
- `1 route class blocked`;
- `backup verification stale`;
- `autoswitch frozen by safety state`.

