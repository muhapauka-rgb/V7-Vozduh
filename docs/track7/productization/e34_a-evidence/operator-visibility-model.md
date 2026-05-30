# E34.A Operator Visibility Model

operator_visibility_defined=true

## Operator Questions

Operators need to answer:

- What release is running?
- What code version is running?
- What configuration is running?
- Does runtime differ from repo/release?
- What was deployed before?
- What rollback target exists?
- Which certification status applies?

## Required View Sections

| Section | Contents |
| --- | --- |
| Running Release | release_id, release_version, source_commit, deployment_id. |
| Runtime Fingerprint | observed runtime fingerprint, expected fingerprint, match status. |
| Config Fingerprint | observed config fingerprint, expected fingerprint, drift status. |
| Drift Status | active drift findings, severity, affected artifacts, next action. |
| Deployment History | release history, deployment events, actor, timestamps. |
| Rollback History | rollback targets, previous rollback events, containment status. |
| Certification Status | release certification status and report links. |

## Display States

| State | Meaning | Operator Action |
| --- | --- | --- |
| CONVERGED | Runtime matches release and config expectations. | Monitor. |
| DEV_DIRTY | Repo has uncommitted state; not commercial release. | Commit/release before production. |
| DRIFT_WARN | Non-critical drift exists. | Review before promotion. |
| DRIFT_BLOCKING | Runtime or config cannot be proven. | Deny production; remediate. |
| LINEAGE_UNKNOWN | Deployment chain missing. | Reconstruct or certify manually. |
| RELEASE_REVOKED | Running or intended release is revoked. | Containment/rollback. |

operator_visibility_defined=true
