# Block E Truth Source Audit

Date: 2026-06-01

## Truth Source Map

| Domain | Canonical Source | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Proposal | `v7-users-autoswitch` shadow JSON plus `v7-autoswitch-proposal-cap` output | proposal hash and bounded move list | `BLOCK_E_OPERATOR_PROPOSAL.md` |
| Approval | Explicit operator response to exact proposal | approval packet text | final chat / future approval artifact |
| Movement | Runtime `v7-user-switch` or approved bounded autoswitch apply path | switch history, registry hash delta | execution report after approval |
| Rollback | Previous egress from `users.registry` and movement preview | `rollback-preview.json` | `BLOCK_E_OPERATOR_PROPOSAL.md` |
| Verification | `v7-killswitch-check`, `v7-user-route-check`, `v7-runtime-contract-validate` | captured outputs in `/private/tmp/v7-block-e` | runtime/operator certification reports |
| Observation | before/after/delayed/final runtime snapshots | registry hashes, route checks, observability summaries | observation/certification reports |

## Current Proposal Truth

- canonical shadow hash: `055f01ce8c5dceab6d2e3609da8da03f865121c433a47d18ef2dc4e77257d6f7`
- safety hash: `daafdf0fa6f1e1e6f0cb0d4ef83c59f5a4078b0bc4a6604826bed188599cb0b5`
- proposal hash: `5f0ab38b601cd1215589b1c008a365af53f49d466d16b543692d3d16ec2f4634`
- move preview hash: `943f1356f1c1777464637600e43192404917344dfdc89ccc44e1fd8d3264bdde`
- rollback preview hash: `d622861fce286e83d1d7aeefc9e88af05b1b7b97c9e23df92aeda4b822f85ad2`

## Verdict

truth_sources_clean=true

