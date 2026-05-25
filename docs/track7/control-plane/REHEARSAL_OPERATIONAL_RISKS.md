# Rehearsal Operational Risks

This document records risks for a future quiet-window rehearsal. It was not executed in Block E7.

## Primary Risk

The rehearsal pauses autoswitch authority. Existing datapath should continue, but automated user movement is temporarily unavailable. The blast radius is all users who would otherwise be eligible for autoswitch during the window.

## Partial Hold Risks

- timer stopped but service remains active;
- service stopped but child `v7-user-switch` or `v7-routing-sync` remains;
- timer reactivates during observation;
- operator mistakes timer inactive state for full quiet state.

Mitigation: process checks after every hold phase.

## Stale State Risks

- registry snapshot may be stable but health/load state stale;
- reconcile may pass under quiet window while later autoswitch writes reintroduce races;
- Trusted RU state may remain stale and unrelated to rehearsal success.

Mitigation: treat rehearsal success as necessary but not sufficient for canary.

## Human Operator Risks

- running a forbidden command from muscle memory;
- forgetting restore;
- interpreting a warning as permission to repair;
- copying commands into the wrong shell or host;
- extending the hold beyond approved duration.

Mitigation: one operator executes, one reviewer watches, and restore is verified before analysis.

## Mistaken Restore Risks

- starting the service manually when only timer restore was intended;
- failing to notice timer not listed after start;
- restoring different authority from pre-hold state;
- leaving autoswitch inactive after evidence collection.

Mitigation: compare `systemctl-active.before.txt`, `systemctl-enabled.before.txt`, and post-restore captures.

## Observational Blind Spots

- route/rule snapshots do not prove every client path works;
- kill switch check may not cover every future route mutation;
- quiet state does not prove policy apply safety;
- no customer experience validation occurs;
- no canary traffic is moved.

## Current Risk Status

```text
rehearsal_planned
runtime_mutation_performed=false
canary_allowed=false
```
