# RESET-M2 Truth Owner and State Surface Collapse Engineering Report

Status: `RESET_M2_ONE_OWNER_PER_NECESSARY_RUNTIME_FACT_AND_COLLAPSE_DISPOSITIONS_COMPLETE`

Intent closed: every necessary routing Runtime fact now has one named existing authoritative owner and every surrounding projection has a collapse disposition. This phase changes no live Runtime state or routing behavior.

| Runtime fact | Authoritative existing owner/source | Necessary reader/decision | Freshness/invalidation | Disposition |
| --- | --- | --- | --- | --- |
| user assignment | existing users/assignment registry written by `v7-user-switch`/autoswitch owner | PLAN delta, APPLY CAS, route verify | assignment generation; any writer commit invalidates | `KEEP_AUTHORITATIVE` |
| egress health | current Service Matrix/quality owner receipt | OBSERVE/PLAN target eligibility | generation and bounded age; new probe/failure invalidates | `KEEP_AUTHORITATIVE` |
| capacity | existing egress registry plus generation-bound Matrix capacity receipt | PLAN admission and blast reserve | registry/policy/assignment change invalidates | `MERGE` into one prepared target receipt |
| active policy | `/etc/v7/policy.json` existing policy owner | PLAN and pre-apply safety validation | policy generation/hash; any owner write invalidates | `KEEP_AUTHORITATIVE` |
| Authority generation | `admin_core/operator_execution.py` owner-issued policy/Authority audit lineage | pre-apply admission | expiry, policy/decision supersession invalidates | `KEEP_AUTHORITATIVE` |
| incident/failure generation | existing Service Failure/Matrix incident owner | OBSERVE trigger and affected scope | fresh Matrix generation/recovery invalidates | `MERGE` into compact failure receipt; legacy incident history read-only |
| target health receipt | existing Matrix exact-path receipt | PLAN target and bounded revalidation | path fingerprint, generation, age or topology change invalidates | `KEEP_AUTHORITATIVE` |
| active operation/lease | existing `operator_execution` Packet/lease/barrier owner | single-writer fencing and idempotency | terminal/expiry/generation mismatch invalidates | `KEEP_AUTHORITATIVE` |
| kernel route state | Linux kernel route/rule/mark tables through existing route-check owner | APPLY reconciliation and VERIFY | every apply/netlink/process change invalidates | `KEEP_AUTHORITATIVE` |
| verification result | existing exact user-route/payload verifier receipt | success, rollback or forward recovery | operation/generation/route/payload context bound | `KEEP_AUTHORITATIVE` |
| outcome | existing execution feedback/closure append-only owner | async evidence, Replay, Learning, CPS/OMP residual | immutable operation identity; correction is append-only | `KEEP_AUTHORITATIVE` |

Collapse dispositions for surrounding surfaces:

- CPS remains sole compact Program/capability frontier; it is `DERIVED_ASYNC_ONLY` for routing facts and cannot be a Core input.
- OMP, Reports, Production Maturity, Replay, Learning, Polygon and campaign state are `DERIVED_ASYNC_ONLY`.
- broad snapshots, dashboards and inventories are `DERIVE_ON_DEMAND` or `DERIVED_ASYNC_ONLY`.
- historical Packet, Mission, incident and campaign projections are `LEGACY_READ_ONLY`.
- duplicate capacity/health/incident summaries `MERGE` into generation-bound prepared receipts; physical retirement waits for M7/M9 evidence.

The current detailed CPS compatibility projection remains source history during migration, but only its Section 0 Program frontier is authoritative. It does not gain routing-truth status. Hard-coded legacy Program normalization remains a source defect to be corrected with compact CPS consumer work; it grants no production/runtime effect in this report.

Owner: existing Runtime fact owners, CPS volatile owner and OMP development-plane owner. No new owner/store/registry was created.

Evidence: Master Audit code/state graph, CPS Section 0, SYSTEM_MAP routing truth chain, existing policy/Matrix/assignment/operator-execution/verifier/feedback owners.

Residual: specify the exact vNext positive/negative contracts, recovery clock, freshness decisions, fencing and crash recovery before code.

Exact successor: `EXECUTE_RESET_M3_VNEXT_ARCHITECTURE_AND_MINIMAL_CORE_CONTRACTS`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
