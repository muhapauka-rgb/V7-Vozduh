# V7 Track 4 - Monolith Containment & Commercial Maturity Foundation

Purpose: define controlled platform maturation without a rewrite.

## Current Monolith State

`admin/v7-admin-api` is still a giant runtime-critical executable:

```text
30067 lines
```

It contains:

- auth/session/RBAC;
- identity DB;
- users/devices/orgs;
- profile delivery;
- provisioning;
- egress lifecycle;
- policy/direct/RU helpers;
- diagnostics;
- observability;
- autoswitch wrappers;
- embedded admin UI.

Governance verdict:

The monolith is not a reason to rewrite. It is a reason to contain.

## Containment Strategy

No giant split.

Safe order:

1. Read-only helper extraction.
2. Redaction and safe JSON IO extraction.
3. Registry/state parsers.
4. Audit event normalization.
5. Observability summary builders.
6. Identity read models.
7. Provisioning validators.
8. Egress parsers with regression tests.
9. Auth/session module.
10. Mutating provisioning actions.
11. Embedded UI extraction.

Dangerous to extract early:

- user switching;
- route policy apply;
- direct/RU and Trusted RU flows;
- profile token delivery;
- provisioning apply;
- autoswitch apply;
- anything that shells out to `v7-*` mutation tools.

## Stable API Boundaries

Before extraction, freeze endpoint contracts:

- response schema;
- state files touched;
- external commands called;
- audit event emitted;
- rollback context required;
- operator UI dependency.

Every extracted module must preserve:

- endpoint path;
- JSON shape;
- auth behavior;
- redaction behavior;
- audit behavior;
- runtime command semantics.

## Operator UX Evolution

Current direction is correct after Blocks 1-3.4:

- autoswitch is calmer;
- Telegram sentinel is advisory-first;
- health truth is more consistent;
- capacity is visible;
- runtime baseline is cleaner.

Next UX maturity priorities:

1. Compact platform status:
   - system state;
   - affected users;
   - degraded channels;
   - autoswitch guard state;
   - trusted/direct RU unknown/degraded status.
2. Incident-first navigation:
   - "what changed";
   - "who is affected";
   - "safe action";
   - "rollback impact".
3. Runtime governance summary:
   - current release/baseline;
   - suspicious executables;
   - production-only tool count;
   - sensitive-state warnings.
4. Provisioning readiness:
   - imported;
   - quarantined;
   - testing;
   - ready;
   - degraded;
   - rollback available.

Do not build a giant dashboard. The operator should see grouped summaries with drill-down only when needed.

## Provisioning Maturity Review

Current maturity:

- formal lifecycle docs exist;
- read-only validator exists in repo;
- egress state tooling exists;
- quarantine/enable-gate language exists;
- rollback strategy exists mostly as practices and scripts.

Commercial gaps:

- lifecycle state is not yet a fully enforced runtime contract everywhere;
- driver capability model is still more documented than enforced;
- rollback verification needs one operator-visible summary;
- provisioning actions need consistent actor/reason/before-after events;
- production-only provisioning tools need repo lineage.

Next safe provisioning priorities:

1. Make lifecycle state validator operator-visible.
2. Add capability metadata to egress registry without changing routing behavior.
3. Add dry-run enable report:
   - kill switch compatible;
   - service matrix status;
   - DNS path;
   - route class eligibility;
   - rollback material.
4. Keep enable manual and explicit.

## Commercial Readiness Gap Map

| Area | Current Maturity | Main Gap | Priority |
|---|---|---|---|
| Datapath safety | Stronger after verification | Needs continuous no-leak validation | High |
| Autoswitch | Stabilized | Still has frozen-user/health nuance to mature | High |
| Runtime governance | Started | 117 unknown active-like tools not fully governed | High |
| Release lineage | Weak but improving | No release ID/provenance chain | High |
| Sensitive state | Mixed | Token state `0644` | High |
| Identity DB | Operational | Path contract historical mismatch | Medium |
| Provisioning | Partially mature | Lifecycle not fully enforced as runtime contract | High |
| Admin monolith | Operational but risky | 30k-line coupling | High |
| Operator UX | Calmer foundation | Still monolithic/dense | Medium/high |
| Commercial org model | Documented/partly present | Needs policy enforcement and operator workflows | Medium |

## Controlled Evolution Rules

Any new feature, transport, runtime tool, or service must pass:

1. Governance check:
   - does it preserve datapath safety?
   - does it preserve deterministic routing?
   - does it avoid hidden behavior?
2. Runtime registry check:
   - owner;
   - mutation level;
   - rollback sensitivity;
   - repo lineage.
3. Observability check:
   - compact summary first;
   - drill-down details;
   - no metric wall.
4. Release lineage check:
   - manifest updated;
   - verification recorded;
   - rollback path known.
5. Safety check:
   - `v7-killswitch-check`;
   - `v7-user-route-check`;
   - `v7-provisioning-reconcile-check`;
   - `systemctl --failed`;
   - `v7-observability-summary --pretty`.

## Track 4 Verdict

V7 is past emergency-chaos stabilization, but it is not yet commercial-grade.

Best honest classification:

```text
stabilized operational prototype with credible commercial-grade foundation
```

Next maturity work must focus on governance, lineage, permissions, monolith containment, and provisioning enforcement.

