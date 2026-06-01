# P6.A User Candidate Review

Project: V7 Vozduh

Block: P6.A

## Selected Candidate

- user candidate: `10.7.0.11`
- current egress: `1`
- route table: `1009`
- enabled: true
- blast radius: one user
- rollback target: `1`

## Why This User

`10.7.0.11` is the safest first movement design candidate because:

- it is enabled in the live users registry;
- it is currently on rollback target `1`;
- it has a dedicated route table, `1009`;
- it is the default candidate in existing canary/readiness tooling;
- historical governed movement evidence already used and rolled back this user cleanly;
- route movement preview for `10.7.0.11 -> amneziawg-exec-20260528-10-8-1-14` has no errors;
- rollback preview to `1` is structurally simple.

## Why Not Others

- Disabled users are excluded.
- Users currently on `awg0`, `awg3`, or `vless` are excluded because their rollback/current state is not the calm baseline `1`.
- `10.7.0.12`, `10.7.0.14`, and `10.7.0.15` are viable later cohort candidates, but P6.A needs exactly one user.
- `10.0.0.*` users are excluded because prior autoswitch safety history is noisier and they are not the existing first-candidate path.

## Observability

Candidate observation should track:

- users registry row diff
- `user-10.7.0.11.assign`
- route table `1009`
- `ip rule` for `10.7.0.11`
- checker outputs
- switch-history/audit append

## Verdict

- user_candidate_defined=true
- candidate_user=10.7.0.11
- low_blast_radius=true
- rollback_available=true
