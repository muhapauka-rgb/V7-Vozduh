# Routing / Datapath Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-routing-datapath.txt
docs/track7/control-plane/RECONCILE_TRUTH_AUDIT.md
docs/track7/control-plane/DATAPATH_REALITY_AUDIT.md
```

## Checks

```text
V7_USER_ROUTE_CHECK=OK
V7_RECONCILE_RESULT=FAIL
V7_RECONCILE_ERRORS=9
V7_PROVISIONING_RECONCILE_CHECK=OK
```

E8 pre-hold reconcile previously showed 11 errors. The current snapshot shows 9 errors. That variation supports the active-control-plane/race/semantic concern, but it does not prove the checker is harmless.

## Routing Reality

Observed:

- user route checks use expected egress;
- user route tables have default routes;
- ip rules include per-user lookup table rules in live snapshots;
- provisioning reconcile is OK;
- datapath checks are operationally green.

## Drift / Risk

`v7-reconcile-check` still reports missing lookup-table errors even while user-route/provisioning checks are OK. The most honest interpretation remains:

```text
datapath appears operational
reconcile checker remains FAIL
root cause not proven under quiet control plane
```

## Verdict

Routing is operationally working enough for current service, but it is not safe enough for canary because the control plane is not quiet and reconcile truth is unresolved under quiet-window conditions.
