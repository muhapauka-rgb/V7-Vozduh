# V7 Phase 6 Performance And Scalability UX

## Purpose

Admin UI must scale to more users, egress channels, and incidents without visual collapse.

## Scaling Targets

The UI should stay usable with:

- dozens of egress channels;
- hundreds of users;
- large incident histories;
- multiple organizations;
- frequent diagnostics updates.

## UX Requirements

- summary counts before tables;
- search and filtering;
- pagination or virtualized tables later;
- grouped incidents;
- compact per-organization summaries;
- bounded live refresh.

## Current Risk

Current embedded UI has large tables and repeated render functions. It can work now, but future growth needs modular rendering and data adapters.

## Future Rule

Do not solve scaling with more dashboard density.

Solve it with grouping, summaries, filters, and drill-down.

