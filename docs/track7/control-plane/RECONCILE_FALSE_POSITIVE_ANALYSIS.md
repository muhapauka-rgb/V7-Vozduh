# Reconcile False-Positive Analysis

## Current Finding

`v7-reconcile-check` can report missing ip rules even when stable `ip -4 rule show` snapshots contain the expected rules. A targeted grep for a reported missing rule also succeeded.

This makes the current FAIL partially false-positive or race-sensitive.

## Conditions Where FAIL May Be Operationally Safe

FAIL may be safe enough for one-user canary consideration only when all are true:

- stable pre/post `ip -4 rule show` contains the candidate rule;
- candidate route table default points to expected egress;
- `ip route get` from candidate IP uses expected egress;
- `v7-user-route-check` is OK;
- `v7-killswitch-check` is OK;
- `v7-provisioning-reconcile-check` is OK;
- autoswitch authority is held so the state is not moving during audit;
- failure is limited to checker semantics and not actual missing runtime state.

## Conditions Where FAIL Is Definitely Dangerous

FAIL is dangerous when:

- stable `ip -4 rule show` lacks the candidate source rule;
- candidate table lacks default route;
- route-get uses public interface or wrong egress;
- kill switch check fails;
- provisioning reconcile fails;
- registry and assignment files disagree;
- autoswitch/routing-sync is concurrently mutating users;
- the candidate is not isolated to one table/user.

## Checker Semantics

Current checker behavior is conservative but can overstate operational risk. It has only OK/FAIL, so it cannot distinguish:

- rule absent in stable runtime;
- transient rule rewrite/race;
- parser/color/output mismatch;
- route reality OK but strict rule text check failed.

Recommended future semantics:

```text
OK: stable rules/tables/routes all match
WARN/DEGRADED: rule text check failed but route reality and pre/post stable snapshots pass
FAIL: stable runtime state missing required rule/table/route or leak risk detected
```

## Current Verdict

The current reconcile FAIL is not proven dangerous, but it is not clean enough for canary. It remains a NO-GO blocker until reproduced under an autoswitch hold or reclassified with stronger read-only evidence.
