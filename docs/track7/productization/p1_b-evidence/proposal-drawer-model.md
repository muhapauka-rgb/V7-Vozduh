# P1.B Proposal Drawer Model

proposal_drawer_defined=true

## Drawer Purpose

Proposal Drawer is the shared admin component for inspecting a recommendation before it can enter governance.

## Required Sections

### Summary

Shows:

- proposal type;
- status;
- severity;
- short reason;
- primary object;
- proposed outcome.

### Confidence

Shows:

- confidence level;
- evidence freshness;
- signal agreement;
- known blockers;
- missing evidence.

### Impact

Shows:

- affected users;
- target/channel;
- route classes if relevant;
- required services;
- blast radius estimate;
- current vs proposed state.

### Affected Users

Shows:

- exact user list;
- current target;
- proposed target;
- required services;
- route table when relevant.

### Required Services

Shows:

- mandatory services;
- current channel support;
- proposed channel support;
- service-health blockers.

### Evidence Link

Shows:

- primary Evidence Bundle;
- supporting bundles;
- link to Evidence Drawer.

### Expected Benefit

Shows:

- service satisfaction improvement;
- quality/readiness improvement;
- capacity/load impact;
- risk reduction.

### Rollback Hint

Shows:

- rollback target;
- rollback scope;
- rollback constraints.

This is a hint only. Governance still must produce a rollback manifest.

### Governance Path

Shows:

```text
Proposal
-> Batch
-> Policy
-> Capacity
-> Concurrency
-> Scheduling
-> Execution-Time Recheck
-> Execution
```

### Advanced Details

Shows role-gated:

- score inputs;
- routing intelligence details;
- policy context;
- source references;
- raw but redacted payload snippets.

## Drawer Verdict

Proposal Drawer helps the operator understand and review. It never bypasses approval packets, runtime gates or execution-time recheck.
