# V7 Phase 8 Predictive Degradation Detection

## Purpose

Detect dying channels before complete failure while avoiding panic-switch behavior.

## Signals

Use bounded summaries of:

- latency drift;
- reconnect growth;
- packet loss trends;
- MTU instability;
- service degradation patterns;
- route verification failures;
- Telegram instability;
- quality score degradation;
- chronic maintenance/quarantine history.

## Prediction States

watch:

- one weak signal;
- no action except observation.

likely_degrading:

- multiple weak signals or one persistent strong signal;
- suggest diagnostics or maintenance review.

high_risk:

- multi-signal persistent degradation with affected users or services;
- suggest quarantine, maintenance, or bounded autoswitch review.

## Anti-Flapping Rule

Predictions are not switches.

Predictions only raise confidence for already-bounded autoswitch or operator workflows.

## Explanation Contract

Every prediction must explain:

- which signals changed;
- over what window;
- affected objects;
- confidence;
- safe next action.

