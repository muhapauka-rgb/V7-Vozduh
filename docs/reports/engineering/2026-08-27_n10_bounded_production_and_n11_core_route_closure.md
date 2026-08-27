# N10 bounded production and N11 Core-route closure — 2026-08-27

## Scope and outcome

This block continued the existing `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`; it did not create a Matrix, Planner, route writer, state source or Authority owner.

The Runtime is coherent after the work: Core-primary verifies `125/125` user memberships and `4/4` classes; `v7-user-route-check` passes; `legacy_primary_rules_present=false`; `v7-health.service` is active; the standalone Matrix and Telegram timers are inactive as intended.

`N10_BOUNDED_PRODUCTION` is **not newly credited by this block**.  A full four-member move completed the governed route and Core-primary chain, but it happened before the N10 cohort path recorded the required service/path S11.  The missing S11 was implemented and deployed.  The immediately next fresh cohort was safely denied before movement because only two of the four exact current members remained at Packet materialization.  It cannot be substituted or counted.

Current lawful frontier: `N10_LAWFUL_CURRENT_COHORT_BOUNDARY`.  Re-entry requires a fresh Matrix-backed exact 2–4 member cohort that remains exact through Packet materialization; the existing Authority owner then issues a new one-use contract.  No historical cohort, failed transaction or expired contract is reusable.

## Root causes found and closed

1. A bounded cohort could reach its Core-primary map commit even where the move would alter a non-member routing class.  `c8afcc9a` adds an existing-owner read-only admissibility preflight before one-use Authority consumption.
2. The installed nft parser did not support the former map-update grammar.  `f9447434`, `5f1328bf`, and `6cf988f7` reconcile the command to a single transactional delete/add batch.  A live no-assignment owner validation returned `CORE_PRIMARY_COHORT_COMMIT_PASS` and whole-system verification passed.
3. Broad N10 planning/verification could let the diagnostic `v7-state.json` overlay an older routing assignment onto `users.registry`.  `6a27f9fd` makes the canonical registry win for routing fields and retires only the exact cohort's temporary per-user Core-primary rules after its map commit.
4. The Core-primary N10 cohort path omitted its required service/path S11.  `684c7c39` makes that existing Matrix verification mandatory for every member; failure triggers the existing rollback path and cannot be classified as success.

## Evidence

Focused tests after each material repair: `345` passed.

Safe deployment and truth gates passed for all deployed commits:

- `c8afcc9a` — Core-primary cohort admissibility preflight.
- `f9447434` — successful preflight exit status.
- `5f1328bf` and `6cf988f7` — supported atomic nft map update.
- `6a27f9fd` — canonical registry precedence and cohort legacy-route retirement.
- `684c7c39` — mandatory N10 service/path S11.

The valid governed route/Core-primary transition was operation `runtime_autoswitch_21765ec91c8303883674b2ea`: four exact members, one Planner-selected target `awg3`, four successful route checks, one Core-primary affected-scope commit, and whole-system map verification.  It is retained as routing evidence only, not N10 S11 credit.

The next current request (`accauth_r1_65e4183eb87b51dc57533c8a`) was rejected before route mutation: at packet materialization the exact four-member subject had drifted to two selected members.  Its one-use contract was not consumed; no residual contract remains current.

## N11 replacement-closure audit

| Surface | Result | Disposition |
| --- | --- | --- |
| Core-primary maps and broad verifier | Core owner exact; `125/125`, `4/4`, whole-system PASS | Retain as current owner/consumer. |
| Per-user primary rules | Four residual rules removed by one existing `v7-routing-sync --core-primary-apply` closure; no user assignment changed | Retired from Runtime; fallback implementation remains only for Core-primary inactive recovery. |
| `v7-user-route-check` | Existing broad consumer is Core-primary aware and passes | Retain; it is not obsolete. |
| Standalone Matrix/Telegram timers | inactive | Retain disabled lifecycle artifacts until their installer/recovery consumers are fully replaced; no blind deletion. |
| `v7-state.json` routing projection | diagnostic data remains useful to non-routing consumers; it no longer overrides registry routing fields | Retain; no duplicate routing truth remains. |
| Append-only execution/closure ledgers | active outcome/audit consumers still read them | Retain; history is not a duplicate current-state source. |
| Legacy Core-primary fallback | `legacy_sync` remains the explicit recovery fallback, not the active path | Retain by Program safety law. |

## Runtime effect

No manual route command or direct state-file edit was used.  All route changes and cleanup passed through the existing route/Core-primary owners.  The final N11 cleanup removed four stale per-user primary rules and routes, did not change registry assignments, and left all users covered by verified Core-primary class routing.

## Exact next action

Do not manufacture an ordinary cohort.  On a fresh Matrix generation, ask the existing N10 authority-request adapter for a 2–4 member current cohort.  Only if the exact subject survives the Packet/Lease/Barrier and the Core-primary admissibility preflight may the existing owner run the mandatory route + Core commit + service/path S11 sequence.
