# Live VLESS multi-target recovery blocker

Date: 2026-09-01

## Scope

This report records one live V7 Runtime attempt after the recovery-latency SLO
re-entry. It is evidence for the active contract, not acceptance evidence: no
ordinary user was moved.

## Proven automatic path

The normal `v7-health.service` owner, not Codex, observed an ordinary
profile-required VLESS failure and invoked the existing Matrix consumer. The
consumer receipt recorded an active source scope of three ordinary users.

| Stage | Measured result | Owner |
| --- | ---: | --- |
| Detector batch probe wall | 1505 ms | existing `v7-egress-diagnose` batch producer |
| Detector post-processing | 1607 ms | existing Matrix consequence path |
| Detector total | 3113 ms | existing `other_required` health role |
| Matrix/consumer attempt | 36.5–38.5 s | existing Matrix -> governed executor chain |
| Result | `STOP_SAFE`, no route mutation, zero users moved | existing governed executor |

The longer historical 41 s detector invocation occurred immediately after the
health-service restart; subsequent live batches returned to about 3.1 s. It
remains visible as fail evidence and is not counted as a good sample.

## Exact causal blocker

Planner correctly selected different safe targets for the affected profiles:
one target for the Telegram-compatible profile and another for the profiles
that additionally require YouTube. The optional existing Core-primary cohort
commit accepts one target only. Runtime treated that optimisation constraint as
a reason to stop the whole recovery before Authority consumption:

```text
core_primary_cohort_not_admissible_before_authority_consumption
-> l3_production_validation_downstream_proof_failed
```

This is a generic implementation defect. It is not an unsafe target, an
Authority rejection, a missing Matrix incident, or an instruction for Codex to
move any user.

## Repair

The Core-primary cohort optimisation is now selected only for a bounded cohort
whose Planner-selected target is exactly one channel. A bounded multi-target
recovery retains the existing governed per-member route path. Matrix still
owns the failed source; Planner still selects targets; Authority, Candidate,
Packet, Lease, Barrier, route writer and required-service S11 stay unchanged.

Focused checks passed:

- single-target cohort still uses one Core-primary commit;
- Core-primary owner binding remains exact;
- multi-target cohort selects the existing governed per-member fallback.

## Next action

Deploy this bounded generic repair, then observe the already-running V7 health
caller process the current VLESS incident. Acceptance requires a fully
automatic current sample with exact failure-to-all-affected-S11 timing; no
manual recovery is valid evidence.
