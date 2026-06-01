# Program Z1.5 Fingerprint Model

Date: 2026-06-01

## Approval Fingerprint

Must include:

- schema version
- approval mode: `TARGET` or `POLICY`
- approved user or candidate class
- budget
- route class
- service scope
- target egress for target approval, or target class for policy approval
- rollback contract
- TTL
- policy hash
- org policy hash
- proposal generation ID
- proposal fingerprint
- runtime fingerprint at approval time

## Runtime Fingerprint

Must include:

- `users.registry` hash
- `egress.registry` hash
- approved user row hash
- policy hash
- org policy hash
- safety state hash or safety status timestamp
- service matrix hash
- telegram sentinel hash
- quality summary hash
- selected moves hash

## Proposal Fingerprint

Must include:

- candidate user
- current egress
- recommended target or target class
- route class
- move type
- score
- reason list
- eligible target set
- held candidates
- budget
- proposal cap version

## Match Rules

Target approval:

- exact candidate and target must match.

Policy approval:

- exact candidate must match unless candidate-class approval is explicit.
- target may change only if substitution rules pass.
- target class, trust class, route class, budget, rollback, policy hash, and safety status must match.

## Verdict

fingerprint_model_defined=true

