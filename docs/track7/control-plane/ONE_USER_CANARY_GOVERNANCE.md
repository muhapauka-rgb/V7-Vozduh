# One-User Canary Governance

This document defines future governance for a one-user canary. It does not authorize or execute the canary.

## Approval

A future one-user canary requires explicit operator approval naming:

- user IP;
- current egress;
- target egress;
- rollback egress;
- canary window;
- autoswitch hold plan;
- stop conditions;
- rollback authority.

Approval is valid only for the named user and target. It does not approve routing-sync, autoswitch apply, policy apply, Direct/RU mutation, proxy apply, or broader migration.

## Execution Authority

Only an operator with control-plane responsibility may execute the future canary. The execution must be manual, observed, and bounded. Automation must not choose or expand the candidate during the canary window.

## Required Pre-Canary Packet

```text
candidate user
from egress
to egress
route table
target interface
forward preview JSON
rollback preview JSON
kill switch status
user route check status
provisioning reconcile status
reconcile status or approved explanation
autoswitch hold confirmation
target egress readiness
operator approval
```

## Blast Radius Control

- one user only;
- no `v7-routing-sync` as first mutation;
- no autoswitch apply during observation;
- no policy/Direct/RU/proxy mutation;
- no kill switch rebuild unless separately approved;
- no automatic escalation to multi-user movement.

## Rollback Readiness

Rollback must be known before the canary. For the current conditional candidate:

```text
v7-user-switch 10.7.0.13 awg0
```

Rollback is mutation and requires the same observation discipline as the forward switch.

## Autoswitch Non-Interference

Before execution, the operator must prove autoswitch cannot concurrently move users. A canary is invalid if autoswitch can run `--apply` during the window.

## Automatic Failure Conditions

The canary fails if any occur:

- user route table does not point to target interface;
- registry/assignment mismatch appears;
- kill switch check warns or fails;
- route check warns or fails;
- target egress health falls below accepted threshold;
- autoswitch moves any user during the window;
- unexpected policy/Direct/RU/proxy state changes appear;
- rollback command cannot be executed promptly when needed.

## Result Recording

The operator must record:

- exact commands run;
- timestamps;
- pre/post check outputs;
- forward and rollback preview hashes;
- whether rollback was needed;
- observed user impact;
- final assignment and route state;
- whether autoswitch authority was restored.

## Verdict

The governance model exists, but canary remains NO-GO under current evidence.
