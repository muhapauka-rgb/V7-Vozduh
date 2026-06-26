# ADR-V7 Canonical Policy Library

Status: Accepted
Date: 2026-06-26

## Context

V7 is moving from governed operations toward delegated and production autonomy.

Operational behavior must not be invented from personal opinion or one-off prompts.
It must be based on proven world knowledge, compared against V7 reality, adapted through existing owners, verified, certified, and integrated into OMP.

Existing V7 owners already cover methodology and execution boundaries:

- Product Specification owns product meaning;
- Research Framework owns mature-system research methodology;
- OMP owns implementation and production maturity;
- Canonical Reference owns current truth;
- SYSTEM_MAP owns owner topology;
- Runtime Model owns execution semantics;
- existing runtime, packet, rollback, verification, learning, truth, and convergence owners remain unchanged.

Need New Owner remains `FALSE`.

## Decision

Create `docs/policies/` as the Canonical Policy Library.

The library is the permanent documentation source for V7 operational behavior policy.

Before any policy becomes operational, it must follow:

```text
DISCOVER
  -> FULL WORLD RESEARCH
  -> INDUSTRY CONSENSUS DETECTION
  -> INDUSTRY DISAGREEMENT DETECTION
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> REUSE EXISTING V7 OWNERS
  -> CANONICAL POLICY
  -> IMPLEMENTATION
  -> VERIFICATION
  -> CERTIFICATION
  -> OMP INTEGRATION
```

Operational implementation before certification is forbidden.
The `IMPLEMENTATION` lifecycle step may prepare code or documentation only after a canonical policy exists; runtime enablement waits for `CERTIFICATION` and OMP integration.

V7 may innovate only after proving that no stable world consensus exists or that world consensus does not fit V7 architecture.

## Consequences

- OMP must check the Canonical Policy Library before implementing or changing operational behavior.
- If a policy exists, OMP reuses it.
- If a policy is partial, OMP extends it through the full methodology.
- If no policy exists, OMP runs the full world research methodology before implementation.
- First policy research target is `POLICY_001_HARD_FAILURE`.
- The first nine policy shells are created without invented policy content.

## Forbidden

This ADR does not authorize:

- runtime apply;
- user movement;
- restore-barrier writes;
- rollback apply;
- daemon or timer enablement;
- authority expansion;
- planner redesign;
- governance redesign;
- execution redesign;
- truth-source creation;
- synthetic evidence;
- floor lowering;
- invented policy content before research.

## Affected Modules

- `docs/policies/`
- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Verification

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

No runtime mutation, no apply, no user movement, and no authority expansion.
