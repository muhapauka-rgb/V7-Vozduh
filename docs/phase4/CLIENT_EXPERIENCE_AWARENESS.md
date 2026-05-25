# V7 Phase 4 Client Experience Awareness

## Purpose

A tunnel can be technically alive while the user experience is poor. Autoswitch must include bounded client-side signals without turning V7 into invasive telemetry.

## Allowed Signals

Client experience awareness may use:

- reconnect frequency;
- session instability;
- client-side throughput summary;
- app startup delays when available as bounded counters;
- mobile roaming hints when explicitly exposed;
- last successful activity age.

## Forbidden Signals

Autoswitch must not require invasive content inspection, broad tracking, or user behavior profiling.

## Interpretation Rules

Reconnect spikes can mean:

- egress degradation;
- last-mile instability;
- mobile roaming;
- overloaded server;
- bad target after previous switch.

Autoswitch should not assume all reconnects are egress failures. Client-local instability should produce diagnostics and low-confidence movement unless supported by route or service evidence.

## Decision Impact

Client signals may:

- increase confidence when they correlate with egress/service degradation;
- reduce confidence when they are isolated to one client;
- trigger freeze after repeated failed movement;
- suggest operator review for last-mile instability.

## Operator Summary

Client experience should be shown as compact summaries:

- reconnect loops observed;
- affected users;
- likely scope;
- suggested safe action.

Raw per-client telemetry belongs behind drill-down.

