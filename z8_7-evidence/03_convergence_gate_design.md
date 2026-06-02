# Z8.7 Evidence 03 - Permanent Convergence Gate Design

## Gate Name

```text
V7_PERMANENT_CONVERGENCE_GATE
```

## Mandatory Before

- deploy
- runtime certification
- one-user execution
- rollback certification
- production certification
- operator approval
- Z9 retry

## Inputs

Repository:

- canonical workspace path
- local branch
- local commit
- local git status
- remote canonical branch commit

Runtime code:

- runtime root
- runtime branch
- runtime commit
- deploy manifest commit
- autoswitch binary hash
- audit binary hash
- admin API version/hash
- operation wiring markers

Runtime services:

- autoswitch service status
- autoswitch timer status
- service `ExecStart`
- last execution status

Runtime state:

- users registry hash/freshness
- egress registry hash/freshness
- restore barrier state
- audit path availability
- closure path availability
- operation lineage availability

## Verdict Logic

```text
if any required input is UNKNOWN -> NO-GO
if workspace branch != canonical branch -> NO-GO
if local canonical commit != GitHub canonical commit -> NO-GO
if GitHub canonical commit != runtime commit and no approved deploy manifest explains it -> NO-GO
if binary hashes do not match expected source/deploy manifest -> NO-GO
if service status is unknown -> NO-GO
if restore barrier is active/unreadable -> NO-GO
if audit or closure path is unavailable -> NO-GO
else PASS
```

## Output

```json
{
  "gate": "V7_PERMANENT_CONVERGENCE_GATE",
  "verdict": "PASS|NO-GO",
  "workspace": {},
  "github": {},
  "runtime": {},
  "services": {},
  "state": {},
  "blockers": [],
  "next_allowed_action": "none|read_only_audit|deployment_approval|z9_readiness"
}
```
