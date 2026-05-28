# E9.3.7 Fixture Test Plan

Mode: repo-side fixture tests only.
Runtime mutation: no.

## Purpose

The fixture tests should prove the proposed policy semantics before any runtime policy change:

```text
single transient service failure -> degraded/penalized, not global failover
persistent or multi-signal failure -> conditional/hard ineligibility
transport failure -> immediate hard ineligibility
restore stage -> bounded movement requires explicit approval
```

## Fixtures

### 1. Instagram Single-Sample Failure

Inputs:

```text
service_instagram_failed samples=1
telegram=OK or DEGRADED not hard-blocked
interface=UP
route/user/checkers=OK
```

Expected:

```text
egress_state=DEGRADED_SERVICE
global_eligible=true
selected_moves=0
```

### 2. Instagram Persistent Failure

Inputs:

```text
service_instagram_failed samples=3
window_seconds<=180
interface=UP
```

Expected:

```text
egress_state=CONDITIONAL_INELIGIBLE
global_eligible=false or apply_requires_approval=true
selected_moves<=max_failover_per_restore_stage during restore stage
```

### 3. Telegram Degraded Not Hard-Blocked

Inputs:

```text
telegram.status=DEGRADED
telegram.hard_blocked=false
other services OK
```

Expected:

```text
egress_state=DEGRADED_SERVICE
global_eligible=true
selected_moves=0
```

### 4. Interface Down

Inputs:

```text
interface=DOWN
services unknown or OK
```

Expected:

```text
egress_state=HARD_INELIGIBLE
global_eligible=false
failover_allowed=true
```

### 5. Multiple Critical Services Failed

Inputs:

```text
instagram failed
youtube failed
interface=UP
```

Expected:

```text
egress_state=CONDITIONAL_INELIGIBLE
global_eligible=false or apply_requires_approval=true
```

### 6. Post-Restore Stage

Inputs:

```text
restore_stage=true
single service failure
selected_moves would be broad under old policy
```

Expected:

```text
selected_moves=0
apply_restore_allowed=false unless operator explicitly approves exact bounded moves
```

## Implemented Repo-Side Tests

`tests/unit/test_v7_autoswitch_policy_design.py` implements a small pure-Python design fixture model for the proposed policy. It does not import runtime state, run autoswitch, start timers, call user-switch, or mutate files outside temporary unittest state.

The tests are intentionally design-contract tests. They are not a deployed policy change.

