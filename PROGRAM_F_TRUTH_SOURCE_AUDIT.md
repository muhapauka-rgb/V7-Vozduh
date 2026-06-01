# Program F Truth Source Audit

Date: 2026-06-01

## Truth Source Map

| Domain | Canonical Source | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Proposal | `shadow.json` + `proposal-cap.json` | proposal hash, candidate list | `PROGRAM_F_OPERATOR_AUTOSWITCH.md` |
| Approval | explicit operator-approved packet | none present | final report stop verdict |
| Movement | `v7-user-switch` only after approval | registry delta, switch history | execution report after approval |
| Rollback | original `users.registry` current egress | `rollback-preview.json` | rollback reliability report |
| Verification | runtime checkers | captured checker output | audit/certification reports |
| Observation | before/after/delayed/final snapshots | registry hashes, route checks | observation sections |

## Evidence Hashes

- shadow: `b223cae7e88447b3a101c272831ef304021d5ad5f3a3c94435bb15fb7ad7ef63`
- safety: `0fae09a5512797934f04df782b3efa959837bbb05b4bb46f7dd677f18c046113`
- proposal: `33f9e7b4ea1d74fc6064fa10450674d23b243e89204f688ace625bf2d10b2e91`
- movement preview: `c13a0281721544fdf62c1e53d1220552dc8b9374806f166e3cc3e4a6f4e72ca2`
- rollback preview: `d622861fce286e83d1d7aeefc9e88af05b1b7b97c9e23df92aeda4b822f85ad2`

## Verdict

Truth sources are clear, but approval truth is missing.

