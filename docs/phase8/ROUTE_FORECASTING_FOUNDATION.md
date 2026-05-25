# V7 Phase 8 Route Forecasting Foundation

## Purpose

Forecast route risk without uncontrolled auto-routing.

## Forecast Types

- probable degradation;
- overload risk;
- unstable route prediction;
- route class service risk;
- trusted RU degradation risk;
- stealth escalation need.

## Inputs

- service matrix;
- Telegram sentinel;
- egress quality summary;
- client reconnect state;
- path benchmark;
- path optimizer advice;
- autoswitch safety;
- quarantine/maintenance history;
- route class policy.

## Output Contract

Forecast output must include:

- target object;
- forecast type;
- confidence;
- evidence;
- safety bounds;
- recommended operator action;
- blocked automatic actions.

## Boundary

Forecasting is not a routing engine.

It feeds operator assistance and bounded autoswitch hooks only.

