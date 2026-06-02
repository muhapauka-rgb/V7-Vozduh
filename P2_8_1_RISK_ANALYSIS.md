# P2.8.1 Risk Analysis

Project: V7 Vozduh
Block: P2.8.1

## Overall Risk

Overall risk: High.

safe_to_continue=false

## Main Risks

| Risk | Severity | Evidence | Required mitigation |
| --- | --- | --- | --- |
| Admin API provenance mismatch | High | runtime/local/GitHub Admin API hashes all differ | dedicated Admin API lineage review |
| Dirty local implementation | High | `admin/v7-admin-api` modified with 3432 insertions and 20 deletions | review, test, commit or split |
| Production-only runtime artifacts | High | runtime has files with no local exact source | manifest and ownership mapping |
| Branch role ambiguity | Medium | GitHub default is `main`; active local work is `Updatesystem` | branch strategy decision |
| Runtime state copied into reports | Medium | `/etc/v7` and `/opt/v7` contain live config/state | use hashes/metadata only unless secret-safe review approves content capture |
| Remote-only branch ambiguity | Medium | `codex/dynamic-load-autoswitch-pr` present in GitHub live refs | inspect in future read-only branch audit |

## Safety Verdict

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_mutation_performed=false
trusted_direct_ru_mutation_performed=false
execution_engine_implemented=false
runtime_hooks_implemented=false
git_push_performed=false
git_merge_performed=false
git_rebase_performed=false
deploy_performed=false
systemd_changed=false
