# PROGRAM A.2 - ELIGIBILITY RECOVERY, CANDIDATE RESTORATION AND PROGRAM A UNBLOCK ATTEMPT REPORT

Date: 2026-06-02
Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Executive Verdict

Program A.2 completed as a fail-closed candidate restoration attempt.

Safe recovery was attempted:

- service matrix recomputation;
- Telegram sentinel recomputation with `--no-autoswitch`;
- quality summary recomputation;
- load recomputation;
- planner recomputation;
- restore-settle recomputation;
- targeted raw quality probes for the nearest possible candidates.

No candidate was restored.

After recovery:

- `healthy_egress_total=0`
- `candidate_moves=0`
- `selected_moves=0`
- `execution_allowed_now=false`

Single remaining blocker:

`production_candidate_pool_exhausted_by_canonical_gates`

Exact meaning: no non-reserved production candidate satisfies the canonical planner gates. The only high-throughput target observed in raw diagnostics is still unavailable to Program A either because it is canary-reserved (`wireguard-1779454504-c43409`) or because canonical planner inputs still reject it (`vless` with `severity_SUSPECT`, low stability, and min floor failure). Converting raw probe data into eligibility by hand would be a planner/quality/governance override and is forbidden by A.2.

## Evidence

- `docs/reports/evidence/program_a2_evidence/phase1_remote_eligibility_recovery.txt`
- `docs/reports/evidence/program_a2_evidence/a2_eligibility_before_after_summary.json`
- `docs/reports/evidence/program_a2_evidence/phase2_targeted_quality_probe.txt`
- `docs/reports/evidence/program_a2_evidence/a2_final_forensics_summary.json`
- `docs/reports/evidence/program_a2_evidence/a2_remote_eligibility_recovery.sh`
- `docs/reports/evidence/program_a2_evidence/a2_remote_targeted_quality_probe.sh`

## Safety Statement

No user movement was executed.

No direct `v7-user-switch` was executed.

No route mutation, policy mutation, capacity override, planner override, governance bypass, reservation bypass, canary bypass, audit bypass, closure bypass, service restart, or systemd modification was performed.

Unlike A.1, Telegram sentinel was run with `--no-autoswitch`; it did not invoke autoswitch apply.

The final no-movement check showed unchanged registry hashes:

- users registry: `68c0318884fa6a8c5fe874b2f4249b7a63d635c832da802fffa419855bd040d3`
- egress registry: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`

## Fresh Runtime Read

Runtime host:

- `v3119922.hosted-by-vdsina.ru`

Runtime time:

- `2026-06-02T22:25:54+03:00`

Runtime linkage:

- authoritative branch: `Updatesystem`
- deploy commit: `ddc7d1cf048277e8ffa7e7ef3d6a0c85f256e7ca`
- deploy id: `deploy-z8-14-Updatesystem-ddc7d1c-20260602T154925`
- runtime identity model: copied binaries from deploy manifest

Services:

- `v7-admin-api.service`: active
- `v7-users-autoswitch.service`: inactive
- `v7-users-autoswitch.timer`: inactive
- `v7-service-matrix-refresh.timer`: active
- `v7-telegram-sentinel.timer`: active
- `v7-egress-quality-compact.timer`: active

Freshness before recovery:

- `V7_STALE_RESULT=OK`
- `v7-state.json`: fresh
- `summary.state`: fresh
- `egress-status.state`: fresh

Freshness after recovery:

- `V7_STALE_RESULT=OK`
- service matrix updated at `2026-06-02T19:27:16.840780+00:00`
- Telegram sentinel updated at `2026-06-02T19:27:16.843241+00:00`
- quality summary updated at `2026-06-02T19:27:16.974402+00:00`

## Duplication Audit

No active alternate mover was observed.

Authority map:

| Area | Owner | A.2 classification |
| --- | --- | --- |
| Planner / selected moves | `tools/v7-users-autoswitch` | Reuse only |
| Service matrix | `v7-service-matrix-refresh-all`, `v7-service-matrix-test` | Reuse for diagnostics/recompute |
| Telegram service signal | `v7-telegram-sentinel` | Reuse with `--no-autoswitch` |
| Quality summary | `v7-egress-quality-compact` | Reuse |
| Load | `v7-egress-load` | Reuse |
| Restore-settle | `v7-restore-settle-gate` | Reuse |
| Direct movement | `v7-user-switch` | Reject direct use |
| Reservation/canary status | egress registry/governance | Do not bypass |
| Policy | policy files/admin APIs | Do not mutate |

No alternate planner or alternate selected move source was accepted.

## Configured Quality Floors

Canonical floors from policy:

- `min_avg_mbps=15.0`
- `min_floor_mbps=10.0`
- `min_stability=0.45`

These floors were not changed.

## Full Candidate Matrix After Recovery

| Egress | Health | Quality | Capacity | Service Matrix | Trust / Reservation | Planner Eligibility |
| --- | --- | --- | --- | --- | --- | --- |
| `1` | `code=000`, `severity=FAIL` | avg `0`, min `0`, stability `0`, fail rate `0.9998` | load OK, users 0 | `FAIL 0/14`, Telegram DOWN | not reserved | ineligible: health, service, Telegram, avg/min floors |
| `amneziawg-exec-20260528-10-8-1-14` | `code=200`, `severity=OK` | avg `1.75`, min `0.24`, stability `0.137` | heavily loaded by execution users | `WARN 13/14`, Telegram OK | `manual_only=1`, `reserve_only=1`, `canary_reserved=true`, `production_assignment_allowed=false` | ineligible: reservation plus avg/min/stability floors |
| `awg0` | `code=200`, `severity=OK` | avg `1.14`, min `0.87`, stability `0.765` | current users 3 | `WARN 13/14`, Telegram OK | not reserved | ineligible: avg/min floors |
| `awg3` | `code=200`, `severity=OK` | avg `1.56`, min `0.96`, stability `0.614` | current users 3 | `WARN 13/14`, Telegram OK | not reserved | ineligible: avg/min floors |
| `openvpn-1779388847-d2ad7c` | `code=000`, `severity=FAIL`, interface down/missing | avg `0`, min `0`, stability `0` | load OK, users 0 | `FAIL 0/14`, Telegram DOWN | not reserved | ineligible: health, service, Telegram, avg/min floors |
| `vless` | `code=200`, `severity=SUSPECT` | avg `38.74`, min `6.82`, stability `0.176`, 1h fail rate `0.9658` | current users 4 | `WARN 12/14`, Telegram OK | not reserved | ineligible: `severity_SUSPECT`, min floor, stability floor |
| `wireguard-1779454504-c43409` | `code=200`, `severity=OK` | avg `14.17`, min `6.03`, stability `0.425` | load OK, users 0 | `WARN 13/14`, Telegram OK | `canary_reserved=true` | ineligible: canary reservation plus avg/min/stability floors |

## Quality Floor Forensics

Quality floors are realistic as safety gates for production movement, but current canonical measurements do not satisfy them for any candidate.

Near candidates:

- `awg0`: current avg/min are `1.14/0.87 Mbps`; targeted raw benchmark produced `1.53 Mbps` and timed out. This confirms real low throughput, not stale evidence.
- `awg3`: current avg/min are `1.56/0.96 Mbps`; targeted raw benchmark produced `0.73 Mbps` and timed out. This confirms real low throughput, not stale evidence.
- `vless`: current canonical avg is high enough, but min/stability fail. Targeted raw benchmark produced `99.86 Mbps`, yet canonical planner still sees `severity_SUSPECT`, `min_mbps_below_floor`, and `stability_below_floor`. This is not safely correctable inside A.2 because planner eligibility consumes canonical state/quality/severity inputs, not ad hoc benchmark proof.
- `wireguard-1779454504-c43409`: targeted raw benchmark produced `74.0 Mbps`, but canonical state is just under avg/min/stability floors and the target is canary reserved. Reservation alone is enough to keep it unavailable.

Measurements were refreshed. The remaining quality blockers are current canonical planner inputs, not stale files.

## Severity Forensics

| Egress | Severity | Generator/evidence | Freshness decision |
| --- | --- | --- | --- |
| `1` | `FAIL` | curl failed and handshake stale; Telegram DOWN | fresh enough, confirmed bad |
| `openvpn-1779388847-d2ad7c` | `FAIL` | interface down/missing; Telegram DOWN | fresh enough, confirmed bad |
| `vless` | `SUSPECT` | `v7-egress-diagnose` marks VLESS handshake unsupported even when curl succeeds | current canonical severity, not bypassed |
| `awg0` | `OK` | handshake recent | severity not blocker |
| `awg3` | `OK` | handshake recent | severity not blocker |
| `wireguard-1779454504-c43409` | `OK` | handshake recent | severity not blocker |
| `amneziawg-exec-20260528-10-8-1-14` | `OK` | handshake recent | severity not blocker |

## Service Matrix Forensics

After service matrix and Telegram refresh:

- `1`: genuine service failure, Telegram hard down.
- `openvpn-1779388847-d2ad7c`: genuine service failure, Telegram hard down.
- `awg0`, `awg3`, `amneziawg-exec-20260528-10-8-1-14`, `vless`, `wireguard-1779454504-c43409`: service matrix mostly passes or warns, so service matrix is not the sole blocker.

Service evidence is fresh.

## Reservation Impact Map

| Candidate | Reservation-only? | Impact |
| --- | --- | --- |
| `wireguard-1779454504-c43409` | No, but reservation is decisive | Even if raw benchmark is strong, canary reservation blocks production assignment. |
| `amneziawg-exec-20260528-10-8-1-14` | No, but reservation is decisive | Manual/reserve/execution-only governance blocks production assignment. |
| `awg0` | No | Not reserved; blocked by low avg/min quality. |
| `awg3` | No | Not reserved; blocked by low avg/min quality. |
| `vless` | No | Not reserved; blocked by canonical severity and quality stability/min gates. |
| `1` | No | Not reserved; blocked by health/service/Telegram/quality failure. |
| `openvpn-1779388847-d2ad7c` | No | Not reserved; blocked by interface/service/Telegram/quality failure. |

No candidate is blocked only by reservation. The strongest raw-speed target is also canary reserved, so it cannot be restored without governance bypass.

## Safe Recovery Performed

Performed:

- service matrix refresh;
- Telegram sentinel refresh with `--no-autoswitch`;
- quality compact refresh;
- egress load refresh;
- stale-state check;
- planner recompute;
- restore-settle recompute;
- targeted raw path benchmarks for `awg0`, `awg3`, `vless`, `wireguard-1779454504-c43409`.

Not performed:

- policy changes;
- reservation/canary changes;
- planner override;
- quality floor changes;
- direct route repair;
- direct movement;
- manual conversion of raw benchmark into planner truth.

## Planner Before / After

Before safe recovery:

- `healthy_egress_total=0`
- `candidate_moves=0`
- `selected_moves=0`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

After safe recovery:

- `healthy_egress_total=0`
- `candidate_moves=0`
- `selected_moves=0`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- planner generation: `c5d999f7b70b4a87ac4917ce3c213ae2312e0020416e8b2295573e1b6ac246ab`

Restore barrier after recovery:

- enabled: `true`
- clearance expired: `true`
- clearance expected selected moves: `1`
- selected moves before guard: `0`
- current selected move hash: empty selected-move hash

Restore barrier remains invalid, but it is not hiding a candidate.

## Execution Readiness Attempt

Candidate does not exist, so Program A execution readiness cannot be certified.

Restore-settle after recovery:

- `gate_status=CONDITIONAL`
- `execution_allowed_now=false`
- reasons:
  - `sample_count_below_required:1<3`
  - `apply_timer_intervals_below_required:0.00<2`

Because there is no candidate, no governance clearance should be regenerated yet.

## Root Cause Decision

Primary root cause:

`production_candidate_pool_exhausted_by_canonical_gates`

Secondary root causes:

- nonreserved AWG candidates are currently too slow for production movement (`awg0`, `awg3`);
- `vless` has strong raw throughput but fails canonical planner severity/quality inputs;
- `wireguard-1779454504-c43409` has strong raw throughput but is canary reserved and still slightly below canonical quality floors;
- `1` and `openvpn-1779388847-d2ad7c` are genuine health/service/Telegram failures;
- restore barrier clearance is expired and generation/hash mismatched, but no selected move exists behind it.

Safe correction status:

- Stale evidence was refreshed.
- Missing measurements were probed.
- No safe candidate restoration path remains without changing policy, reservation, planner semantics, or canonical quality state.

## Final Verdicts

all_theories_tested=true
healthy_candidates_exist=false
planner_candidate_exists=false
quality_evidence_fresh=true
service_matrix_fresh=true
governance_evidence_fresh=true
safe_recovery_performed=true
candidate_restored=false
selected_moves_present=false
execution_readiness_possible=false
safe_to_retry_PROGRAM_A=false

## Conclusion

Program A.2 did not restore a candidate. The exact remaining blocker is not "candidate absent" in the abstract; it is that every available production target fails at least one canonical gate after safe refresh. The only raw-fast paths cannot be accepted safely: `wireguard-1779454504-c43409` is canary reserved, and `vless` is rejected by canonical severity and quality stability/min inputs. Program A must not be retried until a nonreserved production egress satisfies the configured quality floors and canonical planner eligibility without override.
