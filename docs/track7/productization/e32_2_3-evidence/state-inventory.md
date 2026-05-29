# E32.2.3 State Inventory

state_inventory_defined=true

## Scope

This inventory classifies the batch states defined in E32.2.2 into transient and terminal states.

No runtime mutation, user movement, routing mutation, autoswitch apply, UI execution, canary, or cohort execution was performed.

## State List

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

## Transient States

Transient states are states from which the batch must move to another state or be denied/expired.

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
```

## Terminal States

Terminal states end the current batch lifecycle.

```text
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

## Terminal State Semantics

### COMPLETED

The batch completed required execution, observation, rollback if required, replay validation, audit closure, and final checks.

### FAILED_CLOSED

The batch failed without expanding scope. Forward execution is denied. Containment may require a separate containment or rollback batch if exact scope is known.

### REPLAY_DENIED

A replay attempt was detected and denied. No movement or routing mutation may occur.

### CANCELLED

The batch was cancelled before execution. It cannot be resumed without a new generation or new batch.

### EXPIRED

The execution window expired. Forward execution is denied. A fresh batch or packet is required.

## Inventory Verdict

State inventory is defined.

