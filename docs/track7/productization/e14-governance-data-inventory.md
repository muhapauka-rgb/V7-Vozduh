# E14 Governance Data Inventory

## Purpose

E14 starts from the current truth problem: V7 has strong governance evidence,
but the operator truth still lives in many human-readable reports, evidence
folders, runtime tools, journals, and state files. The productization layer must
normalize those sources into canonical machine-readable governance objects.

## Current Truth Sources

| Source | Current role | Truth type | Productization gap |
|---|---|---|---|
| `BLOCK_E*.md` reports | Authoritative block verdicts and mutation statements. | Historical governance verdict. | Human-readable, not queryable as current operator truth. |
| Evidence directories | Per-block command output, JSON samples, tests, snapshots. | Evidence and replay material. | Naming varies by block; current/historical distinction is implicit. |
| `tools/v7-control-plane-governance-check` | Aggregated governance assertions. | Current governance status. | Strong checker, but not a full read model for UI. |
| `tools/v7-second-canary-target-readiness` | Target readiness and reserved target checks. | Target readiness. | Output needs canonical schema and freshness metadata. |
| `tools/v7-restore-settle-gate` | Restore-settle decision and samples. | Restore gate truth. | Gate result must be linked to operation/generation lifecycle. |
| `tools/v7-users-autoswitch` dry-run | Selected moves, candidate pressure, barrier/generation behavior. | Planner/apply pressure and movement preview. | Needs stable selected-move set schema and fingerprint ownership. |
| Planner/apply journals | Timer events, recompute behavior, selected move outcomes. | Runtime lineage. | Raw journal slices are too low-level for primary operator truth. |
| Switch history | User movement record. | Movement lineage. | Needs approval linkage, unapproved movement classification, and operation id. |
| `autoswitch-restore-barrier.json` | Restore barrier and clearance state. | Restore/generation safety. | Needs contract schema and lifecycle ownership. |
| Runtime checkers | Reconcile, route, kill-switch, provisioning checks. | Runtime health. | Needs common health schema and stale handling. |
| Egress registry | Target metadata, reservation, capacity, protocol. | Target pool truth. | Needs target readiness and reservation read model. |
| Users registry | User-to-egress assignment and user summary. | Runtime routing assignment. | Needs safe summary and hash-first freshness model. |
| Runtime/repo diff | Deployed vs repo tool lineage. | Release and deploy confidence. | Current warnings must surface without blocking unrelated read-only views. |
| Release lineage check | Release provenance and partial-lineage warnings. | Release governance. | Needs normalized lineage status and current release id. |
| E13 design docs | Product UX and contract intent. | Productization requirements. | Must be formalized into schemas and API models. |

## Duplication And Drift

- Target readiness appears in multiple evidence directories as JSON and pretty
  text.
- Restore-settle appears as live samples, pre-restore checks, and post-restore
  samples.
- Selected moves appear as autoswitch output, local copied-state rehearsals,
  and report summaries.
- Runtime checker output is repeated in block evidence and governance checker
  summaries.
- Movement truth exists in switch history, report narrative, and registry hash
  changes.
- Generation-token evidence exists in E12 runtime deploy/test evidence but not
  as a durable operator object.

## Stale Evidence Risks

| Risk | Example | Required mitigation |
|---|---|---|
| Historical evidence mistaken for live state | Earlier NO-GO readiness vs later GO readiness. | Every evidence object needs `state_source`, `collected_at`, `valid_until`, and `superseded_by`. |
| Copied-state rehearsal mistaken for live approval | E12 local copied-state nonzero budget rehearsal. | State source must be `live`, `copied_state`, or `simulation`. |
| Selected moves sampled before timer recompute | E11.14 delayed apply movement. | SelectedMoveSet must carry generation id, sampled_at, source, and expiry. |
| Restore-settle GO mistaken for lifecycle complete | Apply restore can still trigger delayed movement. | RestoreSettleState must link to delayed monitor contract. |
| Target readiness GO mistaken for movement approval | Target readiness does not approve selected movement. | RuntimeSnapshot must separate readiness, approval, and execution eligibility. |
| Generation token mistaken for blanket approval | Token must bind exact fingerprint and budget. | GenerationClearance schema must include allowed users/targets and selected-move hash. |

## Operator Confusion Risks

- Reports answer "what happened" well, but not "what can I safely do now".
- Evidence folders are audit-rich but not optimized for first-screen operator
  state.
- The same concept appears under different names across blocks: selected moves,
  movement pressure, candidate moves, dry-run plan.
- Live vs historical vs copied-state requires domain memory.
- Timer state is operationally critical but not a normalized first-class object.

## Machine-Readable Gaps

The following canonical objects are missing today:

- MovementApproval.
- RollbackApproval.
- RestoreApproval.
- GenerationClearance.
- CohortApproval.
- EmergencyContainment.
- ReplayProtection.
- BlastRadiusContract.
- DelayedMonitoringContract.
- RuntimeSnapshot.
- OperationTimeline.
- MovementLineage.
- RestoreLineage.
- GenerationLineage.
- GovernanceVerdict.

## Inventory Verdict

The current governance evidence is strong enough to seed a read-only operator
foundation, but it is not productized. E14 must make reports and evidence
secondary audit material behind canonical current-state objects.

