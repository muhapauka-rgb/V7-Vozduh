# V7 Vozduh Block E4 Report

## Reconcile Truth & Routing Integrity Audit

Block E4 collected read-only routing evidence and formalized the reconcile truth model. No routing-sync, user-switch, autoswitch apply, reconcile repair, route mutation, ip rule mutation, nft mutation, kill switch mutation, restart, deploy, chmod/chown, cleanup, or live canary was performed.

## 1. Real Cause Of Reconcile FAIL

The FAIL is not explained by stable missing ip rules. Stable `ip -4 rule show` snapshots before and after reconcile contained the expected enabled-user rules. A targeted shell grep for a reported missing rule returned `grep_rc=0`.

The likely cause is a checker semantic/race false-positive under active control-plane conditions. Autoswitch authority is active, and registry state moved since Block E2.

## 2. Dangerous Or False-Positive?

Partially false-positive is likely:

```text
stable rules present: yes
route tables present: yes
route-get checks OK: yes
kill switch OK: yes
provisioning reconcile OK: yes
v7-reconcile-check FAIL: yes
```

It is not proven dangerous at the datapath level, but it is still operationally dangerous as a canary precondition because the control plane is not quiet and the checker cannot distinguish race/semantic mismatch from real missing rules.

## 3. Current Routing Integrity Status

```text
route_table_integrity=OK_AT_SNAPSHOT
duplicate_enabled_tables=none observed
missing_enabled_tables=none observed
invalid_table_ids=none observed
enabled_users_current=vless
expected_interface=tun0
```

## 4. Current IP Rule Integrity Status

```text
ip_rule_integrity=OK_AT_STABLE_SNAPSHOT
enabled_user_rules_present=true
disabled_user_rule_1005_absent=true
duplicate_user_rules=none observed
```

## 5. Current Datapath Reality Status

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Datapath appears operational at snapshot.

## 6. Current Leak Risk

No leak evidence was observed. Kill switch direct leak drop, direct fwmark rule, reverse routes, NAT, MSS clamp, and user route checks were OK.

## 7. Kill Switch Dependency Risk

Kill switch is OK at snapshot, but it does not prove intended path correctness by itself. Canary still needs candidate table/rule/route verification immediately before and after execution.

## 8. Canary Decision

```text
NO-GO
```

Routing integrity is better than the raw reconcile FAIL suggested, but canary cannot proceed until autoswitch authority is held and reconcile false-positive/race is proven under a quiet control-plane window.

## 9. Remaining Blockers

- autoswitch authority active;
- reconcile FAIL not clean under quiet conditions;
- candidate penalty history;
- target egress quality issue from E3;
- Trusted RU stale state remains governance blocker where relevant.

## 10. Exact Next Step

Next step should be a separately approved **read-only quiet-window audit plan**:

1. Hold autoswitch authority under explicit approval.
2. Do not switch users.
3. Run `ip -4 rule show`, candidate table route, route-get, `v7-reconcile-check`, `v7-user-route-check`, `v7-killswitch-check`, and `v7-provisioning-reconcile-check`.
4. If reconcile still fails while stable rules are present, reclassify checker semantics before canary.

## 11. Runtime Mutation

```text
Runtime mutation performed: NO
Live canary executed: NO
Autoswitch apply executed by this block: NO
v7-routing-sync executed: NO
v7-user-switch executed: NO
reconcile repair/apply executed: NO
```

## 12. Files Created Or Updated

```text
docs/track7/control-plane/RECONCILE_TRUTH_AUDIT.md
docs/track7/control-plane/ROUTE_TABLE_INTEGRITY_AUDIT.md
docs/track7/control-plane/IP_RULE_INTEGRITY_AUDIT.md
docs/track7/control-plane/DATAPATH_REALITY_AUDIT.md
docs/track7/control-plane/KILLSWITCH_DEPENDENCY_ANALYSIS.md
docs/track7/control-plane/CANARY_INTEGRITY_GATES.md
docs/track7/control-plane/RECONCILE_FALSE_POSITIVE_ANALYSIS.md
tools/v7-control-plane-governance-check
```

## 13. Verification Results

```text
tools/v7-run-tests: 39 tests OK, py_compile OK
tools/v7-control-plane-governance-check --pretty: OK, current_canary_integrity_status=NO-GO
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, critical lineage gaps known=33
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release object ready=True, remaining known unresolved=43
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile ...: OK
python3 -m json.tool canary preview artifacts: OK
git diff --check: OK
```
