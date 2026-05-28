# E11.2 Second Canary Simulation

Simulation only. No user-switch, routing mutation, reservation mutation, or
canary execution was performed.

Assumed future preconditions:

```text
wireguard reservation applied=true
restore_settle_gate=GO
runtime_checks=OK
hidden_user_switch=false
hidden_routing_sync=false
candidate selected fresh at execution packet time
```

## Expected Target

```text
expected_selected_target=wireguard-1779454504-c43409
target_status=CONDITIONAL_RESERVED_TARGET
waiver_required=true
```

If diagnose semantics are fixed so live fresh handshake clears the persisted
SUSPECT state:

```text
expected_second_canary_readiness=GO
```

If diagnose remains `SUSPECT` but the stale-handshake waiver is accepted:

```text
expected_second_canary_readiness=CONDITIONAL
```

## Candidate

The candidate must be selected fresh in the next canary approval packet.
Do not reuse stale candidates from E9/E10 without another read-only snapshot.

Expected candidate requirements:

```text
enabled=1
current stable
not recently moved
table route sane
route_get sane
rollback target explicit
not Trusted RU sensitive
```

## Restore Lifecycle

Future execution must use the staged lifecycle:

```text
hold planner/apply
execute one approved canary user-switch
observe quiet-window
rollback or explicitly keep
restore planner only
run restore-settle gate across >=2 apply intervals
restore apply only if settle gate GO
post-restore settle monitoring
```

## Remaining Blockers

```text
reservation_not_applied=true
diagnose_semantics_not_fixed=true
waiver_not_yet_approved_for_execution=true
fresh_candidate_not_selected=true
execution_allowed_now=false
```
