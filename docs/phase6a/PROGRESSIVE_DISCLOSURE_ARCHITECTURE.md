# V7 Phase 6A Progressive Disclosure Architecture

## Purpose

Complexity should be reachable, not dumped.

The UI pattern is:

summary -> details -> diagnostics -> telemetry

## Block Contract

Every operator block should support:

- summary: one status, one impact statement, one next action;
- details: grouped reasons and affected objects;
- diagnostics: verification evidence;
- telemetry: raw or near-raw technical details.

## Good Flow

`2 degraded channels`

Then:

- details: affected services and users;
- diagnostics: route/service/MTU checks;
- telemetry: command output or raw JSON.

## Forbidden Flow

Do not start with:

- 300 metric rows;
- full route reality table;
- full service matrix;
- all audit events;
- raw Linux internals.

## Drawer Use

Drawers are the preferred detail layer for:

- incident details;
- route class evidence;
- affected users;
- channel readiness;
- trusted RU explanations;
- autoswitch decision summaries.

Full pages should remain workflow containers, not telemetry dumps.

## Runtime Compatibility

This document does not require a rewrite of the current embedded admin. Future extraction should preserve existing drawer/detail behavior and reduce table-first screens incrementally.

