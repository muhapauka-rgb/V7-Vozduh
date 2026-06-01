# Program Z2 Runtime Audit

Date: 2026-06-01

## Verdict

runtime_audit_complete=true

## Live Runtime Availability

The live runtime directory `/opt/v7/egress/state` is not mounted in this workspace. Live movement was therefore not attempted.

## Repository Evidence Runtime

Latest repository evidence from `docs/track7/productization/e30-evidence`:

- users registry hash: `f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042`
- egress registry hash: `0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689`
- readiness hash: `0123a1b71338d36b2e80e3fc90c1060512461e9b15081ef05bbe90716adba6f8`
- readiness status: `GO`
- selected target: `amneziawg-exec-20260528-10-8-1-14`
- target mode: `execution_only_mode=true`
- runtime commands executed: `false`

## Z2 Fixture Runtime Recheck

Z2 local recheck:

- verdict: `ALLOW_HYBRID_BOUNDED_AUTONOMY`
- safety status: `ok`
- selected move count: `0`
- target descriptor:
  - egress: `awg3`
  - route class: `GLOBAL_STABLE`
  - trust class: `RU_SENSITIVE_EXCLUDED`
  - policy class: `AUTOSWITCH_ALLOWED`
  - capacity class: `EMPTY`

## Runtime Hashes

- users registry hash: `bb7e9c250471aa3229d9d07a94be1884ac957490855d8f4fbd91f2f338c2bb5d`
- egress registry hash: `b751b93d8f901b13b43cf9954bea723b28667f3c8a780676192278840bef2aab`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime fingerprint: `a35ea271f45acc2416ecf9154ccecea37f84b58f87f1abb213dca469c6b77049`

## Safety

- runtime_mutation_performed=false
- routing_changed=false
- users_moved=false
- autoswitch_apply_run=false

