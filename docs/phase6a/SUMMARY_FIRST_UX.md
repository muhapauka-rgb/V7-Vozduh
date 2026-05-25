# V7 Phase 6A Summary-First UX

## Purpose

Main screens must make the operator calmer and faster.

They should not demonstrate how much telemetry the system has.

## Required Summary Fields

Every summary card should include:

- status;
- impact;
- reason;
- urgency;
- safe next action;
- drill-down target.

## Overview Content

The overview should prioritize:

- system healthy/degraded;
- incidents requiring attention;
- affected users;
- degraded channels;
- trusted RU status;
- autoswitch status;
- kill switch status.

## What Stays Secondary

These belong behind drill-down:

- detailed channel matrices;
- route reality rows;
- long event streams;
- command output;
- MTU details;
- interface internals.

## Current Admin Reading

The current `admin-v2` already has a summary-first intent through metrics, alerts, and drawers. The main risk is that routing, checks, logs, and settings workspaces can become table-first as the platform grows.

