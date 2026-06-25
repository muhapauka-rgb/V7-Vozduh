# ADR-V7 Action-Class Authority

Status: Accepted

## Context

V7 originally used exact packet approval as the governed authority boundary for early one-user canary execution.

That was useful for proof because it bounded subject, target, selected move hash, rollback, restore barrier, verification, and outcome closure.

Project history now shows that packet approval does not scale as the primary product abstraction:

- packets are snapshots of a fast-changing runtime reality;
- approved packets can become stale before execution;
- fresh dry-runs can produce different users, targets, operation ids, selected move hashes, and rollback manifests;
- repeated packet approval creates operator work without increasing durable product maturity;
- a product targeting `100+` channels and `10000+` users cannot depend on approving individual short-lived packets.

Existing V7 owners already cover the needed model:

- OMP owns the Autonomy Promotion Engine and authority evaluation;
- Current Program State holds volatile packet/current-stop state;
- Runtime Model owns execution semantics;
- `admin_core/autonomy_trust_acceleration.py::build_action_class_runtime_enablement_model` exposes read-only action-class runtime enablement;
- `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only` exposes the same path through an existing CLI;
- `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle` maps packets to action classes and stops at authority;
- `tools/v7-operator-execution-packet` and `admin_core/operator_execution.py` remain the packet/restore/rollback owners.

Need New Owner remains `FALSE`.

## Decision

Action-Class Authority becomes the primary V7 approval model.

The operator approves durable product capabilities:

```text
Action Class
  -> Authority Expansion
  -> Product Policy
  -> New Classes
  -> Exceptional Situations
```

Packets are runtime execution artifacts.
They are fresh, bounded, validated, and ephemeral.

Runtime must generate or consume a fresh packet immediately before execution and verify that it belongs to an already approved Action Class.

Packet-level approval remains only as a temporary `GOVERNED_ONLY` fallback until the relevant action class is certified and explicitly approved for class authority or runtime capability.

Promotion must end with Runtime capability, not packet approval.

## Consequences

- Product Specification treats Action Class as the durable approval object.
- OMP must ask after every certified action class whether packet-level approval can be retired for that class.
- Runtime semantics require fresh packet validation against approved class authority, policy, freshness, safety, rollback/no-rollback, verification, learning, and blast-radius bounds.
- Packet staleness is treated as evidence that packet approval is not scalable, not as a reason to weaken safety.
- No runtime automation is enabled by this ADR.
- No packet is approved by this ADR.
- No authority is expanded by this ADR.
- No user movement, restore-barrier write, apply, daemon, timer, event consumer, planner, governance, execution path, truth source, floor change, or synthetic evidence is introduced.

## Alternatives Considered

1. Keep packet approval as the primary model.
   - Rejected. It repeatedly binds human authority to volatile runtime snapshots and does not scale to high channel/user counts.

2. Extend packet leases until operators can approve in time.
   - Rejected as the product model. Leases can protect governed proof execution, but they do not create durable authority or reduce repetitive operator work.

3. Create a new authority engine.
   - Rejected. OMP, Runtime Model, Current Program State, action-class read models, packet owner, restore/rollback owner, feedback, learning, truth, and convergence already provide sufficient semantic coverage.

4. Enable runtime automation now.
   - Rejected. This ADR changes product authority semantics only. Runtime automation still requires evidence, certification, explicit authority, and existing-owner implementation.

## Affected Modules

- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- Existing read-only action-class runtime enablement owners
- Existing packet/restore/rollback owners

## Reference Updates

- Canonical Reference records Action-Class Authority as the primary approval model.
- SYSTEM_MAP maps Product Specification, OMP, Runtime Model, and Action-Class Runtime Enablement to the updated authority semantics.

## Verification

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

