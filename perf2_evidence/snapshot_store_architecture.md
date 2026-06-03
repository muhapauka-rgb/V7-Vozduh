# PERF.2 Snapshot Store Architecture

## Canonical Location

`/opt/v7/egress/state/intelligence/`

## Ownership

Brain-side producers write snapshots.

Runtime and Admin read snapshots.

No runtime writes are allowed.

## Lifecycle

1. Heavy Brain worker computes outside runtime.
2. Worker writes a complete snapshot envelope atomically.
3. Runtime reads bounded JSON.
4. Runtime validates schema, freshness, confidence, source hashes, and item count.
5. Runtime consumes compact items only.
6. Raw history remains outside snapshot store.

## Retention

- runtime-required snapshots: latest plus short archive
- admin-only snapshots: latest plus shorter archive
- raw audit/history/probe logs: outside snapshot store
- rotation: producer-owned, bounded by file count and age

## Implemented Contract Module

`admin_core/intelligence_snapshots.py`

The module is read-only from runtime perspective:

- reads snapshot files
- validates envelope schema
- evaluates freshness
- evaluates confidence
- returns runtime behavior
- does not integrate with planner
- does not execute commands
- does not write runtime state
