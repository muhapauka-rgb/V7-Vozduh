# V7 Phase 4 - Compact Autoswitch UX

## Purpose

Autoswitch UI must explain decisions without turning into a NOC dashboard.

## Summary First

Show:

- affected users;
- degraded channels;
- suggested action;
- switch reason summary;
- confidence;
- anti-flap state.

## Drill-Down Only

Hide by default:

- full candidate matrix;
- every score part;
- raw service samples;
- all safety JSON.

## Decision Card

Each switch/keep decision should show:

- current egress;
- recommended egress;
- action;
- move type;
- confidence;
- top reason;
- blockers if not switching.

## Operator Trust

Operator must be able to answer:

- why did V7 switch;
- why did V7 not switch;
- how many users are affected;
- how to roll back;
- whether safety gates passed.
