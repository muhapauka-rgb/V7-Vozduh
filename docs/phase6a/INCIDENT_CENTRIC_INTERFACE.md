# V7 Phase 6A Incident-Centric Interface

## Purpose

Incidents are the bridge between platform intelligence and operator action.

The interface should start from the incident, not from raw telemetry.

## Incident Summary Contract

Each incident summary should include:

- title;
- severity;
- affected users, orgs, channels, or route classes;
- probable cause;
- current state;
- suggested safe action;
- rollback or safety implication;
- verification state.

## Incident Detail Contract

Incident detail may show:

- grouped evidence;
- event correlation;
- impacted route classes;
- impacted services;
- related autoswitch decisions;
- related provisioning actions.

## Forbidden Patterns

Do not make incidents look like:

- a raw log stream;
- a wall of charts;
- a network topology graph;
- an ungrouped list of metrics.

## Operator Outcome

The operator should be able to say:

- what is broken;
- who is affected;
- how bad it is;
- what to do next;
- what not to do.

