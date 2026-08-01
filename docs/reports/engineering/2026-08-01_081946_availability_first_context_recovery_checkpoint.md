# V7: recovery checkpoint availability-first campaign

Date: `2026-08-01T08:19:46+07:00`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission residual: `RECOVER_AND_CONTINUE_AVAILABILITY_FIRST_LADDER_AFTER_CONTEXT_EXHAUSTION_V1`  
Evidence class: production owner reconstruction; this report is historical evidence, not live truth.

## Summary

The prior prose statement was not reused as truth. Live production owners prove that the standing contract `sdpc_285af5fc6f4de20415c3e5b1` is active and stages `1`, `2`, `5`, and `10` are complete and consumed. Stage `25` was already active when this recovery began, so no second Matrix caller, Candidate, Packet, lease, restore barrier, or transaction was created.

The missing Outcome/Replay consumption link for target-bound trials was repaired in commit `aeccab8c922406614fc7231b51b04f3448554336` and deployed only through `tools/v7-safe-deploy` as deploy `deploy-z8-14-Updatesystem-aeccab8-20260801T080934`.

## Deploy

- safe-deploy manifest: `PASS`, blockers `[]`;
- local/GitHub commit: `aeccab8c922406614fc7231b51b04f3448554336`;
- production delta: only `/usr/local/bin/v7-governed-canary-dry-run-cycle`;
- service restart: not required;
- policy, Authority, systemd units, routing and Production Maturity: unchanged.

## Live campaign checkpoint

- campaign receipt owner: existing append-only `operator-execution-audit.jsonl`;
- completed stages: `1,2,5,10`;
- receipts: `afstage_bb5405ab5264071e8c38169b`, `afstage_9f17fda93a97572c6092d75c`, `afstage_a1411e6e4dfbfe50aa8606fd`, `afstage_74d124e8951bfaccf499067a`;
- production-proven maximum: `10`;
- first incomplete stage: `25`;
- Stage 25 owner: `v7-service-matrix-refresh.service` -> `v7-governed-canary-dry-run-cycle`;
- invocation: `01537c4091cb4fbfb1b13384a13ff13c`;
- parent PID at checkpoint: `1042303`; governed child PID: `1081950`;
- source/baseline: `vless`;
- later read-only checkpoint: the same owner process remained alive after `58:31`, with no duplicate caller; `23/48` campaign identities were on `awg3` and `25/48` remained on `vless`;
- no second transaction was started and the active transaction was not killed.

## Identity accounting

Live `users.registry` contains `52` certification identities and `73` ordinary identities. Four `polygon-l7-canary` identities belong to a different campaign and were excluded from Stage 25. The active group `t48-d27d985e237c` is owner-distinct. The initial checkpoint showed `18` identities on `awg3` and `30` on `vless`; the later checkpoint showed `23` on `awg3` and `25` on `vless`, proving forward progress by the same Matrix invocation.

The executor deliberately implements one aggregate stage as serialized fresh one-user Packet/lease operations with `max_concurrent_transactions=1`, followed by serialized baseline reset. Its existing per-member bounded verification timeout is up to `330` seconds. The elapsed runtime and a transient interval with no child process therefore do not by themselves prove a hang.

Ordinary-user involvement in the certification cohort: `NONE`.

## Exact current state

`FORWARD_IN_PROGRESS` for Stage 25.

The only legal successor is the terminal of the already-running owner process:

`ACTIVE_STAGE_25_OWNER_COMPLETES -> VERIFY_ALL_MEMBERS -> SERIAL_BASELINE_RESET -> OUTCOME_REPLAY_LEARNING -> EXACT_ONCE_STAGE_RECEIPT -> CPS_OMP_RECONCILIATION`.

Stage 48 must not start before the Stage 25 receipt is consumed.

## Impact

- product/runtime change: compact evidence consumer repair only;
- user effect caused by this recovery context: `NONE`;
- ordinary-user route/assignment delta: `0`;
- Authority expansion: `NONE`;
- Production Maturity: `NO_CHANGE`;
- L8 credit: `NONE`.

## Re-audit rule

Re-read live route, Packet, operation, reset, Outcome, Replay, Learning and campaign receipt owners after the current service reaches its own bounded terminal. Never infer Stage 25 completion from this report or from forward movement alone.
