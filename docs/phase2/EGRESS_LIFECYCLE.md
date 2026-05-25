# V7 Phase 2 - Egress Lifecycle

## Purpose

Every egress must move through a deterministic lifecycle before it can affect production routing.

Phase 2 lifecycle governance does not rewrite the existing provisioning code. It formalizes the states already visible in draft metadata, registry rows, runtime tests, quarantine checks, and guarded enable flows.

## Lifecycle States

### imported

Raw source was received.

Accepted sources:

- config file;
- subscription;
- URI;
- QR payload;
- outbound fragment;
- provider bundle.

Production impact: none.

### parsed

The source was recognized enough to identify protocol/runtime mode or to ask the operator for endpoint selection.

Production impact: none.

### validated

Required fields and static safety constraints passed.

Examples:

- WireGuard/AmneziaWG keys and endpoint are parseable;
- OpenVPN scripts/hooks are blocked;
- proxy outbound can be normalized;
- container/subscription config is not treated as one runnable egress.

Production impact: none.

### draft

Root-only draft metadata and input config exist under the draft directory.

Production impact: none.

### preflight_passed

No-runtime-start checks passed:

- required tools present;
- unsafe hooks absent;
- runtime adapter known;
- active registry does not already contain this draft id.

Production impact: none.

### runtime_tested

An isolated temporary runtime test was attempted.

Production impact: none.

Rules:

- temporary interface/proxy only;
- no user moves;
- no route-class eligibility;
- cleanup verified.

### quarantined

The egress is isolated from production routing until service and datapath checks prove safe.

Production impact: none.

Quarantine can be `PASS`, `BLOCKED`, or stale.

### staged

The egress can be added to the pool only as disabled.

Production impact:

- `egress.registry` may gain a row with `enabled=0`;
- users are not moved;
- routes are not changed;
- autoswitch must not use it.

### enabled

The egress is explicitly enabled after readiness gates.

Production impact:

- egress becomes eligible for future bounded routing decisions;
- enable alone must not migrate users.

### degraded

The egress is enabled or known but health indicates reduced reliability.

Production impact:

- autoswitch should be cautious;
- operator sees impact summary;
- no panic migration.

### maintenance

Operator intentionally removes egress from normal use.

Production impact:

- no new assignments;
- existing users require drain/migration planning;
- rollback context required.

### disabled

Egress is not production eligible.

Production impact:

- no autoswitch participation;
- no route-class eligibility.

### failed

Provisioning/runtime/quarantine verification failed.

Production impact: none unless an existing egress update was attempted and rolled back.

### rollback_candidate

An action has changed files/runtime and has backup context available.

Production impact:

- operator must see rollback availability and verification result.

### deleted

Draft was archived or egress was removed through an explicit safe flow.

Production impact:

- deleting pooled/enabled egress must be blocked until runtime and registry cleanup are safe.

## State Mapping To Current Runtime

Current code already exposes many state markers:

- draft metadata `validation`;
- `last_preflight_status`;
- `last_runtime_status`;
- `last_quarantine_status`;
- `pool_action`;
- `runtime_profile_status`;
- `next_step`;
- `egress.registry enabled`;
- `egress-flags.state`;
- runtime readiness checks.

## Production Eligibility Rule

An egress is production-eligible only when all are true:

- exists in `egress.registry`;
- `enabled=1`;
- runtime profile exists;
- readiness has no blocker;
- quarantine passed or equivalent evidence exists;
- kill switch compatibility is verified;
- route class policy allows it;
- health state is not blocked/quarantined/maintenance.

## Forbidden Transitions

- imported -> enabled
- draft -> enabled
- runtime_tested -> enabled without quarantine
- quarantined blocked -> enabled
- failed -> enabled
- disabled/maintenance -> user migration without dry-run and guard

## Phase 2 Boundary

This lifecycle model does not change current provisioning behavior. It defines the required semantics for future implementation and validation.
