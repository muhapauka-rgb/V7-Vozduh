# P1.A Final Model Decision

evidence_bundle_system_defined=true

## Decision

Evidence Bundle System is the first implementation package after architecture mapping.

It becomes the shared proof substrate for:

- checks;
- logs;
- proposals;
- user and channel diagnostics;
- route decisions;
- release verification;
- recovery verification;
- operator runbooks.

## Model Summary

Evidence is modeled as an object-linked bundle with:

- stable bundle id;
- primary object and related objects;
- status and severity;
- summary and diagnosis;
- timeline;
- evidence items;
- recommendation;
- verification state;
- closure state.

## Admin Decision

Evidence appears through existing admin surfaces and drawers. No new top-level navigation is created.

## Runtime Decision

Evidence is not runtime authority and cannot mutate runtime. It informs operator decisions and future admission surfaces.

## Storage/API Decision

P0 requires:

- Evidence Bundle Store;
- Evidence API;
- object linkage index;
- shared Evidence Drawer;
- redaction and advanced-detail rules.

## Recommended Next Block

recommended_next_block=P1.B_PROPOSAL_SYSTEM

