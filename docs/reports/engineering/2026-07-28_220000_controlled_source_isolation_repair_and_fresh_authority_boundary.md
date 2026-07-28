# Engineering Report: Controlled Source Isolation Repair

Date: `2026-07-28`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: existing `T48-M8` reconciliation

## Result

The exact Authority decision for request
`cpsauth_r1_7b3cf7eab9af58a7a3839aaa` was recorded and consumed. Before any
substrate write, production revalidation proved that its hash-bound source
`wireguard-1779454504-c43409` contains enabled non-certification users.
Deliberate failure on that source would involve ordinary customers and is
therefore forbidden by the approved scope.

No identity was created, no user was classified or assigned, no controlled
condition was activated, and no campaign stage was executed.

## Root cause and repair

The existing certification-pool projection counted certification identities
but did not require source isolation. This could publish a false readiness or
incremental-pool successor for a mixed production source.

The existing owners were extended to:

- count enabled certification and non-certification assignments separately;
- require zero enabled non-certification users for controlled-failure
  readiness;
- expose compact isolation status without storing raw identity lists;
- fail closed when an approved request is bound to a mixed source;
- reuse an already-existing empty eligible source candidate for a fresh exact
  Authority request.

Commit `d4a8dffaafab206b1cc5d21e5cc74a5273083431` was pushed and deployed only
through `tools/v7-safe-deploy`. Production runtime linkage is
`deploy-z8-14-Updatesystem-d4a8dff-20260728T215438`.

## Production verification

The non-test production status caller proved:

- mixed controlled sources: `1`;
- maximum certification users on an isolated active controlled source: `0`;
- exact blocker:
  `active_controlled_source_contains_non_certification_users`;
- one existing empty isolated source candidate: `1`;
- prior approved request source isolation: `STOP_SAFE`.

Forbidden effects remained absent:

- policy or contract write;
- identity creation;
- classification or assignment;
- Candidate, Packet or lease creation;
- controlled-source mutation;
- routing mutation or user movement;
- rollback apply;
- Authority expansion;
- Production Maturity change.

## Fresh exact boundary

The same existing Authority request producer registered:

- request ID: `cpsauth_r1_d27d985e237c9582656b26e7`;
- request hash:
  `d27d985e237c9582656b26e75e36a1dd3ef9a602cd8e87f7a793033d8e97cc5c`;
- source: existing empty isolated candidate `1`;
- campaign stages: `5 -> 10 -> 25 -> 48`;
- max concurrent transactions: `1`;
- ordinary-customer involvement: `false`;
- expiry: `2026-07-29T14:55:54.838313+00:00`.

Exact legal terminal:

`ENGINEERING_AUTHORITY_CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_READY`

Re-entry requires one independent exact
`APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN` or `DECLINE` for the
fresh request ID/hash and all four named subscopes. The previous approval is
not reusable for this different source identity.
