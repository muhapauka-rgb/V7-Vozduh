# V7 Phase 2 - Runtime Verification Before Enable

## Purpose

Enable is a guarded transition. It makes an egress eligible for future routing decisions, but it must not migrate users by itself.

## Required Gates

Before enable:

- registry row exists;
- registry row is disabled;
- runtime profile exists;
- interface/proxy model is known;
- dependency checks passed;
- preflight passed;
- runtime test passed;
- quarantine passed;
- service matrix passed for intended role;
- duplicate conflicts resolved;
- kill switch compatibility verified;
- no conflicting subnet or interface;
- no route-table ambiguity;
- health minimum passed.

## Readiness Blockers

Block enable when:

- runtime profile missing;
- enabled flag already mismatches lifecycle metadata;
- interface name invalid;
- profile path differs from expected target;
- dependency missing;
- quarantine not passed;
- service matrix not passed;
- egress registry row is corrupt;
- kill switch check failed;
- direct/RU safety cannot be proven.

## Post-Enable Validation

After enable:

- registry says `enabled=1`;
- runtime readiness remains OK;
- users were not moved by enable action;
- routes were not changed by enable action;
- kill switch was not bypassed;
- operator sees next safe actions.

## Safe Next Actions

Allowed after enable:

- run service matrix;
- manually switch one test user;
- run rebalance dry-run;
- watch health history before broader assignment.

Forbidden after enable:

- automatic mass user migration;
- autoswitch participation before health evidence is available;
- direct/RU policy bypass.
