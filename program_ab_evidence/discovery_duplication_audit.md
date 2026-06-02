# PROGRAM A.B Discovery And Duplication Audit

Scope: local repository, branch `Updatesystem`, workspace `/Users/ponch/Documents/New project`.

Initial read-only truth check:

- Command: `tools/v7-truth-check --all`
- Result after read-only network/runtime access: PASS
- Local, GitHub, runtime, and state were fully aligned before A.B code edits.

## Component Classification

| Component | Location | Classification | Decision |
|---|---|---|---|
| Runtime planner | `tools/v7-users-autoswitch` | AUTHORITATIVE | EXTEND |
| Service matrix | `tools/v7-service-matrix-test`, `service-matrix.json` | EXISTING TRUTH SOURCE | REUSE |
| Telegram sentinel | `tools/v7-telegram-sentinel`, `telegram-sentinel.json` | EXISTING SERVICE SIGNAL | REUSE |
| Route-class fitness | `service-matrix.json`, `tools/v7-users-autoswitch` | EXISTING ROUTING SIGNAL | REUSE |
| Admin route scoring | `admin/v7-admin-api` | READ/PREVIEW SURFACE | DO NOT TOUCH |
| Quality summary | `egress-quality-summary.json` | SUPPORTING QUALITY HISTORY | REUSE |
| Reservation gates | `tools/v7-users-autoswitch` | SAFETY/GOVERNANCE GATE | DO NOT WEAKEN |
| Manual/reserve gates | `tools/v7-users-autoswitch` | SAFETY/GOVERNANCE GATE | DO NOT WEAKEN |
| Relative improvement | `_beats_current` in `tools/v7-users-autoswitch` | MIGRATION THRESHOLD | PRESERVE |
| Sticky/anti-flap | safety/cooldown/pair reversal logic | SAFETY GATE | PRESERVE |

## Duplicate Logic Findings

Existing service logic already exists and was reused:

- Telegram service status and hard/soft states.
- YouTube, Instagram, ChatGPT service catalog entries.
- Service matrix scoring and route-class fitness.
- Required services path through service preferences and policy.
- Runtime planner candidate scoring.

The remediation did not create:

- a second planner;
- a second service matrix;
- a second truth source;
- a second execution path.

## Main Semantic Drift

Before A.B:

- Quality floors were hard eligibility gates before scoring.
- `SUSPECT` severity was untyped and hard-blocked.
- Service matrix data contributed to scoring and service gates, but could not rescue a protocol-limited candidate from early quality/severity disappearance.

After A.B local implementation:

- Hard safety/governance gates stay hard.
- `SUSPECT` is typed.
- `handshake_unsupported_for_protocol_vless` becomes `protocol_diagnostic_limited_suspect`.
- Service suitability is computed as 0-100 service evidence, not Mbps.
- Quality floors become contextual only for protocol-limited candidates with supporting service and one-hour quality evidence.

