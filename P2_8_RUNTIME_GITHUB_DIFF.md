# P2.8 Runtime vs GitHub Diff

## Observed Runtime

Public runtime is alive:

- Admin health OK
- Public Gateway responds
- Admin HTTPS is fronted by Caddy

## Observed GitHub

GitHub remote HEAD is `main` at `593619d494e215d11fd826086593527a4a555690`.

The latest `Updatesystem` remote branch is `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`.

## Diff Status

Runtime source hash was not available from public checks. Therefore runtime cannot be proven equal to either GitHub `main` or GitHub `Updatesystem`.

Historical runtime docs identify `/usr/local/bin/v7-admin-api` and other `/usr/local/bin/v7-*` tools as production source, which is a deploy artifact model, not a direct GitHub checkout proof.

## Verdict

runtime_github_aligned=false

Runtime is alive but GitHub equivalence is unproven. Treat runtime/GitHub drift as unresolved and potentially high risk until source hashes or deployment manifests are checked.
