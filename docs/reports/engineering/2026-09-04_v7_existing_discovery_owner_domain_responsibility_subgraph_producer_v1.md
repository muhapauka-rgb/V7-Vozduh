# Engineering Report — V7 Existing Discovery Owner Domain Responsibility Subgraph Producer V1

## Mission

Implement the minimum on-demand, domain-scoped derived-evidence producer for
`ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION`, under the existing
Engineering evidence and OMP completion owners.

## Current authoritative frontier preserved

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` remains unchanged. The active
product/program frontier is still the existing Recovery Latency SLO frontier;
this Mission neither admits nor projects a replacement Mission into CPS.

## Decision

`EXTEND_EXISTING_OWNER`. The implementation extends only
`tools/v7_sync_lib.py`, the existing read-only `tools/v7-truth-check` CLI, and
their tests. It creates no Agent System, Coordinator, Function Graph owner,
planner, queue, watcher, daemon, Runtime, persistent database, registry or
new canonical truth source.

## Existing producer / consumer / execution path

The producer is `derive_responsibility_subgraph`. Its consumer is the existing
`MISSION_COMPLETION_EVIDENCE_GATE`, reached through the already-admitted
`GPT_DECISION_REVIEW` profile and its required `ARCHITECTURE_REVIEW`. The
proof is an in-memory `admit_execution_profile_contract → result → review →
completion gate` chain. It does not create a BDP candidate or a disposable
BDP/OMP Mission.

## Input boundary

The request is fail-closed and requires Mission/run/profile/input identity,
the authorized domain, source fingerprint, typed canonical references, exact
seed entrypoints, a five-path allowlist, depth/file/edge/unknown-output/TTL
bounds and generator version. Unknown domain, unknown path, bad fingerprint,
unbounded scope or invalid limits stop safe.

## Pilot scope

The bounded responsibility subgraph spans these current source surfaces:

- `tools/v7-users-autoswitch`
- `admin_core/operator_execution.py`
- `admin_core/operator_execution_pipeline.py`
- `tools/v7-service-matrix-test`
- `systemd/v7-health.service`

Seed entrypoints are the existing adaptive service-failure cohort contract,
governed packet execution, governed apply policy and the health unit. This is
a responsibility subgraph, not a claim that any single source file owns the
entire responsibility.

## Derived-evidence contract

The result is explicitly `DERIVED_EVIDENCE`, `canonical: false`, discardable,
and has `decision_authority: NONE`, CPS/Runtime/Production/Authority impact
`NONE`. It records direct AST-call and systemd declaration facts only. State,
lock/lease and process behavior that was not statically derived is explicitly
`UNKNOWN_NOT_DERIVED`; no Runtime or production observation is claimed.

## Canonical references

Responsibility, owner and plane are typed top-level references, not AS-IS node
types. AS-IS nodes remain implementation/evidence surfaces such as file,
function and systemd unit.

## Fingerprints and freshness

`SUBGRAPH_FINGERPRINT` covers only canonical static structural content.
`RESULT_FINGERPRINT` covers the full derived result, including generated and
expiry metadata. The result declares the exact fingerprint scopes, TTL and
that external expiry enforcement is not claimed.

## Unknowns, semantics and counterfactuals

Unresolved or ambiguous static calls are retained as bounded unknown evidence,
not converted into guessed edges. Every node/edge and every exposed
counterfactual reference is `UNCLASSIFIED` for semantic necessity. The
producer cannot mark anything redundant or superseded and it proposes no
deletion, migration or compatibility removal.

## Complexity-regression support

`responsibility_subgraph_structural_delta` compares two immutable derived
snapshots by node/edge identity and emits an empty bounded signal list unless
a later existing owner supplies a lawful signal rule. It deliberately does not
turn structural removal into a semantic-deletion verdict.

## Completion binding

The existing completion gate now conditionally consumes a supplied derived
subgraph only when its static fingerprint, profile-output binding, exact
review, identity and current Mission fields agree. Missing, stale, altered or
ambiguous material stops safe. The gate has no graph-analysis capability and
does not mutate CPS.

## Verification

`tools/v7-truth-check --omp-responsibility-subgraph-proof --json` passed:

- derived pilot: `34` bounded nodes, `58` direct static edges, `439` retained
  unknown references;
- profile/review/subgraph identity: consumed by the existing completion gate;
- BDP Mission created: `false`;
- CPS effect: `false`;
- Runtime, Production and Authority impact: `NONE`.

Focused tests passed: `30` tests across responsibility-subgraph,
bounded-execution-profile and functional-footprint contracts. The existing
bounded execution-profile proof also passed with no CPS effect.

## Functional-footprint reconciliation

`tests/unit/test_omp_functional_footprint.py` had stale expectations: the
repository has four real `program_execution_reconciliation` callers, not
three. Its three altered historical automation assertions expected generic
failure, but the actual current Recovery Latency SLO frontier intentionally
short-circuits those historical projections and returns
`ACTIVE_NOT_CONSUMED`. Tests now assert that current canonical behavior rather
than misclassifying the active frontier as a failed historical contract.

## Explicit non-effects

No CPS, Matrix, Planner, Authority, SYSTEM_MAP, canonical reference, runtime
service, systemd installation, deploy state, route, packet, recovery action,
user movement, source cleanup or code-optimization change was executed.

## Residual and exact next action

The producer proves bounded static structure only. It does not prove current
state/lock/process semantics, real Runtime behavior, production consumption,
or that any node is necessary/redundant/superseded. The exact next action, if
needed by an existing owner, is to consume one fresh immutable result through
the existing completion gate and independently supply the missing semantic or
Runtime evidence; no new discovery system is authorized by this result.
