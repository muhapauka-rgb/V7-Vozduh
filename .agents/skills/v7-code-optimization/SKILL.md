---
name: v7-code-optimization
description: Run the V7 governed Code Optimization campaign when the user says `CODE_OPTIMIZATION FULL_BASELINE`, `CODE_OPTIMIZATION CHANGED`, `CODE_OPTIMIZATION DOMAIN`, `CODE_OPTIMIZATION CONTINUE`, or `CODE_OPTIMIZATION STATUS`. Use only in this V7 repository; do not use for generic refactoring.
---

# V7 Code Optimization

## Trigger and boundary

On a compact `CODE_OPTIMIZATION` intent, read the current CPS, OMP protocol,
Operational Maturity Program and this skill. OMP remains the sole orchestration
owner, `CODE_OPTIMIZATION` the bounded profile, and
`mission_completion_evidence_gate` the completion consumer. Do not create a
V7 coordinator, Agent System, owner, queue, registry, planner, CPS frontier,
Runtime truth source or Authority. Keep the active Product frontier unchanged.

## Algorithm

1. Invoke the existing compact caller or the deterministic bundle wrapper,
   preserving the user's scope: `tools/v7-truth-check --json CODE_OPTIMIZATION
   <scope...>` or `tools/v7-code-optimization-bundle prepare --mode <scope>
   --output-dir <disposable-temp-dir>`. The first result is allowed to be
   `SEMANTIC_EXECUTOR_REQUIRED`; that is an internal milestone, never the
   response to the user. Do not ask the user to relay packets.
2. Preparation must rediscover current domains from existing owner
   configuration plus current SYSTEM_MAP executable surfaces. Its projection is
   disposable and must not become a registry, queue, owner or truth source.
3. For one frozen `FULL_BASELINE`, use exactly two distinct native contexts:
   `ANALYST` and independent `REVIEWER`. The Analyst records exact path, symbol, line, input/output,
   reads/writes, errors/STOP_SAFE, compatibility consumer, observability,
   terminal effect, canonical owner and removal/bypass consequence; it also answers
   the semantic question and generates/ranks counterfactuals. Work domains
   sequentially and record one immutable checkpoint after each completed domain.
   Dispatch the two contexts through native internal-agent tools: Analyst first
   for the current packet, then Reviewer for the immutable Analyst artifact.
   Record observed context IDs and manifest/packet/result fingerprints. Python
   validates this structural binding only; it must not invent IDs or claim
   model-level provenance.
   Analyst final payload is one JSON object with every existing
   `CODE_OPTIMIZATION_OUTPUT_FIELDS` field plus `symbol_evidence`,
   `counterfactual_attempts` and `considered_mechanisms`; it never contains a
   review verdict. `mission_reference`, `profile_reference` and
   `input_fingerprint` are the exact scalar values from the admitted profile,
   never descriptive objects. `responsibility_subgraph` is exactly the six-field
   identity projection `domain_id`, `repo_fingerprint`, `subgraph_fingerprint`,
   `result_fingerprint`, `generated_at`, `expires_at` from the prepared packet,
   without summaries or renamed keys. Every non-UNKNOWN responsibility classification
   includes `subject`, `caller`, `consumer`, `behavior_state_effect`,
   `semantic_contribution`, `invalidation_triggers`, `claim_type` and
   `evidence_item_ids`; the claim type must be explicitly supported by every
   cited evidence item. Every ranked candidate includes `caller`, `consumer`,
   `control_path`, `counterfactual_path`, `proof_plan` and
   `evidence_item_ids`. Reviewer final payload is one JSON object with exactly five
   named sections, one verdict, rejected candidate IDs/reasons and the exact
   immutable Analyst artifact hash; it never rewrites Analyst fields. Invalid
   JSON or a missing field permits one transport-only correction in the same
   role, then `STOP_SAFE_INVALID_NATIVE_AGENT_OUTPUT`.
5. Every UNKNOWN names the missing fact, existing evidence owner, acquisition
   action and re-entry condition. Static reachability, LOC, tests,
   documentation or a missing static caller alone are not semantic proof.
6. Only `REDUNDANT_LINK_PROVEN` permits at most one bounded product cleanup.
   Recompute the before/after subgraph, callers/consumers, regression and
   residue. Otherwise record an evidence-backed honest zero.
7. Freeze the proposed result. The one independent Reviewer checks all five
   mandatory aspects—Architecture, Safety, Evidence, Quality and Mission
   Integrity—in one context and returns only rejected candidate IDs. It cannot
   edit the proposal. One targeted Analyst re-entry is allowed for those IDs;
   a second rejection is the exact STOP_SAFE terminal.
8. Re-enter the original prepared packets and external results with
   `tools/v7-code-optimization-bundle consume`, which calls
   `submit_code_optimization_result` and `mission_completion_evidence_gate`.
   Require exactly one Analyst and one independent Reviewer identity,
   exact packet/result bindings and no collisions. Python may collect, package,
   fingerprint, validate and reject; it may not author semantic classifications,
   counterfactual verdicts or PASS reviews.
9. `FULL_BASELINE` also calls `tools/v7-code-optimization-bundle
   benchmark-prepare` in a disposable temporary directory and uses the same
   two-role protocol.
   The
   fresh benchmark context receives its bounded files and question but not the
   expected redundant symbol or answer. The benchmark is two-stage: first the
   agent emits a read-only candidate with no mutation; only then may the
   orchestrator call `tools/v7-code-optimization-bundle benchmark-authorize`
   to issue a candidate-fingerprint-bound fixture-only authorization, after
   which the same agent may perform one cleanup. Acceptance requires
   independent `REDUNDANT_LINK_PROVEN`, exactly one fixture-only cleanup,
   preserved behavior/errors/state, zero residue, one independent all-aspect PASS
   reviews and zero product/CPS/Runtime/Production/Authority effect.
10. Consume `CONTINUE_SAME_MISSION` until the product-domain campaign returns
    its legal internal terminal, then call
    `tools/v7-code-optimization-bundle accept` with the same prepared packet
    set, native results, consumed product result and verified benchmark. Only
    that deterministic joint gate may return
    `V7_CODE_OPTIMIZATION_AGENT_RUNTIME_FULLY_ACCEPTED`. `STATUS` is read-only
    and reports current recomputed coverage; it creates no durable run state.
    After an executed campaign, create or update one compact Engineering Report
    with coverage, contexts, benchmark, cleanup, limits, effects, terminal and
    exact next compact command.

## Native context fail-closed rule

Stop at the first exact `STOP_SAFE_CODE_OPTIMIZATION_AGENT_RUNTIME_*` result if
the Codex child runtime is unavailable, a packet is stale, a role output is
missing, context identities collide, a reviewer does not PASS, a semantic
template reappears, the benchmark answer is leaked/not discovered, or cleanup
proof/residue is invalid. Never fall back to personas in one context or
fabricated ids. Absence of a proved product cleanup is an honest zero, not a
failure.

## Tool and truth boundary

Python packages, fingerprints, validates, tests and gates. It never decides
semantic truth or auto-generates classifications, candidates or PASS reviews.
No fresh executor result means exactly `SEMANTIC_EXECUTOR_REQUIRED` and
`CONTINUE_SAME_MISSION`. Reject stale, duplicate, unsupported and
blanket-UNKNOWN submissions. Distinguish `FULL_ACTIVE_COVERAGE` from
`PARTIAL_OWNER_BACKED_COVERAGE`; keep unadmitted surfaces as owner-backed local
blockers.

## Completion

Do not stop at packet-ready, tests-pass, report-created or candidate-ready. The
only successful full-command terminal is
`V7_CODE_OPTIMIZATION_AGENT_RUNTIME_FULLY_ACCEPTED`.
Report in compact Russian: intent, coverage, inspected symbols, classes,
hypotheses/counterfactuals, cleanup, localized UNKNOWN, review separation,
terminal and next compact command. Use existing canonical V7 docs and one
Engineering Report; never a new Program or roadmap.
