# Action Class Ownership Proof

Status: `COMPLETE`
Mode: `FINAL_ARCHITECTURE_INVESTIGATION`
Code modified: `NO`
Runtime modified: `NO`
Planner modified: `NO`
OMP modified: `NO`
Architecture changed: `NO`

## Summary

The single canonical owner of Action Class is:

```text
OMP Autonomy Promotion Engine / Action-Class Authority
```

The Planner owns candidate selection and movement recommendation.
The Decision Model owns action vocabulary.
Policy owners define action-class conditions and boundaries.
Authority owners approve/deny execution authority for a class.
Runtime consumes an approved/certified action class and executes or stops.

None of those subsystems owns the durable Action Class object.

## Action Class Inventory

| Action / class term | Meaning | Canonical owner | Consumer | Legal effect |
| --- | --- | --- | --- | --- |
| `KEEP` | Current assignment acceptable; no movement. | Decision Model vocabulary | Planner, UI, Runtime | Non-mutating decision. |
| `MOVE` | Move users to a better eligible channel under governance. | Decision Model vocabulary; OMP owns class promotion if it becomes durable class. | Planner, Runtime | Candidate only until authority/readiness pass. |
| `FAILOVER` | Move affected users away from failing channel. | Decision Model vocabulary; OMP owns class state. | Planner, L3, Runtime, Authority | Candidate class input, not execution authority alone. |
| `DRAIN` | Stop new assignments and gradually move users away if safe. | Decision Model vocabulary; OMP owns future class state. | Planner, policy, Runtime | Requires separate class/policy authority. |
| `QUARANTINE` | Remove channel from assignment/retention until recovery admission passes. | Decision Model vocabulary; policy/OMP class owner for durable behavior. | Planner, Runtime, UI | Non-executable or executable only if certified. |
| `RECOVER` | Re-admit channel after sufficient recovery evidence. | Decision Model vocabulary; OMP class owner for promotion. | Recovery policy, Runtime | Requires recovery admission certification. |
| `PROBE_ONLY` | Collect fresh evidence; no movement. | Decision Model vocabulary | Observation/evidence owners | Read-only action. |
| `ASK_OPERATOR` | Human decision required. | Decision Model vocabulary / OMP stop rules | OMP/operator | Authority boundary, no mutation by itself. |
| `NO_ACTION` | No useful or safe action exists now. | Decision Model vocabulary | Runtime/UI | Sleep/report/no mutation. |
| `WAIT` / waiting states | Wait for evidence, authority, previous level, or safe condition. | Runtime/OMP state vocabulary depending on context | Runtime/OMP/UI | No mutation. |
| `single-user governed candidate failover` | First certifiable Action Class. | OMP Autonomy Promotion Engine | Runtime/Authority/Execution | Current state `GOVERNED_ONLY`. |
| `two-user failover` | Larger failover class. | OMP Autonomy Promotion Engine | Runtime/Authority | Not certified. |
| `small batch movement` | Future batch class. | OMP Autonomy Promotion Engine | Runtime/Authority | Not certified. |
| `channel hard-fail failover` | Emergency failover due to hard channel failure. | OMP Autonomy Promotion Engine + L3 capability contract | Runtime/Authority | Governed/certification path only. |
| `channel degradation` | Degraded-channel movement. | OMP Autonomy Promotion Engine | Runtime/Authority | Future L4/class path. |
| `recovery admission` | Re-admit recovered channel gradually. | OMP Autonomy Promotion Engine / Policy 003 | Runtime/Authority | Requires recovery certification. |
| `service failover` | Move affected users for service-specific failure. | OMP Autonomy Promotion Engine / policy/service owners | Runtime/Authority | Requires class evidence and authority. |
| `rollback` | Reverse/compensate unsafe execution. | OMP class state + Policy 007 + rollback owners | Runtime/Execution | Requires rollback authority/certification. |
| `verification` | Prove action result. | OMP class state + verification owners | Runtime/Learning | Required before trust/promotion. |
| `outcome closure` | Record terminal outcome. | OMP/Feedback owners | Learning/Production Maturity | Feeds maturity, not execution by itself. |
| `learning refresh` | Update knowledge from verified outcomes. | OMP/Learning owners | OMP/Planner | Non-mutating maturity input. |
| `L3_EMERGENCY_AUTONOMOUS_FAILOVER` | Capability specification for emergency failover. | OMP / Autonomous Execution Program / Autonomous Runtime Model composition; OMP owns class state. | L3 implementation, Runtime, Authority | Implementation contract, not standalone authority. |

## Ownership Graph

```text
Product Specification
  defines Action Class as durable approval object
  ↓
OMP Autonomy Promotion Engine
  owns Action Class states, promotion, certification, and packet-approval retirement
  ↓
Policy owners
  define class conditions and boundaries
  ↓
Decision Model
  owns vocabulary used to express decisions
  ↓
Planner
  selects candidate and explains reason
  ↓
Authority
  approves/denies execution authority for the class/scope
  ↓
Runtime
  consumes class + authority + readiness and executes or STOP_SAFE
```

## Lifecycle

```text
World Fact
  -> Observation
  -> Classification
  -> Planning
  -> Authority
  -> Execution
  -> Verification
  -> Learning
```

| Stage | Can create Action Class? | Can modify Action Class? | Can reject Action Class? | Can consume Action Class? |
| --- | --- | --- | --- | --- |
| Product Specification | Defines product meaning of Action Class. | Only via explicit product/canonical change. | Can reject product-incompatible class concepts. | N/A |
| OMP Autonomy Promotion Engine | `YES`: owns canonical class states and promotion path. | `YES`: promotes/downgrades state through evidence and authority. | `YES`: keeps class `NOT_CERTIFIED`/`GOVERNED_ONLY` or blocks promotion. | `YES` |
| Policy owners | `NO`: define conditions/bounds for classes. | `NO`: may change policy only through policy lifecycle. | `YES`: reject class applicability when policy not satisfied. | `YES` |
| Decision Model | `NO`: owns vocabulary, not durable class state. | `NO` | `YES`: can classify unknown action vocabulary as invalid. | `YES` |
| Observation | `NO`: produces facts. | `NO` | `YES`: missing/contradictory observation prevents class applicability. | `YES` |
| Planner | `NO`: selects candidates inside known vocabulary/classes. | `NO` | `YES`: can return no candidate/blocker. | `YES` |
| Authority | `NO`: approves or denies class/scope authority. | `NO`: expansion requires OMP/operator/policy. | `YES`: denies authority. | `YES` |
| Runtime | `NO`: must not invent or promote action classes. | `NO` | `YES`: `STOP_SAFE` if class not certified/authorized/ready. | `YES` |
| Execution | `NO`: applies selected action only. | `NO` | `YES`: fail closed on mismatch. | `YES` |
| Verification/Learning | `NO`: produce evidence for OMP. | `NO` | `YES`: failed evidence blocks promotion. | `YES` |

## Where Action Class Is Born

Action Class is born canonically in OMP, not in Planner.

Evidence:

- Product Specification states the durable approval object is an Action Class.
- OMP states the durable authority object is the Action Class.
- OMP owns the Autonomy Promotion Engine.
- SYSTEM_MAP states OMP owns Action-Class Authority evolution, action-class states, and Autonomy Promotion Engine.
- Runtime Model states Runtime executes certified action classes only when OMP and authority policy have promoted that class.
- Decision Model owns vocabulary, but says it creates no governance layer, execution path, truth source, runtime behavior, apply behavior, or user movement authority.

Therefore:

```text
Action Class birth = OMP class registry / promotion state.
Planner output = candidate decision using vocabulary.
```

## Replay Of Current Production Candidate

Current implementation path:

```text
tools/v7-users-autoswitch::_decision_for_user()
  sees current channel not eligible
  sets action = switch
  sets move_type = failover
  adds reason = current_egress_not_eligible
```

This component is the Planner/Autoswitch owner.

It is legally allowed to produce a candidate recommendation.
It is not legally allowed to create or certify the Action Class `L3 Emergency Failover`.

The first divergence is:

```text
Planner move_type=failover
  treated as if it establishes L3 action-class classification
```

Canonical requirement:

```text
OMP-owned Action Class + policy facts + L3 entry truth
  -> class applicability
Planner
  -> selected candidate inside that class
```

## Counterfactuals

| Removed subsystem | Who can still create Action Class? | Result |
| --- | --- | --- |
| Planner removed | OMP can still define/certify Action Class; no candidate execution can be selected. | Planner is not indispensable Action Class owner. |
| Runtime removed | OMP can still define/certify Action Class; no execution occurs. | Runtime is not owner. |
| Authority removed | OMP can still define/certify class; execution authority cannot pass. | Authority is not owner. |
| Execution removed | OMP can still define/certify class; no mutation occurs. | Execution is not owner. |
| Decision Model removed | OMP still owns class state but loses canonical vocabulary interface. | Decision Model is semantic vocabulary owner, not durable class owner. |
| OMP removed | No canonical action-class state, certification, promotion, approval retirement, or class authority evolution remains. | OMP is indispensable. |

## Uniqueness

Action Class has one canonical owner:

```text
OMP Autonomy Promotion Engine / Action-Class Authority
```

Other owners produce required inputs:

- Product Specification defines product intent.
- Decision Model defines action vocabulary.
- Policies define eligibility/boundaries.
- Planner selects candidates.
- Authority approves/denies allowed class/scope.
- Runtime consumes and executes/stops.

These are not competing Action Class owners.

## Falsification

### Attempt 1: Planner is owner

Rejected.

Planner owns candidate ranking, blockers, selected moves, and explanations. L3 explicitly says Planner selects candidate and Runtime executes or stops. OMP certifies capability. Planner cannot approve class state, promote class, retire packet approval, or expand authority.

### Attempt 2: Runtime is owner

Rejected.

Runtime Model states Runtime executes certified action classes only when OMP and authority policy have promoted that class. Runtime must not invent decisions or promote classes.

### Attempt 3: Authority is owner

Rejected.

Policy 004 and OMP separate authority from operational safety and promotion. Authority approves/denies scope; it does not create class semantics or class evidence.

### Attempt 4: Observation is owner

Rejected.

Observation produces world facts. It may prove current channel failure or service failure, but facts alone do not define a durable Action Class.

### Attempt 5: Separate classifier owner exists

Rejected.

Autonomous Runtime Model lists Classify owner as OMP / Policy owners / Decision Model. SYSTEM_MAP maps Action-Class Authority to OMP / Policy 005. No separate classifier owner is canonical.

### Attempt 6: Shared ownership is canonical

Rejected for the durable Action Class object.

There is shared input responsibility, but not shared ownership. The canonical durable state and promotion authority are OMP-owned.

## Formal Ownership Proof

Proof result:

```text
OMP is the canonical owner.
```

Mapped to provided proof choices:

```text
F. Shared ownership is canonical
```

only for the classification pipeline inputs.

But the asked object is the Action Class itself. For that object, the single canonical owner is:

```text
OMP Autonomy Promotion Engine / Action-Class Authority
```

## Root Cause

Current owner in implementation:

```text
Planner / Autoswitch currently emits move_type=failover from current_egress_not_eligible.
```

Canonical owner:

```text
OMP Autonomy Promotion Engine / Action-Class Authority.
```

First divergence:

```text
Planner candidate vocabulary is being used as if it were OMP-owned Action Class classification.
```

## Stop Condition

Ownership is uniquely proven.

No further architecture investigation is required for Action Class ownership.

Next work must be implementation debugging/correction inside existing owners only.

Final verdict:

```text
ACTION_CLASS_OWNER_PROVEN
```
