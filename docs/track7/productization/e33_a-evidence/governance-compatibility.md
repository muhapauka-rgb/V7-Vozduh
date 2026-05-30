# E33.A Governance Compatibility Review

governance_compatible=true

## Capacity Program Compatibility

Routing Intelligence may read capacity status and target quality, but cannot certify capacity or override effective_batch_cap.

## Execution Batches Compatibility

Routing Intelligence proposals must become proposed batches before any execution path can exist.

## Policy Engine Compatibility

Routing Intelligence cannot bypass policy. Policy may deny, require review, or require additional gates for any proposal.

## Concurrency Controls Compatibility

Routing Intelligence cannot reserve, lock, or bypass conflict checks. Any proposal must later pass concurrency validation.

## Scheduling Compatibility

Routing Intelligence cannot dispatch. It may recommend timing inputs, but scheduler remains the time-ordering layer.

## Execution-Time Recheck Compatibility

Routing Intelligence cannot bypass execution-time recheck. All proposal-derived movements must be rechecked against live runtime truth.

## Decision

governance_compatible=true
