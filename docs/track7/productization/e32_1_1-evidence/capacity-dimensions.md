# E32.1.1 Capacity Dimensions

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_dimensions_defined=true

## Definition

A capacity class is a governance certification level for a target. It states the largest bounded batch size that the target may accept in a governed movement packet without exceeding the proven blast radius, quality, rollback, audit, and runtime-safety envelope.

A capacity class is not only a throughput number. It is a combined safety state made from technical performance, governance behavior, and evidence freshness.

## Required Dimensions

### User Count

Meaning: maximum approved users in one bounded movement packet.

Use:

- Defines blast radius.
- Must be less than or equal to target hard limit.
- Must match the certified class ceiling.

### Throughput

Meaning: measured target-local and long-window throughput under class-appropriate pressure.

Use:

- Validates that class promotion is not only metadata.
- Supports confidence that target can carry the batch.

### Minimum Mbps

Meaning: lowest accepted measured throughput sample during validation.

Use:

- Prevents promotion on high average with unsafe troughs.
- Existing floor inherited from E25-E31: min Mbps must remain at or above the movement readiness floor.

### Stability

Meaning: quality consistency across the validation window.

Use:

- Blocks promotion when target oscillates.
- Requires no hidden quality degradation and no readiness oscillation during the validation window.

### Readiness Status

Meaning: target readiness helper verdict for the target and class context.

Use:

- Must be GO before packet generation.
- Must be GO during execution-time recheck.
- Must fail closed if target becomes NO-GO.

### Target Users Count

Meaning: current number of users assigned to the target.

Use:

- For execution-only targets, pre-forward target users must match the packet assumption.
- Capacity class does not allow accidental occupancy outside approved packets.

### Runtime Checker Health

Meaning: runtime platform checkers must remain OK.

Use:

- Confirms NAT/MSS, provisioning reconcile, kill-switch expectations, registry consistency, and related platform assumptions.
- Any checker failure blocks promotion and execution.

### Restore-Settle State

Meaning: restore-settle gate must be GO before approval and after rollback.

Use:

- Confirms selected moves are zero.
- Confirms hidden movers are absent.
- Confirms runtime is quiet enough for bounded movement.

### Validation Age

Meaning: freshness of capacity evidence.

Use:

- Prevents relying on stale long-window proofs after runtime drift, target degradation, metadata change, or operator changes.
- Stale class evidence degrades to candidate or conditional status until revalidated.

### Confidence Level

Meaning: confidence assigned from evidence quality.

Suggested levels:

- LOW: static/model-only evidence, no movement proof.
- MEDIUM: target-local pressure validation and long-window readiness, but no class-sized governed movement.
- HIGH: class-sized governed movement, rollback, delayed monitoring, replay denial, and clean restore-settle all completed.

## Class Qualification Rule

A target qualifies for a certified class only when all required dimensions are true:

- class-sized or higher target-local validation passes;
- long-window validation passes;
- class-sized governed movement proof exists;
- rollback proof exists for the same class size;
- replay denial proof exists;
- delayed monitoring shows no unapproved movement;
- restore-settle returns GO;
- runtime checkers remain OK;
- evidence is fresh enough for the configured policy.

If any dimension is missing, the class may be `CANDIDATE` but not `CERTIFIED`.

