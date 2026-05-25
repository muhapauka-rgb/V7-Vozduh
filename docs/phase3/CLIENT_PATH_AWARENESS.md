# V7 Phase 3 - Client Path Awareness

## Purpose

Server-side checks are necessary but insufficient.

V7 must understand client-visible quality without invasive tracking.

## Client Signals

Allowed bounded signals:

- client-side latency;
- reconnect frequency;
- last-mile degradation;
- mobile instability;
- roaming changes;
- client throughput;
- ingress type;
- egress id;
- path profile.

Existing related components:

- `tools/v7-client-speed-api`;
- `tools/v7-path-sample-ingest`;
- `tools/v7-path-benchmark`;
- `client-reconnect-state.json`.

## Privacy And Safety

Client telemetry must be:

- minimal;
- bounded;
- purpose-specific;
- free of browsing history;
- free of payload inspection;
- tied to routing health only.

## Interpretation

Client path issue examples:

- server-to-egress fast, client-to-egress slow: likely ingress/last-mile issue;
- reconnect spikes on one user: user/client instability;
- reconnect spikes on many users on same egress: egress or route instability;
- low throughput only on one ingress type: transport-specific path issue.

## Operator View

Summary:

- affected users count;
- likely client-side vs egress-side;
- safe next action.

Drill-down:

- latest samples;
- ingress type;
- egress id;
- reconnect event timestamps.
