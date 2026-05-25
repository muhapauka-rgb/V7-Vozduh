# V7 Phase 4 Autoswitch Audit And Operator UX

## Purpose

Autoswitch must be trusted because it is explainable, observable, and bounded.

## Audit Requirements

Every applied switch action must include:

- timestamp;
- actor;
- reason;
- confidence;
- source egress;
- target egress;
- affected user or group;
- route class;
- before state;
- after state;
- verification result;
- rollback context.

## Decision Visibility

Dry-run and guarded apply output should show:

- planned moves;
- skipped users;
- rejected candidates;
- active cooldown/freeze;
- degraded services;
- confidence level;
- safety blockers.

## Compact Operator UX

Main overview should show:

- autoswitch mode;
- active degraded channels;
- affected users;
- last switch reason;
- confidence;
- pending safe action;
- quarantine/freeze summary.

It should not show raw scoring tables by default.

## Drill-Down UX

Detailed diagnostics may expose:

- candidate scoring;
- evidence samples;
- route-class gates;
- load calculations;
- rejected candidate reasons;
- historical reliability summaries.

## Alert Philosophy

Autoswitch alerts should be:

- grouped;
- deduplicated;
- severity-aware;
- actionable.

No alert should exist only to display raw telemetry.

