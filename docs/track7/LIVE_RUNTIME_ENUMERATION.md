# V7 Track 7.3 — Live Runtime Enumeration Model

Track 7.3 defines a read-only way to enumerate live V7 runtime tools and expand lineage confidence. It must not import runtime files into git, delete files, chmod/chown, restart services, sync deployment, or mutate datapath state.

## Read-Only Enumerator

Tool:

```text
tools/v7-runtime-tool-enumerate
```

Default target:

```text
/usr/local/bin/v7*
```

Collected metadata per tool:

- basename;
- full path;
- sha256;
- size;
- mode;
- mtime epoch;
- executable bit;
- systemd references, only with `--references`;
- reference count/sample, only with `--references`;
- repo linkage status;
- production-only status;
- governance class;
- runtime criticality;
- release relevance;
- provenance confidence.

Non-mutation guarantee:

```text
no import
no delete
no sync
no chmod/chown
no service restart
```

## Expected Live Command

On the VPS, run:

```bash
cd /path/to/repo
tools/v7-runtime-tool-enumerate --references > runtime-enumeration.json
tools/v7-runtime-tool-enumerate --references --pretty
```

Then feed the JSON into the governance diff:

```bash
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
```

## Current Local Result

Local execution against default `/usr/local/bin` found no V7 runtime tools:

```text
total_v7_tools=0
production_only=0
warning=No runtime tools found in supplied runtime dirs. Run on VPS or provide mounted/copied runtime directory.
```

This is expected on the local workstation and does not resolve the 83 unlisted production-only gaps.

## Live Access Status

Read-only SSH access to the VPS was attempted with BatchMode and failed:

```text
root@195.2.79.116: Permission denied (publickey,password).
```

No live files were read, changed, imported, archived, chmodded, chowned, or restarted.

## Governance Interpretation

Until live enumeration succeeds or a copied `/usr/local/bin` runtime snapshot is provided:

- named lineage gaps remain: 20;
- unlisted lineage gaps remain: 83;
- production-only tool count remains: 103;
- critical known lineage gaps remain: 16;
- runtime inventory ambiguity is not resolved.

## Safe Next Evidence

Acceptable evidence sources:

- run `tools/v7-runtime-tool-enumerate --references` directly on the VPS;
- provide a read-only copied `/usr/local/bin` tree;
- provide a live runtime manifest with per-tool hashes and basenames.

Not acceptable for Track 7.3:

- mass importing `/usr/local/bin`;
- deleting or archiving unknown tools;
- syncing runtime to repo;
- chmod/chown;
- deployment rewrite.
