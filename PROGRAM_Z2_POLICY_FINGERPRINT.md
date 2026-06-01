# Program Z2 Policy Fingerprint

Date: 2026-06-01

## Verdict

policy_fingerprint_working=true

## Implemented Fingerprints

Implemented by `admin_core/hybrid_approval.py`:

- proposal fingerprint
- policy fingerprint
- runtime fingerprint
- approval fingerprint

## Z2 Fingerprints

- proposal fingerprint: `87eacb4f30bc23f5f13236d8a6296a282e63c1d03985105d46fa05f41a629692`
- policy fingerprint: `7293744babf174e3d1fda4dc1416beddef2822493ac445edf080c4b877578fde`
- runtime fingerprint: `a35ea271f45acc2416ecf9154ccecea37f84b58f87f1abb213dca469c6b77049`

## Bound Fields

Policy fingerprint binds:

- approval mode
- budget
- allowed users
- route class
- target class
- trust class
- policy class
- capacity rule
- rollback target

Runtime fingerprint binds:

- users registry hash
- egress registry hash
- selected move hash
- selected move count
- safety status

Proposal fingerprint binds:

- budget
- selected user
- current egress
- recommended egress
- action
- move type
- route class

## Safety

Any mismatch in expected fingerprints denies execution.

