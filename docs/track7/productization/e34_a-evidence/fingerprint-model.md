# E34.A Fingerprint Model

fingerprint_model_defined=true

## Fingerprint Types

| Fingerprint | Scope | Generation Method | Owner | Freshness |
| --- | --- | --- | --- | --- |
| runtime_fingerprint | Running binaries/scripts/process command lines/service units. | Hash normalized runtime inventory and executable file hashes. | Deployment/runtime verifier. | Collected per deployment and on demand. |
| config_fingerprint | Runtime config files, registries, policy, matrices, env, service units. | Hash canonicalized config manifest and file contents. | Configuration verifier. | Collected before approval and after deployment. |
| release_fingerprint | Repo commit, release manifest, packaged artifacts, expected config schema. | Hash release object and artifact manifest. | Release builder. | Immutable per release. |

## Canonicalization Rules

- Sort manifest entries by path.
- Hash file content, size, mode, and normalized owner where relevant.
- Exclude volatile runtime counters unless classified as runtime_state_fingerprint.
- Redact secret values before evidence publication, but hash secret-bearing files in local verification.
- Use explicit schema versions for fingerprint manifests.

## Verification Model

```text
release_fingerprint + deployment_manifest -> expected_runtime_fingerprint
observed_runtime_fingerprint -> live_runtime_truth
expected_runtime_fingerprint == observed_runtime_fingerprint -> converged
```

Config verification uses:

```text
expected_config_fingerprint == observed_config_fingerprint
```

## Product Decision Required

```text
ARCHITECTURE_DECISION_REQUIRED:
decision_needed=fingerprint_hash_algorithm
options=sha256, sha512, blake3
pros=sha256 is universal; sha512 is conservative; blake3 is fast
cons=sha256 less future margin; sha512 larger metadata; blake3 less universally available
recommended_option=sha256_for_portability
```

fingerprint_model_defined=true
