# Codex Continuation Prompt

```text
V7 CODEX TASK — WORLD MODEL PROVENANCE TRACE

Task

Do NOT redesign.
Do NOT patch first.
Do NOT create architecture.
Do NOT create owner.
Do NOT create runtime.
Do NOT create planner.
Do NOT create wake system.
Do NOT create truth source.
Do NOT move users.

MISSION

Find whether Planner received incorrect/incomplete World Model or Planner overclassified correct input.

This is an executable provenance trace.
Use source code, current reports, state files, fixtures, and production evidence already captured.
Do not infer from architecture when executable values are available.

TARGET CANDIDATE

user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
current_failures: []

READ FIRST

- docs/reports/engineering/2026-07-01_172201_gpt_handoff_package.md
- docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md
- docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md
- docs/reports/engineering/2026-07-01_151234_formal_model_verification.md
- docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md
- docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md
- docs/reference/V7_RUNTIME_MODEL.md
- docs/reference/V7_DECISION_MODEL.md
- docs/reference/SYSTEM_MAP.md
- docs/policies/POLICY_001_HARD_FAILURE.md
- docs/policies/POLICY_004_AUTHORITY.md
- docs/policies/POLICY_008_FRESHNESS.md

KNOWN FACTS

Good L3 test path:

current candidate has required-service failure row:
telegram DOWN / PERSISTENT_FAIL / FRESH
-> current_failures non-empty
-> wake accepted
-> emergency gate passes

Production path:

selected source awg0 has no Runtime-verifiable required-service failure row
-> current_failures=[]
-> required_service_failure_required
-> confirmed_l3_wake_required
-> STOP_SAFE

First executable difference already found:

selected_move.candidates[current_source].service_suitability.per_service[required_service]

OPEN QUESTION

Why did Planner see or derive a World Model where awg0 became current_egress_not_eligible, but no same-subject required-service failure exists for awg0 at Runtime evidence extraction?

Choose only after proof:

A. Planner input/world model was wrong or incomplete.
B. Planner input was correct, but Planner overclassified broad current_egress_not_eligible as L3 failover.
C. Runtime evidence extraction consumed a different fact than Planner consumed.
D. Serialization/restore/authority regression reappeared.
E. TRACE_INCONCLUSIVE with exact missing evidence.

TRACE REQUIRED

Trace executable values only:

Observation
-> Service Matrix
-> Read Models
-> Planner Inputs
-> _decision_for_user()
-> selected move
-> approved_plan_lock.selected_moves
-> restore_barrier.approved_plan_lock.selected_moves
-> _emergency_failover_move_evidence()

For each fact used by Planner for 10.7.0.5 / awg0 / vless, record:

- producer
- file/state source
- generation
- timestamp
- freshness
- raw value
- normalized value
- planner consumer
- why Planner saw current_egress_not_eligible
- whether Runtime saw the same fact
- whether the fact can prove L3 required-service failure

TRACE POINTS

1. user registry assignment for 10.7.0.5
2. awg0 channel state
3. awg0 service matrix row
4. required services for the user/cohort/group
5. route class / service profile used by Planner
6. current candidate built for awg0
7. current candidate eligibility and blockers
8. current candidate service_suitability.per_service
9. target candidate vless service_suitability.per_service
10. reason list before selected move creation
11. move_type chosen by _decision_for_user()
12. selected move after Planner
13. selected move inside approved plan lock
14. selected move inside restore barrier
15. Runtime move_evidence
16. current_failures
17. wake decision
18. emergency_failover_authority_gate

QUESTIONS

1. What exact input made Planner set current_egress_not_eligible?
2. Was that input a required-service failure on awg0?
3. If not, what kind of ineligibility was it?
4. Did Runtime receive the same input?
5. Did selected move preserve the relevant input?
6. Did Runtime extract from the same source and same services?
7. Is the first divergence in Observation, World Model, Planner normalization, selected move serialization, restore barrier, or Runtime extraction?
8. Is Planner input wrong/incomplete, or did Planner overclassify correct input as L3 failover?

DO NOT

- create new wake event system;
- create new truth source;
- create new Runtime;
- create new Planner;
- bypass Runtime gate;
- bypass required_service_failure;
- treat current_egress_not_eligible as sufficient for L3 execution;
- patch Runtime to accept empty current_failures;
- certify capability without movement/verification/learning;
- move more than one user;
- rerun broad architecture investigations.

REPORT

Create:

docs/reports/engineering/<timestamp>_world_model_provenance_trace.md

Include:

- Summary
- Target candidate
- Source files/state inspected
- Planner input provenance table
- Runtime input provenance table
- Planner vs Runtime fact comparison
- First divergence
- Owner
- Exact file/function
- Minimal correction direction
- Tests needed if implementation follows

FINAL OUTPUT

Return exactly:

FIRST_DIVERGENCE_FOUND

or

TRACE_INCONCLUSIVE

If found, return only:

- first divergent fact
- producer
- consumer
- owner
- exact file/function
- minimal correction direction

No implementation unless explicitly requested.
```
