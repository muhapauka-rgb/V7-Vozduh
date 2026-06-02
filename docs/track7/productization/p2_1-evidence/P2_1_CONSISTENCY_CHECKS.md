# P2.1 Consistency Checks

## Checks Implemented

Execution store consistency checks report:

- contract count
- event count
- duplicate contract ids
- orphan events
- invalid contracts
- store existence
- event store existence

Invalid contract conditions:

- missing contract id
- missing rollback manifest
- movement budget lower than affected user count
- blast radius lower than affected user count

## Status Model

`OK`:
contracts/events exist and no blocking consistency issue is found.

`EMPTY`:
stores are empty or absent; this is allowed for read-only foundation.

`WARN`:
orphan events exist.

`FAILED_CLOSED`:
duplicate contract ids or invalid contract structure exists.

## Safety

Consistency checks are informational only.

They do not:

- repair stores
- mutate runtime
- move users
- change routing
- apply autoswitch

## Verdict

consistency_checks_implemented=true
fail_closed_status_available=true
runtime_mutation_performed=false
