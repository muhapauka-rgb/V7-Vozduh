# E33.B Governance Compatibility Review

governance_compatible=true

## Capacity Program

Routing Intelligence may read capacity status, target quality, and effective capacity. It cannot certify capacity, modify capacity class, reserve capacity, or override effective_batch_cap.

## Execution Batches

Executable Routing Intelligence proposals must become proposed execution batches. RI does not execute batches and cannot consume approval packets.

## Policy Engine

Policy remains admission logic. RI may provide service evidence and proposal rationale, but policy may deny, require review, or require additional gates.

## Concurrency Controls

RI cannot acquire locks, transfer owners, or reserve targets. Any proposal must later pass user, target, batch, packet, audit, and reservation checks.

## Scheduling

RI may recommend urgency and timing evidence. Scheduler owns ordering, timing, and dispatch eligibility.

## Execution-Time Recheck

RI cannot bypass execution-time recheck. Live runtime truth must be verified again before any movement.

## Required Services Preservation

required_services influence is preserved across the governance path:

```text
required_services -> user_specific_health -> proposal evidence -> batch metadata -> policy review -> execution-time recheck
```

If required_services are missing, stale, or unknown, RI output must be OBSERVE or REVIEW_REQUIRED, not high-confidence movement.

governance_compatible=true
required_services_influence_preserved=true
