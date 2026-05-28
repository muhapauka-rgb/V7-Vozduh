# E24.1 Repo Helper Source Review

Reviewed local repo helper sources before deployment.

## Source Files

- `tools/v7-second-canary-target-readiness`
  - sha256=`75607c4e56740788cb8b1e160efa539059bcf4ca29f0d8978b8b6ae2b43aff8a`
  - size=`17580`
  - shebang=`#!/usr/bin/env python3`
- `tools/v7-restore-settle-gate`
  - sha256=`eb74101dd44b0bfe8df106719602a8318ba7593149f6535f0ec0dcb9fc6dfbdc`
  - size=`17329`
  - shebang=`#!/usr/bin/env python3`

## `v7-second-canary-target-readiness`

Source semantics:

- Read-only Python helper.
- Declares `read_only=true`, `mutation=false`, `runtime_commands_executed=false`, `forbidden_commands_called=false`.
- Default state lookup checks `/opt/v7/egress/state` first.
- Supports explicit `--state-dir`.
- Parses:
  - `users.registry`
  - `egress.registry`
  - `egress-load.state`
  - `egress-stability.state` / `stability.state`
  - `egress-quality-summary.json`
  - `egress-diagnose.state`
  - `interface-state.state`
- Default candidate/user shape matches E24:
  - `candidate_user=10.7.0.11`
  - `current_egress=1`

Operational fit:

- Live-runtime based on VPS by default because `/opt/v7/egress/state` exists.
- Suitable for E24/E25 target readiness gate after deploy.

## `v7-restore-settle-gate`

Source semantics:

- Read-only Python helper.
- Declares `read_only=true`, `mutation=false`, `runtime_commands_executed=false`, `forbidden_commands_called=false`.
- Does not execute runtime commands.
- It classifies saved planner/apply observation samples.
- Supports explicit `--state-dir`.
- Default state directories are repo/evidence sample directories:
  - `docs/track7/control-plane/e11_13-evidence/restore-settle-samples`
  - `docs/track7/control-plane/e11_12-evidence/restore-settle-samples`
  - older restore evidence directories

Operational fit:

- The helper is safe to deploy.
- It is not a live sampler by itself.
- It requires current restore-settle sample evidence to produce an E25-grade GO.
- On a bare VPS without repo evidence samples, default output is expected to be NO-GO/CONDITIONAL, not authoritative live GO.

## Local Validation

- `PYTHONPYCACHEPREFIX=.pycache-e24_1 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate`: PASS
- `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate`: PASS, `19` tests.
- Local JSON smoke:
  - `tools/v7-second-canary-target-readiness --json`: JSON OK
  - `tools/v7-restore-settle-gate --json`: JSON OK

## Source Review Verdict

- Both helpers are safe to deploy as read-only governance tools.
- `v7-second-canary-target-readiness` is live-runtime usable on VPS.
- `v7-restore-settle-gate` is safe and available after deploy, but requires current settle samples for a GO verdict.
