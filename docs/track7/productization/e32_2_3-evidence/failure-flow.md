# E32.2.3 Failure Flow

failure_flow_defined=true

## FAILED_CLOSED

Entry conditions:

- metadata invalid;
- approval invalid;
- execution-time recheck failed;
- capacity gate failed;
- runtime checker failed;
- selected moves appeared;
- hidden movers appeared;
- exact scope mismatch;
- partial execution requires containment.

Operator actions:

- inspect denial reason;
- repair metadata if no mutation occurred;
- generate fresh batch or packet if stale;
- rollback/contain if mutation occurred and scope is exact.

Terminal behavior:

```text
forward_allowed=false
```

## EXPIRED

Entry conditions:

- `now > expires_at`;
- packet expired;
- batch stale beyond allowed window.

Operator actions:

- generate fresh batch or fresh packet;
- rerun precheck and approval;
- do not execute stale batch.

Terminal behavior:

```text
forward_allowed=false
```

Rollback containment remains possible only if exact scope is known.

## CANCELLED

Entry conditions:

- operator cancellation before forward execution;
- scheduler cancellation before execution;
- policy cancellation before execution.

Operator actions:

- create new batch if work remains needed;
- preserve cancellation audit.

Terminal behavior:

```text
forward_allowed=false
resume_allowed=false
```

## REPLAY_DENIED

Entry conditions:

- packet already consumed;
- replay attempt detected;
- batch generation reused after terminal event.

Operator actions:

- inspect replay denial;
- verify no movement;
- verify no routing mutation;
- preserve audit.

Terminal behavior:

```text
forward_allowed=false
movement_during_replay=false
routing_mutation_during_replay=false
```

## Recovery Paths

Recovery never resumes a terminal batch directly.

Allowed recovery:

```text
new_batch_generation
new_approval_packet
fresh_execution_time_recheck
```

For containment:

```text
new_CONTAINMENT_BATCH_or_ROLLBACK_BATCH
```

## Failure Verdict

Failure flow is defined and fail-closed.

