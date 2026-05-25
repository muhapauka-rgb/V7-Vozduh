# Runtime Risk Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| autoswitch | active, noisy, multi-authority | unexpected user movement; quiet-window impossible with timer hold only | many users | NO-GO |
| routing-sync | service exited, tool unresolved high-risk | route/rule mutation for all enabled users | all enabled users | forbidden |
| user-switch | governed by preview only | one-user registry/route mutation | one user plus routing side effects | blocked until quiet window |
| kill switch | check OK | mutation/rebuild can affect datapath globally | whole datapath | check-only safe |
| Trusted RU | diagnostic/decision state stale/sensitive | Gosuslugi/Trusted RU route decision influence | policy-sensitive traffic classes | read-only only |
| Direct/RU | autosync state OK | route-class/domain mutation can affect routing decisions | route class / DNS / policy | read-only only |
| proxy runtime | active/public surfaces | proxy apply/guard can affect ingress and runtime traffic | public/API/proxy traffic | no apply |
| provisioning | reconcile OK | set-state/IPAM/user apply can affect live assignments | users/egress pool | read-only only |
| telemetry | active client speed API | writes telemetry/client state; public-token scoped | public telemetry surface | observe only |
| admin API | active local-bound; 192 endpoints static | many high-risk POST actions | platform-wide if misused | no actions |
| rollback | lineage visible, broad restore semantics | restore can rewrite configs/state and services | broad / target-dependent | approval-only |
| release governance | partial | unresolved lineage and runtime drift | reproducibility/commercial trust | continue governance |

## Biggest Blast Radius

`v7-routing-sync`, autoswitch apply, policy apply, proxy runtime apply, kill switch mutation, and broad rollback have the largest blast radius.

## Rollback Clarity

Rollback is clearer for one-user switch than for routing-sync and broad runtime changes. Broad rollback tooling exists but is itself high-risk.
