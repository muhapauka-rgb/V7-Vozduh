# P6.A Channel Candidate Review

Project: V7 Vozduh

Block: P6.A

## Selected Destination

- destination channel: `amneziawg-exec-20260528-10-8-1-14`
- interface: `v7execwg0`
- role: `EXECUTION_ONLY`
- current users: `0`
- manual_only: `1`
- reserve_only: `1`
- execution_reserved: true
- autoswitch_allowed: false
- rebalance_allowed: false
- production_assignment_allowed: false
- reservation_owner: `operator_execution_governance`

## Readiness

Read-only target readiness result:

- candidate_user: `10.7.0.11`
- candidate_still_valid: true
- current_egress: `1`
- execution_only_mode: true
- selected_target: `amneziawg-exec-20260528-10-8-1-14`
- approval_status: `GO`
- second_canary_readiness: `GO`
- runtime_commands_executed: false
- execution_allowed_now: false

## Why This Channel

This channel is the safest destination for the first movement design because:

- it is zero-user now;
- it is isolated from autoswitch and rebalance;
- it is explicitly reserved for operator execution governance;
- it has a known interface, `v7execwg0`;
- route movement preview is precise: table `1009` would change to `v7execwg0`;
- rollback target `1` is known.

## Why Not Other Channels

- `1`: current source, so forward movement would be a no-op.
- `awg0`: occupied by users and missing Direct/RU and Trusted RU sensitive exclusions in readiness output.
- `awg3`: occupied by users and missing Direct/RU and Trusted RU sensitive exclusions in readiness output.
- `vless`: occupied by users, readiness output marks it NO-GO/SUSPECT.
- `openvpn-1779388847-d2ad7c`: zero-user but readiness output marks it NO-GO/SUSPECT.
- `wireguard-1779454504-c43409`: GO and zero-user, but reserved as a second-canary target rather than operator execution governance; keep it as secondary fallback, not first P6.A design target.

## Verdict

- channel_candidate_defined=true
- destination_channel=amneziawg-exec-20260528-10-8-1-14
- destination_zero_user=true
- destination_readiness_go=true
