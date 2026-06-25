# ADR-V7 Delegated Autonomy Policy

Status: Accepted
Date: 2026-06-26

## Context

V7's product direction is autonomous operational routing.

Packet approval does not scale because packets are fresh runtime artifacts and can become stale before an operator reviews them.

Action-Class Authority fixes the durable capability boundary, but approving every action class forever still leaves the operator inside routine operations.

The product needs a bounded policy model:

- operator approves policy boundaries;
- V7 makes operational decisions inside those boundaries;
- V7 stops safely outside those boundaries.

Existing V7 owners already cover the required semantics:

- Product Specification owns product meaning;
- OMP owns autonomy progression and authority evaluation;
- Runtime Model owns execution semantics;
- Action-Class Runtime Enablement Read Model owns read-only action-class capability views;
- packet, restore, rollback, verification, feedback, learning, truth, and convergence owners already exist.

Need New Owner remains `FALSE`.

## Decision

V7 adopts Delegated Autonomy Policy as the target approval-boundary model.

The operator approves a bounded Autonomy Policy once.
Inside that approved policy, V7 may self-approve operational routing decisions.
Outside that policy, V7 stops safely.

The policy must define:

- allowed action classes;
- max users per action;
- allowed failure types;
- required freshness;
- required verification;
- required rollback or certified no-rollback path;
- required anti-flap state;
- required suitability, trust, confidence, and prediction floors;
- max blast radius;
- cooldown;
- stop conditions;
- automatic downgrade rules;
- required reporting after action.

Runtime may execute automatically only if:

1. action belongs to an approved policy;
2. action class is certified or policy explicitly allows governed learning mode;
3. fresh packet is generated immediately before execution;
4. packet matches policy;
5. rollback is ready;
6. verification is ready;
7. anti-flap passes;
8. blast radius is within policy;
9. evidence is not stale;
10. failure mode is known.

V7 may not approve expansion of policy, new action classes, increased blast radius, lowered gates, or authority expansion.
V7 may recommend expansion, but cannot grant it.

## Consequences

- Product Specification explains Delegated Autonomy Policy as the target approval model.
- OMP owns policy progression and must stop at `AUTHORITY_BOUNDARY` before policy expansion.
- Runtime Model requires delegated policy eligibility before automatic execution.
- Action-Class Runtime Enablement exposes read-only policy preview and runtime eligibility through existing owners.
- Current default policy is `dap_default_tier1_readonly`, state `NOT_APPROVED`, current mode `CLASS_APPROVAL`, target mode `DELEGATED_AUTONOMY`, max users per action `1`.
- Runtime automation remains disabled.

## Forbidden

This ADR does not authorize:

- runtime apply;
- user movement;
- restore-barrier writes;
- rollback apply;
- daemon or timer enablement;
- packet approval;
- action-class approval;
- policy approval;
- authority expansion;
- planner redesign;
- governance redesign;
- execution redesign;
- truth-source creation;
- synthetic evidence;
- floor lowering;
- new owner creation.

## Affected Modules

- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tests/unit/test_autonomy_trust_acceleration.py`

## Verification

- tests
- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

No runtime mutation, no apply, no user movement, no restore-barrier write, and no authority expansion.
