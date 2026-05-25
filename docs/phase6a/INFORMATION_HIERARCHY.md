# V7 Phase 6A Information Hierarchy

## Purpose

Phase 6A integrates routing, diagnostics, observability, autoswitch, and platform state without turning the admin into an engineering cockpit.

The hierarchy is:

1. understanding;
2. decision context;
3. technical evidence.

The operator should see what matters first and open detail only when needed.

## Level 1 - Operator Summary

Level 1 is the first visible layer on overview and workflow pages.

It may show:

- overall platform state;
- active incidents;
- degraded channels;
- affected users or organizations;
- required actions;
- kill switch posture;
- trusted RU posture;
- autoswitch posture.

It must answer:

- what is happening;
- who is affected;
- how serious it is;
- what safe action is next.

It must not show:

- raw command output;
- full service matrices;
- route table internals;
- per-interface telemetry;
- every event row.

## Level 2 - Grouped Diagnostics

Level 2 appears after selecting a summary item or workflow group.

Groups:

- Channels;
- Routing;
- Services;
- Users;
- Trusted RU;
- Autoswitch;
- Security;
- Provisioning.

Each group should show:

- current status;
- affected object count;
- likely reason;
- evidence summary;
- suggested safe action;
- drill-down target.

## Level 3 - Technical Evidence

Level 3 is deep diagnostic context.

It may include:

- MTU and path diagnostics;
- interface/runtime details;
- command summaries;
- route reality rows;
- event history;
- service matrix rows;
- raw JSON only when explicitly opened.

Level 3 is never the default state of a page.

## IA Rule

No new page, panel, or card should expose Level 3 data unless Level 1 and Level 2 context already exists for the same concern.

