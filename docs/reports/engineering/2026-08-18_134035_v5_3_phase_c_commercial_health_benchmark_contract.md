# V5.3 Phase C commercial health benchmark contract

Time: `2026-08-18 13:40 MSK`

Summary: `PHASE_C_CONTRACT_UPDATED; FULL_VENDOR_RESEARCH_NOT_EXECUTED`

## Existing evidence discovery

| Reference | Disposition | Existing evidence reused / exact residual |
| --- | --- | --- |
| Envoy | `RESULT_REUSED_VALID` | Hard Failure, Recovery Admission and Anti-Flap policies already cover active/passive health, outlier ejection and recovery. |
| HAProxy | `RESULT_REUSED_VALID` | Existing policies cover fall/rise, active/passive checks and asymmetric recovery. |
| Google Cloud | `RESULT_REUSED_VALID` | Existing policies/research cover protocol checks, consecutive thresholds and target eligibility. |
| AWS ELB/NLB | `RESULT_REUSED_VALID_CONDITIONAL_REFERENCE` | Existing policies cover target health, failure/recovery thresholds and eligibility; reuse only for a named residual. |
| FRRouting/BFD | `RESULT_REUSED_VALID` | Existing Program, OMP and commercial-router report cover lightweight liveness and routing/control/dataplane separation. |
| Cisco | `RESULT_REUSED_VALID` | Existing Hard Failure/Recovery/Anti-Flap policies cover BFD/object tracking; commercial-router report covers IOS XR control-to-dataplane ownership. |
| Fortinet FortiGate | `TARGETED_GAP_RESEARCH_REQUIRED` | Generic SD-WAN and isolated Fortinet references exist, but no current compact owner-consumed Link Health Monitor/Performance SLA mechanism record was found. |
| MikroTik RouterOS | `TARGETED_GAP_RESEARCH_REQUIRED` | No existing repository benchmark record was found for gateway/recursive next-hop/multi-WAN mechanisms. |
| Juniper/Arista/Palo Alto/Ubiquiti/other | `BENCHMARK_NOT_REQUIRED_DUPLICATE_PATTERN` | Not mandatory unless a named unique mechanism gap survives Cisco plus FRRouting/BFD and the required commercial set. |

This classification is discovery evidence, not the Phase C terminal and not
permission to run the two targeted studies without existing OMP admission.

## Exact Program change

`docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`, existing
V5.3 Phase C only, plus one direct Definition-of-Done consumption reference.

Before: Phase C named Envoy, HAProxy, Google, FRRouting/BFD and conditional AWS
patterns but did not explicitly contract commercial SD-WAN/multi-WAN coverage,
source-versus-target semantics, stability/history projection, evidence classes,
comparison schema, terminal or downstream consumers.

After:

- two layers: infrastructure health and commercial routing/SD-WAN/multi-WAN;
- mandatory reference set and conditional/duplicate rules;
- five evidence classes and full observation-to-re-admission lifecycle;
- `SOURCE_HEALTH_NOT_EQUAL_TARGET_READINESS`;
- compact stability/history projection with no FAST raw-history scan;
- `REUSE / ADAPT / REJECT` admission law;
- one comparison schema covering 17 mechanism classes;
- Phase D/E/F/H consumers;
- terminal
  `MATURE_HEALTH_AND_COMMERCIAL_ROUTING_MECHANISM_COMPARISON_CONSUMED`.

Delta: Program/OMP contract only. No new Phase, Mission, owner, tracker,
benchmark project, truth source or vendor-report series was created.

## Current state and boundary

- Program version: `5.3`.
- V5.3: `REGISTERED_BOUNDED_WORKSTREAM`; registration disposition
  `NOT_ADMITTED`; live status is CPS-owned.
- CPS generation: `cpsgen_RS7_ADMIN_COMPLETE_2A5DA0F2`.
- Current CPS Mission: `V7_OMP_BDP_65CB2232971BC224D937140C_V1`.
- Current CPS successor: `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
- Matrix frontier: first unadmitted candidate remains
  `V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`.
- Current Matrix blocker: no exact CPS-admitted V5.3/Phase C Mission identity;
  the RS6 frontier wins.
- Next executable action: `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.

Canonical Reference / SYSTEM_MAP changes: `NONE`; existing Matrix,
Observation, Planner, target-admission and history owners remain correct.

Runtime / Production / Authority effects: `NONE / NONE / NONE`.

Validation: `git diff --check` PASS; focused RS7 lifecycle, OMP program
reconciliation and truth-check suites: `73 tests, OK`.

## Re-entry and re-audit

Targeted Fortinet or MikroTik research may run only after an existing OMP
admission names the exact missing mechanism cell, source set, output consumer
and stop condition. Re-audit consumed evidence only on source/contract drift,
an owner/consumer change, failure of the Matrix subset/target-freshness/
anti-flap/writer model, or a real ordinary failover contradiction.

Terminal: `PHASE_C_COMMERCIAL_HEALTH_BENCHMARK_CONTRACT_REGISTERED_NOT_ADMITTED`.
