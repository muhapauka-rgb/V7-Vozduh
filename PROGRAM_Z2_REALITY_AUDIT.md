# Program Z2 Reality Audit

Date: 2026-06-01

## Verdict

reality_audit_complete=true

## Scope Collected

- users registry: latest repository evidence `docs/track7/productization/e30-evidence/users.registry.snapshot`
- egress registry: latest repository evidence `docs/track7/productization/e30-evidence/egress.registry.snapshot`
- selected moves: Z2 fixture selected moves missing, interpreted as empty
- runtime snapshot: latest repository evidence and Z2 local fixture
- health/capacity/trust: `docs/track7/productization/e30-evidence/readiness.json`
- proposal packet: `docs/track7/productization/z2-evidence/bounded-proposal.json`
- rollback packet: policy rollback target `vless` for user `10.7.0.16`

## Latest Repository Evidence

- `users.registry.snapshot` hash: `f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042`
- `egress.registry.snapshot` hash: `0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689`
- `readiness.json` hash: `0123a1b71338d36b2e80e3fc90c1060512461e9b15081ef05bbe90716adba6f8`
- readiness approval status: `GO`
- readiness candidate: `10.7.0.11`
- readiness selected target: `amneziawg-exec-20260528-10-8-1-14`
- readiness execution-only mode: `true`
- readiness runtime commands executed: `false`
- readiness mutation: `false`

## Z2 Certification Fixture

The Z2 fixture is intentionally local and non-production:

- state directory: `docs/track7/productization/z2-evidence/state`
- candidate: `10.7.0.16`
- current egress: `vless`
- policy target: `awg3`
- budget: `1`
- rollback target: `vless`
- safety status: `ok`

Fixture hashes:

- users registry hash: `bb7e9c250471aa3229d9d07a94be1884ac957490855d8f4fbd91f2f338c2bb5d`
- egress registry hash: `b751b93d8f901b13b43cf9954bea723b28667f3c8a780676192278840bef2aab`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

## Runtime Availability

The live path `/opt/v7/egress/state` is not present in this workspace. Therefore Program Z2 did not run live user movement and did not call `v7-user-switch` or `v7-users-autoswitch --apply`.

## Safety

- runtime_mutation_performed=false
- autoswitch_apply_run=false
- routing_changed=false
- users_moved=false
- deploy_performed=false

