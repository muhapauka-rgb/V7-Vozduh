# V5.3 N8 unattended Runtime caller and consumer cutover

Date: 2026-08-23 (MSK)  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Phase: `N8 UNATTENDED_RUNTIME_CALLER_AND_CONSUMER_CUTOVER`

## Result

`N8 = COMPLETE` for the required automatic controlled chain. A Polygon-only
interface failure was detected by the deployed `v7-health.service`; the health
owner woke the existing `v7-autoswitch-planner.service`, which consumed the
canonical Matrix event and used the existing Planner, Candidate, Packet, Lease,
Barrier, apply, route verification, Outcome and Learning owners. No manual
Planner/apply command was used.

The terminal is server-side `S11`, not remote-client `T11`: no independent
client agent exists. The final Program SLO is not claimed. This real Runtime
sample exposed a 63-second signal-to-S11 path and therefore carries an explicit
latency residual into N9.

## Discover / reuse / repairs

The deployed role loop already had automatic hard-signal wake, but confirmed
profile-service failures only ran targeted Matrix observation. They did not
wake the existing governed consumer. The previous planner invocation had also
ended in OOM and the oneshot unit had no failure restart. Target selection
additionally rejected a safe one-user `EXECUTION_ONLY` target because it used
the obsolete whole-campaign `current_stage_feasible` flag.

Minimal in-place repairs:

- `tools/v7-egress-diagnose`: after bounded repeat confirmation and successful
  targeted Matrix reception, wake the same existing governed consumer; expose
  a wake count, without planning or applying in the producer;
- `tools/runtime-support/v7-health-loop`: pass the existing systemd wake owner
  to the `other_required` role;
- `systemd/drafts/v7-autoswitch-planner.service`: restart on process failure;
- `tools/v7-users-autoswitch`: allow exactly one free slot on an already
  reserved healthy `EXECUTION_ONLY` target, independent of the superseded
  48-user campaign stage; exclude an active controlled-failure source from its
  own healthy target set;
- no new owner, timer, queue, registry, persistence or Authority surface.

Commits:

- `4cb03fdf` — automatic service-failure wake, one-user target admission and
  planner restart recovery;
- the follow-up self-target exclusion and current test-fixture reconciliation
  are committed with this report.

## Verification

Focused and owner-chain suite:

```text
160 tests passed
tests.unit.test_v7_egress_diagnose
tests.unit.test_service_failure_episode
tests.unit.test_v7_health_fast_deadline_loop
tests.unit.test_v7_sync_tools
```

Production facts before the controlled failure:

- `v7-health.service = active`;
- predecessor `v7-service-matrix-refresh.timer = disabled`;
- predecessor `v7-telegram-sentinel.timer = disabled`;
- source `vless/tun0`: eight enabled certification clients, zero ordinary
  clients;
- exact destination selected by the existing owner:
  `amneziawg-exec-20260528-10-8-1-14`;
- no broad systemd/apply command was issued by Engineering.

Controlled action and automatic consumption:

```text
Polygon failure onset: 2026-08-23T13:56:47.744316537Z
automatic planner start: 2026-08-23T13:56:48Z
user: 10.7.0.92
source: vless
target: amneziawg-exec-20260528-10-8-1-14
packet: pkt_60af187b9a6aab3e1e8b146b
lease: execlease_f8dbbda2ef0f78f7782f13b2
operation: govexec_ddbe43e8ec4ee99343a15dd0
reservation: ctm0fsample_2d4e303ef1a54663d909dcf5
S11/forward evidence: 2026-08-23T13:57:51.920660Z
outcome/learning closure: 2026-08-23T13:57:56.058223Z
```

Effects:

- `users.registry`: `10.7.0.92` changed from `vless` to the exact selected
  target;
- policy table 1090 selected the target interface;
- route lookup used `v7execwg0`;
- target-bound payload verification passed;
- Outcome = success; rollback not required; Learning consumed the outcome;
- Polygon `tun0` was restored immediately after the move;
- ordinary-user delta = 0;
- planner peak RSS approximately 323.8 MiB, versus the earlier 1.6 GiB OOM;
- systemd invocation completed successfully in 68.066 seconds.

## Measured latency and interpretation

Owner-backed forward evidence:

| Span | Result |
| --- | ---: |
| decision -> apply admission | 2,758.690 ms |
| assignment commit | 664.558 ms |
| kernel path visibility | 23.890 ms |
| target payload ready after kernel visibility | 9,471.651 ms |
| historical Matrix confirmed failure -> S11 | 406,837.452 ms |
| historical first failed observation -> S11 | 1,303,145.148 ms |

The two historical failure clocks predate this Polygon onset and are not the
new failure-injection latency. Wall-clock Polygon onset -> S11 was about 63.4
seconds. Approximately 34 seconds preceded the bound decision, and the final
payload verifier spent about 9.5 seconds, including a 4-second Telegram probe
even though the selected synthetic identity had no declared Telegram-required
profile. These are measured N9 optimization/scale inputs, not an N8 SLO pass.

`kernel_route_mutation_latency_ms` remains unavailable because the existing
low-level owner commits assignment and route coherently; this run does not
invent a false split clock. Remote device/application recovery remains
`NOT_MEASURED_NO_CLIENT_AGENT`.

## Safety and restart evidence

- canonical Matrix remains the sole health/T0 writer;
- service producer cannot create Candidate, Packet, Lease or route apply;
- consumer single-flight remains systemd plus existing Matrix/lease locks;
- duplicate active sample re-entry terminates at
  `CT_M0F_BOUNDED_SUCCESSOR_LIMIT_REACHED` after the one successful action;
- failed planner processes restart through the same unit and same consumer;
- target/source identity, current controlled scope and contract hashes are
  bound in the Packet lineage;
- Polygon failure affected certification identities only; ordinary routes and
  users did not change.

## Residual and exact next step

Next phase: `N9 FULL SCALE AND CRITICAL-PATH TOURNAMENT`.

Execute the mandatory `7/50/100/1000` egress and
`250/500/10,000+` user/profile matrix while measuring probes/sec, bytes/sec,
processes, sockets, CPU, peak RSS, endpoint pressure, Matrix writes/locks and
deadline misses. In the same measured tournament, compare the current broad
target-selection and payload verification spans with reuse of the already
prepared top-H projection and an exact role/profile-required S11 verifier.
Only measured-safe replacements may be deployed; Full remains the stale,
conflict and disagreement fallback.

