# N10 functional convergence: blocked by Matrix snapshot churn

Date: 2026-08-24 19:45 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Current residual: `POST_N9_HARD_PATH_RUNTIME_SLO_CONVERGENCE`  
Terminal: `N10_FUNCTIONAL_CONVERGENCE_BLOCKED`

## Decision

No further automatic performance patch was made. The first post-interruption
functional cold validation could not be admitted by the existing controlled
setup owner. It stopped before Candidate, Packet, Lease, Apply or a new client
move, so it yields no latency sample and no SLO conclusion.

The deterministic blocker is a producer/consumer conflict:

```text
v7-health.service
  writes service_matrix continuously
        ↓
v7-intelligence-snapshot-refresh
  requires a stable service_matrix source across its bounded build
        ↓
controlled-certification setup
  STOP_SAFE: source_changed_during_snapshot_build:service_matrix
```

The snapshot owner made six bounded consistency attempts. All failed because
`service_matrix` changed during the build. This is not the repaired
`reservation -> reused Planner` defect and therefore is outside the one
permitted correctness-repair cycle in the convergence contract.

## Fresh reconciliation

| Surface | Fresh result |
|---|---|
| Local / GitHub `Updatesystem` | `4f2013102a3953d8f66d317a73f3968401d2bdca`, clean worktree |
| Deployed model | copied-runtime manifest, safe-deploy `PASS`, no runtime delta required |
| Deployed runtime code | `e67e7e6e11eb662d76f50859d6f334819e4a801a`; later local commit is documentation only |
| Current implementation fingerprint | `a7d64e97052018647d5f55c44161033828538950f4d6d5c09576075a88abfb71` |
| Health owner | `v7-health.service` active, MainPID `3717685`, Nice `0` |
| Full Matrix timer | disabled / inactive |
| Telegram timer | disabled / inactive |
| Controlled source | `amneziawg-exec-20260528-10-8-1-14`, enabled, reserved through `2026-08-31` |
| Synthetic identity | `10.7.0.92`, certification-only, currently `awg0` |
| Action control | `OPEN`, global scope |
| Open CT-M0F reservation | none |
| Active execution lease | none; retained terminal lease is `EXECUTION_FINISHED` |

The retained execution lease is historical, not active. It records
`verification_failed_rollback_failed` from the invalid earlier attempt; its
reservation has a terminal record and it cannot authorize a new action.

## Controlled-state reconciliation performed

1. Read-only Matrix path evidence proved `v7execwg0` is currently UP and its
path components pass.
2. The canonical Matrix owner performed `--direct-local-recovery` for the
stale `interface_down_or_missing` episode. It wrote
`CANONICAL_RECOVERY_WRITTEN`, created no Candidate/Packet/Lease and moved no
user.
3. Existing Planner source/target selection remained STOP_SAFE because the
synthetic user is not currently on the isolated controlled source.
4. Existing controlled-certification setup owner was invoked to reconcile that
baseline. It moved no user and stopped safely at snapshot refresh.

No ordinary user was used, no ordinary route changed, and no timer, cadence,
timeout, verifier, Authority or source code was changed.

## Exact failed functional predicate

The setup owner called the existing snapshot owner with its normal bounded
current-state window. The result was:

```text
source_consistency_attempts = 6
source_stable = false
source_consistency_errors = [source_changed_during_snapshot_build:service_matrix]
returncode = 2
controlled_certification_setup_snapshot_refresh_failed
```

The controlled setup therefore returned:

`GOVERNED_TRANSACTION_STOPPED: controlled_certification_setup_transaction_failed`

The target/source selection before the setup was already fail-closed:

`STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED`

with no exact controlled source/client pair and no admitted target in the
current projection.

## N10 evidence status

| Evidence | Result |
|---|---|
| Latest old valid cold sample | fingerprint `44eaaefb…`; 4920.353 ms; historical only |
| Latest invalid sample | fingerprint `34b1bd8c…`; reservation missing from reused Planner lineage |
| Repair for that lineage defect | commit `e67e7e6e`, deployed |
| Valid sample on current fingerprint `a7d64e…` | none |
| Frozen homogeneous SLO series | not started |
| Hard-path SLO result | not evaluated |

STUN remains only a route/egress identity proof. No run redefined S11 or
substituted STUN for required failure-class/profile service verification.

## Smallest remaining architectural choice

Owner decision is required before further work. Choose one bounded direction:

1. **Snapshot isolation/hand-off:** make the existing snapshot owner consume
   an atomic Matrix generation or a verified immutable Matrix snapshot for the
   controlled setup transaction, while preserving freshness and fail-closed
   semantics.
2. **Health write coordination:** provide an existing-owner coordination point
   so the controlled setup can obtain one stable current Matrix generation
   without changing the health cadence or disabling its safety role.
3. **Substrate separation:** move the controlled certification setup to an
   existing lawful substrate whose required Matrix projection is stable during
   setup.

Any option needs a new bounded engineering residual and explicit approval. It
must not weaken S11, stop `v7-health` merely to make a benchmark pass, or add
a parallel state/health owner.

## Exact next frontier

`OWNER_DECISION_REQUIRED: resolve stable Matrix-generation hand-off for
controlled-certification setup, then restart from fresh reconciliation and one
functional cold validation on a new immutable fingerprint.`

