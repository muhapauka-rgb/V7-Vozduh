# P2.8.3 Production Patch Strategy

Project: V7 Vozduh
Block: P2.8.3

## Runtime-Only Patches

| Patch | Status | Keep | Review | Backport | Replace | Archive |
| --- | --- | --- | --- | --- | --- | --- |
| execution read APIs vs `origin/Updatesystem` | UNKNOWN lineage, runtime-proven | yes | yes | yes | only after explicit equivalent review | evidence only |
| execution contract/event normalization helpers | UNKNOWN lineage, runtime-proven | yes | yes | yes | no automatic replacement | evidence only |
| execution summary/contract UI | UNKNOWN lineage, runtime-proven | yes | yes | maybe | maybe with local UI | evidence only |

## Production-Only Patch Policy

- Never overwrite a production-only patch automatically.
- Treat runtime hash as behavior evidence, not development source.
- Backport only after secret scan, diff review, route review, and tests.
- If local candidate supersedes runtime behavior, document one-to-one replacement for every runtime-only API.

## Unknown Lineage Patch Policy

Unknown remains UNKNOWN until a matching signed commit, deploy manifest, or reviewed owner decision exists.

production_patch_strategy_defined=true
