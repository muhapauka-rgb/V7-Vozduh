# DEPLOY A Code Sync Plan

## Source

GitHub `v7-next`:

`12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`

Local checkout matched GitHub before packaging.

## Package

Package:

`/tmp/v7-next-code-12e51a5.tar.gz` on server

Package SHA-256:

`40e92c43631a0e589cbdd790b938325252f105e6fe98b196b33b013b5274bfc5`

## Destination

Filesystem deploy destinations:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/admin_core/*.py`
- `/usr/local/bin/v7-*`

## Exclusions

No runtime state, registries, logs, secrets, private configs, or client profiles were included in the package.

Systemd unit files were not installed or changed.

## Verdicts

- code_sync_plan_ready=true
- sync_method=code_only_archive_install
- runtime_state_in_package=false
- systemd_install_planned=false
