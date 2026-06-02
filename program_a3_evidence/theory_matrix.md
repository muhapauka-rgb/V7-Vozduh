# PROGRAM A.3 Theory Matrix

## Theory 1: Current Policy Is Correct And Channels Are Genuinely Unusable

Partially true.

`1`, `openvpn-1779388847-d2ad7c`, `awg0`, and `awg3` are genuinely unusable or too weak under both canonical and shadow safety analysis. `wireguard-1779454504-c43409` is not usable for production assignment because reservation blocks it. `vless` is not proven unusable; it has high raw throughput and strong one-hour average/minimum data.

Verdict: not sufficient to explain all starvation.

## Theory 2: Quality Floors Are Used As Eligibility Floors When They Should Be Migration Thresholds

True for current implementation.

`tools/v7-users-autoswitch:1407-1417` blocks candidates before score/migration comparison. This makes floors hard eligibility gates, not only migration thresholds.

Verdict: proven.

## Theory 3: Min/Avg/Stability Floors Are Too Aggressive

Partially true.

The floors correctly eliminate `awg0` and `awg3`; their raw probes also fail. For `vless`, the current canonical `min_mbps` and instant stability fail while one-hour minimum and raw benchmark are strong. That suggests the problem is not just numeric aggressiveness; it is window/measurement semantics.

Verdict: true for `vless` semantics, false for weak AWG candidates.

## Theory 4: Severity Model Is Too Aggressive

True for VLESS.

`vless` is blocked by `severity_SUSPECT`, but diagnosis says `handshake_unsupported_for_protocol_vless`. That is a protocol-specific checker limitation, not direct proof of runtime failure, especially when Telegram/service state and raw benchmark are usable.

Verdict: proven for typed VLESS diagnostic.

## Theory 5: Canary Reservation Blocks The Only Viable Candidate

False as "only".

Reservation correctly blocks `wireguard-1779454504-c43409`. However `vless` becomes viable under conservative typed-severity and evidence-backed quality semantics without reservation bypass.

Verdict: reservation blocks one strong candidate, not the only possible candidate.

## Theory 6: Multiple Gates Combine Into Candidate Starvation

True.

Current starvation is caused by a gate combination:

- quality floors eliminate `awg0`, `awg3`, `wireguard`, and `vless`;
- severity eliminates `vless`;
- reservation eliminates `wireguard` and execution-only target;
- service/health eliminates `1` and OpenVPN;
- manual/reserve metadata eliminates execution-only target.

Verdict: proven.

## Theory 7: Planner Correct But Policy Wrong

True in execution behavior.

The planner faithfully executes the configured gates. The questionable part is policy semantics for `vless`: typed diagnostic limitation and evidence-backed quality are not represented.

Verdict: planner behavior correct; policy semantics need redesign.

## Theory 8: Policy Correct But Measurements Misleading

Partially true.

Measurements are misleading for `vless` because canonical instant `min/stability` conflict with one-hour min and raw probe. Measurements are not misleading for `awg0`/`awg3`: canonical and raw evidence both show weak channels.

Verdict: true only for VLESS measurement interpretation.

## Additional Theory 9: Admin Surface And Runtime Planner Use Different Severity Semantics

True.

Runtime autoswitch hard-blocks severity outside `OK/WARN`; admin route candidate scoring penalizes non-OK/WARN severity. This does not create a duplicate execution path, but it can create operator confusion.

Verdict: semantic drift risk.

