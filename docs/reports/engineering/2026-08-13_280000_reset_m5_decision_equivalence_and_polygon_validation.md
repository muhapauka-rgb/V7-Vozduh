# RESET-M5 Decision Equivalence and Polygon Validation Engineering Report

Status: `RESET_M5_CLASSIFIED_DECISION_EQUIVALENCE_AND_POLYGON_VALIDATION_PASS`

What changed: no Runtime code or wiring changed. Existing autoswitch/Polygon-derived policy fixtures and the new Core shadow tests were consumed as one decision-equivalence gate.

Evidence: 12/12 focused tests PASS, covering transient versus persistent service failure, source-scoped selection, multiple transient failures, deterministic Core planning, freshness, Authority/fencing/blast, target health/allowlist/capacity, zero effects and engineering-plane exclusion.

| Comparison | Verdict | Classification |
| --- | --- | --- |
| transient single-sample or nonpersistent failure | Legacy selects no move; Core receives no qualifying failure scope | `EQUIVALENT_AT_CONTRACT_BOUNDARY` |
| persistent qualifying source failure with healthy lawful target | Legacy selects failover; Core returns `PLAN_READY` for same source/user/target class | `EQUIVALENT_REQUIRED_BEHAVIOR` |
| source-scope mismatch | Legacy selects zero moves; Core validates exact declared scope/assignments | `EQUIVALENT_REQUIRED_BEHAVIOR` |
| unhealthy/disallowed/no-capacity target | both refuse a move | `EQUIVALENT_SAFETY` |
| missing/stale Authority, generation or fence | Core STOP_SAFE is stricter than legacy dry-run planning | `INTENTIONAL_CORE_SAFETY_DIVERGENCE` |
| target ranking | Legacy uses broad advice/history; Core uses fresh allowed/healthy capacity and deterministic tie-break | `INTENTIONAL_SIMPLIFICATION`; any policy-required ordering must be prepared by the policy owner before Core |
| evidence/closure expansion | Legacy produces broad operation/campaign artifacts; Core emits only compact shadow decision/apply/verify contracts | `INTENTIONAL_ASYNC_DIVERGENCE` |

No unexplained divergence remains in the admitted Core contract. Polygon/replay evidence is consumed as acceptance corpus, not copied into Core or executed synchronously. Proven legacy defects—broad pre-apply reconciliation, historical state dependence, campaign bookkeeping and multi-process planning—were not reproduced.

Risk closed: superficial same-output equivalence cannot force known legacy defects into Core, while required failure classification, target legality, capacity and safety behavior remain covered.

Owner: existing autoswitch/Polygon test owners and the existing `admin_core` namespace. Legacy remains sole production writer.

Complexity delta: code delta 0 in M5; process/timer/store/state/writer delta 0; Runtime hot-path delta 0.

Residual: prepare a controlled scope-specific migration adapter with atomic writer fencing, deploy through the existing safe owner, and prove zero double-write before any Core effect.

Exact successor: `EXECUTE_RESET_M6_CONTROLLED_MIGRATION_SINGLE_WRITER_FENCED_CUTOVER`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
