# E34.D Deployment Profile Model

deployment_profile_model_defined=true

## Profiles

| Profile | Purpose | Requirements | Restrictions | Certification Level |
| --- | --- | --- | --- | --- |
| LAB | Local experimentation and architecture validation. | Minimal host checks, local-only config, no production secrets. | Not production deployable; may use dirty repo state. | LAB_READY |
| TEST | Test server validation with release candidate. | Release object, preflight checks, backup plan, network checks. | No production user movement; test-only credentials. | TEST_CERTIFIED |
| PRODUCTION | Commercial/real deployment. | Certified release, verified backup, complete preflight, health checks, provenance, rollback. | No dirty release, no unknown lineage, no missing backup. | PRODUCTION_CERTIFIED |
| MULTI_SERVER | Future multi-host deployment. | All PRODUCTION requirements plus host identity, cluster roles, per-host fingerprints, shared lineage. | Not certified until multi-server program is defined. | CANDIDATE_ONLY |

## Profile Selection Rules

- Operator must select profile before preflight.
- Profile determines required checks and failure severity.
- A lower profile cannot be silently promoted to a higher profile.
- PRODUCTION requires certified release and backup readiness.

deployment_profile_model_defined=true
