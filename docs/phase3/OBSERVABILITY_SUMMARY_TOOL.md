# V7 Phase 3 - Observability Summary Tool

## Purpose

Phase 3 adds a read-only summary tool:

- `tools/v7-observability-summary`

It creates a compact operator-first JSON snapshot from existing state files.

## Properties

The tool:

- reads only;
- does not run network probes;
- does not write state;
- does not change routes;
- does not rebuild nftables;
- does not trigger autoswitch;
- does not mutate provisioning.

## Inputs

It can summarize:

- `egress.registry`;
- `users.registry`;
- `service-matrix.json`;
- `telegram-sentinel.json`;
- `egress-quality-summary.json`;
- `autoswitch-safety.json`;
- `client-reconnect-state.json`;
- `path-benchmark.json`;
- `path-optimizer-advice.json`;
- `direct-ru-diagnostics.json`.

## Output Shape

Output groups:

- system;
- routing;
- channels;
- services;
- users;
- trusted_ru;
- autoswitch;
- provisioning;
- security;
- direct_routing.

Each group has:

- status;
- severity;
- reason;
- affected count;
- suggested action.

## Phase 3 Boundary

This tool is a summary foundation, not a new UI and not an alert engine.
