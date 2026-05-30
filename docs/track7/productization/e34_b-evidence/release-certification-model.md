# E34.B Release Certification Model

release_certification_model_defined=true

## Lifecycle States

| State | Meaning | Transition Rules | Audit Requirements |
| --- | --- | --- | --- |
| DRAFT | Release object exists but is not reviewed. | May move to REVIEW after manifest completeness check. | Creation event, source commit, manifest hash. |
| REVIEW | Release is under certification review. | May move to CERTIFIED or back to DRAFT. | Review actor, checks, findings. |
| CERTIFIED | Release passed provenance and required checks. | May move to DEPLOYED, SUPERSEDED, or REVOKED. | Certification report refs, fingerprint, signer/approver. |
| DEPLOYED | Release is linked to runtime via deployment lineage. | May move to SUPERSEDED, ROLLED_BACK, or REVOKED. | Deployment id, runtime/config fingerprints. |
| SUPERSEDED | Newer certified release replaced it. | May become ROLLBACK_ONLY if safe. | Superseding release id. |
| ROLLED_BACK | Runtime was moved away from this release via rollback. | Terminal for that deployment instance. | Rollback lineage, reason, target release. |
| REVOKED | Release provenance or safety is invalid. | Terminal except emergency forensic review. | Revocation reason, actor, impact. |

## Certification Requirements

Certification requires:

- complete release manifest;
- release fingerprint;
- source commit identity;
- test results;
- governance compatibility;
- routing intelligence compatibility if RI code/config is included;
- rollback target or approved exception;
- provenance chain.

## Fail-Closed Rule

Any missing safety-critical certification evidence prevents CERTIFIED status.

release_certification_model_defined=true
