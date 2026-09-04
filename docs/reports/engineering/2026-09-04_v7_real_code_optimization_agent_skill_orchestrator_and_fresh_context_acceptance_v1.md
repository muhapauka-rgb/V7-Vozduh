# V7 Real Code Optimization Agent Skill, Orchestrator and Fresh-Context Acceptance V1

- Mission: `V7_REAL_CODE_OPTIMIZATION_AGENT_SKILL_ORCHESTRATOR_AND_FRESH_CONTEXT_ACCEPTANCE_V1`
- Owner: existing `OMP`; profile: existing `CODE_OPTIMIZATION`; completion: existing `mission_completion_evidence_gate`
- Product frontier: unchanged, `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`
- Boundary: Engineering-plane; no Runtime, production, user, Authority or CPS mutation

## Corrected design

The previous operational campaign was invalid as semantic completion: Python
selected classifications and hypotheses from domain templates, then constructed
PASS reviews. That path was removed. Structural baseline now only derives
bounded evidence; `CODE_OPTIMIZATION FULL_BASELINE` returns
`CONTINUE_SAME_MISSION` plus `SEMANTIC_EXECUTOR_REQUIRED` until fresh external
Codex evidence is supplied.

The supported repository-local skill is
`.agents/skills/v7-code-optimization/SKILL.md`. Codex discovers repository
skills from `.agents/skills`; the skill triggers on every compact
`CODE_OPTIMIZATION` intent and directs the fresh task to use existing OMP,
profiles and gates rather than a new V7 agent owner.

## Packet and role boundary

OMP creates a bounded immutable executor packet per admitted domain. It binds
Mission/profile/repository/subgraph identity, expiry, owner, entry condition,
source scope/fingerprints, graph, static caller/consumer evidence, unknowns,
canonical references, structural baseline, allowed read-only tools, output
requirements and exact consumer.

The current Codex task is the orchestrator. It performs sequential role passes:
Evidence Explorer, Semantic Analyst, Counterfactual Analyst, immutable review
contexts and, only after `REDUNDANT_LINK_PROVEN`, Cleanup Executor. Python only
packages, validates and gates. Review records provide schema/context separation;
they do not claim independent human/model judgment.

## Coverage and current evidence

Current admitted domains are:

1. `ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION`
2. `OMP_EXECUTION_PROFILE_COMPLETION_LIFECYCLE`
3. `OMP_CODE_OPTIMIZATION_MATERIAL_CHANGE_BRIDGE`

Current evidence inspection covered `governed_apply_policy`, `execute_packet`,
`mission_completion_evidence_gate`, `submit_code_optimization_result`,
`code_optimization_material_change_admission` and its existing anti-regrowth
resolver. Runtime/S11 behavioral equivalence, future external callers and true
model-independent review remain localized owner-backed UNKNOWNs. Other active
SYSTEM_MAP surfaces remain `PARTIAL_OWNER_BACKED_COVERAGE`, not silently claimed
as repository-wide inspection.

## Cleanup and proof loop

One bounded cleanup removed the hardcoded
`_code_optimization_semantic_domain_audit` false-semantic template. CONTROL
without an executor result now returns same-Mission continuation; the
COUNTERFACTUAL requires fresh packet-bound Codex result. Anti-regrowth rejects
reintroduction of that helper or a private domain list.

Focused Code Optimization regression: PASS (`15` tests). `git diff --check`:
pending final validation. Fresh-context acceptance is pending the supported
fresh Codex task created from the committed implementation; it is not inferred
from local function calls.
