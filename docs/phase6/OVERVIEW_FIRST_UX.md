# V7 Phase 6 Overview-First UX

## Purpose

The first screen must answer operational questions before showing details.

## Required Overview Items

- system healthy/degraded;
- affected users;
- degraded channels;
- autoswitch state;
- trusted RU status;
- incidents requiring attention;
- kill switch posture;
- pending safe actions.

## Forbidden Overview Patterns

The overview must not start with:

- every metric;
- full service matrix;
- raw logs;
- giant user table;
- giant channel table;
- network graph.

## Summary Contract

Each overview item should include:

- status;
- impact count;
- reason summary;
- suggested action;
- drill-down target.

## Current Compatibility

Current `admin-v2` already has overview metrics and alerts. Phase 6 should preserve the summary-first intent while moving rendering into smaller modules later.

