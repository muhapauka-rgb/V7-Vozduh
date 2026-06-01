# Program Z1 Truth Source Audit

Date: 2026-06-01

## Truth Source Map

| Domain | Canonical Source | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Proposal | `shadow.before.json` and `proposal.before.json` | `precheck-summary.json`, `target-drift-analysis.json` | Program Z1 reports |
| Approval | prompt-approved movement | stale packet verdict | drift handling report |
| Movement | `v7-user-switch` after fresh exact approval | registry and route deltas | execution report |
| Rollback | current egress from `users.before.registry` | rollback preview | rollback report |
| Verification | runtime checkers | captured checker outputs | certification report |
| Observation | before/after/delayed/final snapshots | hashes and route checks | final report |

## Evidence Hashes

- shadow: `169fdc9429ff3aea281b7d1c4122d8e29740a9e03420af27dad7a7aca8c9870e`
- safety: `1db85f86606854cbf8f83bc65d5356f82372717324a0f5567d09ecfcd2bafff0`
- proposal: `7611f8984031bd77a15f6728dd555c4c8116fc07c5d6779b70541c769d7559ca`
- approved movement preview: `2f69bfaf8b43528e12ff2b48a7e2b8f10e791970b4e55d87deb2374e0c631e6c`
- rollback preview: `d622861fce286e83d1d7aeefc9e88af05b1b7b97c9e23df92aeda4b822f85ad2`

## Verdict

Truth sources are clean. Fresh planner truth invalidated the stale prompt-approved packet.

