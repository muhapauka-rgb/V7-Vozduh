# E34.B Operator Visibility Model

release_visibility_defined=true

## Operator Questions

Operators must see:

- What release is current?
- What release history exists?
- What certification status applies?
- What rollback target exists?
- Is the provenance chain intact?
- Does runtime drift from release?

## Required Views

| View | Contents |
| --- | --- |
| Current Release | release_id, version, source commit, fingerprint, deployed_at. |
| Release History | prior releases, supersession, revocation, rollback-only states. |
| Certification Status | DRAFT/REVIEW/CERTIFIED/DEPLOYED/SUPERSEDED/ROLLED_BACK/REVOKED. |
| Rollback History | rollback target, rollback events, verification result. |
| Provenance Chain | source repo, commit, creator, certification refs, deployment lineage. |
| Drift Status | runtime/config/release/lineage drift and severity. |

## Display States

| State | Meaning | Operator Action |
| --- | --- | --- |
| RELEASE_CERTIFIED | Release can be deployed if gates pass. | Continue deployment path. |
| RELEASE_DEPLOYED_CONVERGED | Runtime matches release expectations. | Monitor. |
| RELEASE_DRAFT_OR_REVIEW | Not production deployable. | Complete certification. |
| RELEASE_PROVENANCE_BROKEN | Lineage/fingerprint/source cannot be verified. | Deny deployment; investigate. |
| RELEASE_REVOKED | Release unsafe or invalid. | Containment/rollback. |
| ROLLBACK_AVAILABLE | Known rollback release exists. | Use only through rollback procedure. |

release_visibility_defined=true
