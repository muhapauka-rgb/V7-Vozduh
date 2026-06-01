# Program Z2 Truth Source Audit

Date: 2026-06-01

## Verdict

truth_source_audit_complete=true

## Sources

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Proposal | `v7-autoswitch-proposal-cap` output | proposal fingerprint | Z2 reports |
| Approval | hybrid approval packet | approval/policy fingerprints | approval summary report |
| Movement | existing `v7-users-autoswitch` / `v7-user-switch` runtime authority | registry delta and route checks | execution report |
| Rollback | rollback target in approval policy | rollback compatibility validator | rollback section in reports |
| Verification | runtime registries, selected moves, safety state | runtime fingerprint and recheck verdict | runtime audit |
| Observation | audit JSONL and runtime evidence snapshots | record hash chain | final certification report |

## Z2 Canonical Runtime Inputs

- users registry
- egress registry
- selected moves state
- autoswitch safety status

## Z2 Derived Fingerprints

- proposal fingerprint: `87eacb4f30bc23f5f13236d8a6296a282e63c1d03985105d46fa05f41a629692`
- policy fingerprint: `7293744babf174e3d1fda4dc1416beddef2822493ac445edf080c4b877578fde`
- runtime fingerprint: `a35ea271f45acc2416ecf9154ccecea37f84b58f87f1abb213dca469c6b77049`

## Rule

Approval truth can authorize policy scope, but runtime truth wins at execution time. If runtime registry hashes, selected moves, safety state, target class, trust class, policy class, or rollback compatibility drift, the validator denies.

## Safety

- runtime_mutation_performed=false
- truth_source_duplication=false
- presentation_overrides_runtime=false

