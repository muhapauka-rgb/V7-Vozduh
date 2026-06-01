# Program F2 Truth Source Audit

Date: 2026-06-01

## Truth Sources

| Domain | Canonical Source | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Proposal | fresh `shadow.before.json` + `proposal.before.json` | `target-drift-analysis.json` | approval and certification reports |
| Approval | prompt-approved target `awg3` | stale/mismatch verdict | `PROGRAM_F2_APPROVAL_PACKET.md` |
| Movement | `v7-user-switch` after valid packet only | registry delta and route checks | operator autoswitch report |
| Rollback | original `users.before.registry` current egress | rollback preview | rollback reliability report |
| Verification | runtime checkers | captured outputs | runtime/certification reports |
| Observation | before/after/delayed/final snapshots | hashes and route checks | final report |

## Evidence Hashes

- shadow: `88c6303ab298f5d69372a6a6ae1ff110110df39f2f8edffa14055cc4fa2631d4`
- safety: `07e61c932cc19b41da6708b10f26a341ba3a2e03949989f0dea984c835b069b2`
- proposal: `e9f5fed6cad3a7399f5f040227b1f4325573ce1d296915fcf91ee33a94d89bb6`
- movement preview to approved target `awg3`: `ca147ed019332db835b106c2a8c24f80c3d08adddd65776fa149497d441d843f`
- rollback preview: `d622861fce286e83d1d7aeefc9e88af05b1b7b97c9e23df92aeda4b822f85ad2`

## Verdict

Truth sources are clean. The blocker is not ambiguity; it is freshness mismatch between approved target and fresh canonical proposal.

