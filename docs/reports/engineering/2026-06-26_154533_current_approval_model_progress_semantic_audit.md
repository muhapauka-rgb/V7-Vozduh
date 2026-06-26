# Engineering Report: Current Approval Model Progress Semantic Audit

## Summary

V7 already contains the approval-model transition concept, but it does not expose a single dedicated `Approval Model Progress` percentage.

Verdict: `EXTEND_EXISTING`.

Need New Owner: `FALSE`.

Need New Document: `FALSE`.

## Action Performed

Performed a semantic reuse audit across:

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`
- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/reference/SYSTEM_MAP.md`

The audit searched for behavior equivalent to Current Approval Model, Approval Progress, Packet Approval Retirement, Action-Class Promotion Progress, Delegated Autonomy Progress, Runtime Authority Progress, Approval Transition, Authority Transition, Packet Approval Phase, Class Authority Phase, and Capability Promotion.

## Objective Observations

| Candidate | Owner | Purpose | Current implementation | Maturity | Overlap |
| --- | --- | --- | --- | --- | --- |
| Autonomy Promotion Engine | OMP | Defines how action classes move from governed proof to class approval, bounded autonomy, and autonomous runtime. | Action-class states exist: `NOT_CERTIFIED`, `GOVERNED_ONLY`, `CERTIFIED_FOR_CLASS_APPROVAL`, `CERTIFIED_FOR_BOUNDED_AUTONOMY`, `AUTONOMOUS_RUNTIME`. First class is `GOVERNED_ONLY`; target is `CERTIFIED_FOR_CLASS_APPROVAL`. | `ACTIVE_CANONICAL`; runtime automation disabled. | `HIGH`: directly tracks approval transition semantics. |
| Delegated Autonomy Policy Model | OMP, Runtime Model, Product Specification | Defines target approval model where operator approves bounded policy and Runtime acts inside it. | Current policy `dap_default_tier1_readonly`; policy state `NOT_APPROVED`; current mode `CLASS_APPROVAL`; target mode `DELEGATED_AUTONOMY`; runtime apply `NO`. | `ACCEPTED_CANONICAL`; read-only surfaces exist. | `HIGH`: defines target approval model and mode transition. |
| Authority Evolution capability | OMP Capability Management | Tracks broad movement from packet approval to bounded class/policy authority. | Current percent `40.0%`; blocking backlog items `A3`, `A4`, `A5`, `A6`, `B11`, `B12`, `B13`, `B16`, `B21`, `C3`, `C4`. | `IN_PROGRESS`. | `MEDIUM_HIGH`: closest existing percentage, but broader than Approval Model Progress. |
| Production Maturity Authority category | Production Maturity Model | Weights authority evolution inside production readiness. | `Authority Evolution` category current value `15 / 100`, weight `10`; delegated autonomy policy not approved and authority expansion not granted. | `IN_PROGRESS`. | `MEDIUM`: tracks production authority maturity, not approval-model transition specifically. |
| Current Program State | Current Program State | Stores volatile current authority and progress state. | Stores `authority_class`, `authority_reason`, `required_action`, `autonomy_progress`, `certification_progress`, `current_state`, active capability, and current packet stop. | `ACTIVE_VOLATILE`. | `MEDIUM`: knows current operational approval boundary but not a normalized approval-progress field. |
| Runtime Model | Runtime Model | Defines how Runtime treats packet approval, class authority, delegated policy, and runtime capability. | Runtime must not ask for packet approval when class is `AUTONOMOUS_RUNTIME`; fresh packet must match approved class and policy. | `CANONICAL_DESIGN`; implementation partial/read-only. | `HIGH`: defines execution semantics for the endpoint of approval progress. |
| Product Specification | Product Specification | Defines product-level approval evolution. | Product says packet approval is temporary, Action-Class Authority is durable, Delegated Autonomy Policy is target, and Runtime capability is the endpoint. | `CANONICAL`. | `HIGH`: owns product meaning. |
| SYSTEM_MAP | SYSTEM_MAP | Maps ownership. | OMP owns Autonomy Promotion Engine, Action-Class Authority evolution, Delegated Autonomy Policy progression, action-class states, and packet-approval retirement evaluation. | `CANONICAL`. | `HIGH`: confirms OMP ownership. |

## Engineering Conclusions

1. OMP already knows the current approval model.
   - Current first certifiable action class: `single-user governed candidate failover`.
   - Current action-class state: `GOVERNED_ONLY`.
   - Current policy state: `NOT_APPROVED`.
   - Current mode: `CLASS_APPROVAL`.
   - Runtime automation: `NO`.

2. OMP already knows the target approval model.
   - Target mode: `DELEGATED_AUTONOMY`.
   - Promotion endpoint: `Runtime capability`, not packet approval.
   - Final target: `PRODUCTION_AUTONOMY`, where operator supervises and Runtime performs routine certified work inside policy.

3. OMP already tracks the transition semantically:

```text
Packet Approval
  -> Action-Class Authority
  -> Delegated Autonomy Policy
  -> Runtime Capability
```

4. A current percentage is partially available, but not as a dedicated approval-model metric.
   - `Authority Evolution = 40.0%` in OMP capability management.
   - `Authority Evolution = 15 / 100` in Production Maturity Model.
   - `Production Autonomy = 0.0%`.
   - `autonomy_progress = TIER_1_GOVERNED`.

5. These numbers are adjacent but not equivalent to a normalized `Approval Model Progress` score.

## Impact

No implementation changed. No Runtime changed. No OMP changed.

If future work requires a visible approval-model progress indicator, the correct extension point is existing OMP ownership:

- section `2.1.4. Autonomy Promotion Engine`;
- section `2.1.5. Delegated Autonomy Policy Model`;
- Capability Management row `Authority Evolution`;
- Current Program State progress fields.

## Recommended Extension Fields

If approved later, extend existing owners with:

- `current_approval_model`
- `target_approval_model`
- `approval_model_stage`
- `approval_model_progress_percent`
- `packet_approval_retirement_status`
- `action_class_authority_progress`
- `delegated_autonomy_policy_progress`
- `runtime_capability_progress`
- `approval_model_blockers`
- `approval_model_next_evidence`

Current implementation gap:

V7 has the model and owners, but lacks one unified progress field that summarizes the approval transition.

## Capability Progress

No capability progress changed.

## Backlog Progress

No backlog item changed.

## Production Maturity

No production maturity changed.

## Canonical Knowledge

Canonical Reference was updated to record that Approval Model Progress is not a new owner. If needed, it must be calculated inside existing OMP and Current Program State ownership.

## Evidence

Key evidence:

- OMP section `2.1.4. Autonomy Promotion Engine` defines action-class states and packet approval retirement.
- OMP section `2.1.5. Delegated Autonomy Policy Model` defines current mode `CLASS_APPROVAL` and target mode `DELEGATED_AUTONOMY`.
- OMP Capability Management tracks `Authority Evolution` at `40.0%`.
- Production Maturity Model tracks `Authority Evolution` at `15 / 100`.
- Runtime Model defines the endpoint where Runtime stops asking for packet approval after class/policy authority is approved.
- Product Specification states packet approval is temporary and delegated autonomy is the long-term model.
- SYSTEM_MAP assigns OMP ownership for Autonomy Promotion Engine, Action-Class Authority evolution, Delegated Autonomy Policy progression, action-class states, and packet-approval retirement evaluation.

## Next Step

Do not create a new approval-progress owner or document. If the operator wants a displayed metric, extend OMP and Current Program State with the recommended fields.

## Re-audit Rule

Do not re-audit Current Approval Model Progress unless OMP authority semantics, Product Specification approval model, Runtime Model class/policy authority semantics, or Production Maturity scoring materially change.
