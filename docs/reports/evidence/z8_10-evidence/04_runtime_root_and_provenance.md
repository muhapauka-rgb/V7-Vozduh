# Z8.10 Runtime Root And Provenance

## Runtime root

`/opt/v7` is the production state/runtime root, not the production code root.

Missing canonical provenance objects:

- `/opt/v7/.git`
- `/opt/v7/releases`
- `/opt/v7/releases/current`
- `/opt/v7/deploy-manifest.json`
- release manifest
- runtime linkage manifest

## Deploy metadata found

The closest provenance source is under `/opt/v7/ops`.

Latest deploy metadata:

- Path: `/opt/v7/ops/deploy-a-v7-next-12e51a5-20260601T093725Z/deploy-metadata.env`
- Deploy id: `deploy-a-v7-next-12e51a5-20260601T093725Z`
- Commit: `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`
- Package SHA: `40e92c43631a0e589cbdd790b938325252f105e6fe98b196b33b013b5274bfc5`
- Backup dir: `/root/v7-deploy-backups/deploy-a-v7-next-12e51a5-20260601T093725Z`

The deploy id and metadata identify the production copied-binary deployment as `v7-next` commit `12e51a5...`, not current authoritative `Updatesystem` commit `c85e5cb...`.

## Verdict

Runtime provenance is partially known through deploy metadata. It does not match the current authoritative branch/commit.

