# RT2-PR1 Admission Check and Pre-Mutation Baseline

Status: `RT2_PR1_ADMISSION_NOT_PROJECTED_PRE_MUTATION_BASELINE_CAPTURED_REAL_TRAFFIC_OUTCOME_OPEN`

Scope: only OMP V4.78 Section 28.9 `RT2 Post-Reset Operating Profile`, sequence `RT2-PR1 -> RT2-PR7`. No unrelated OMP/backlog capability is admitted or executed.

## Admission

| Field | Evidence / result |
| --- | --- |
| Trigger | operator explicitly requested execution of the post-Reset profile only |
| Owner | existing OMP admission and CPS projection owners |
| Contract commit | `97e651bb8b414b03d2b1de3b50acc0c9399f2e72`, published to `origin/Updatesystem` |
| Required inputs | Reset terminal, `FINAL_ARCHITECTURE_MAP`, post-Reset reality, local/CPS/runtime truth and measurement owners available |
| First cell | `RT2-PR1 PRODUCTION_REALITY_VALIDATION` |
| Protected WIP | preserved; no CAP-U lane, natural-evidence lane or unrelated OMP item displaced |
| Admission result | `NOT_PROJECTED`: a targeted CPS Section 0 change contradicted the existing mission/registry projections and was reverted; no legal mutation Mission exists |
| Permitted effect | bounded read-only PR1 baseline/observation and independent PR2 analysis only; no Runtime, routing, user, Policy or Authority mutation |

The pre-change truth run proved the Reset terminal and deployed copied-binary identity. A later targeted CPS activation attempt returned `NO-GO` because Section 0, active WIP, registry, mission identity and OMP terminal projections would diverge. Those attempted CPS/OMP pointer changes were reverted rather than hiding the contradiction. Publishing docs-only contract commit `97e651bb` requires no Runtime deploy.

## PRE_MUTATION_BASELINE

Source boundary: Git commit `97e651bb8b414b03d2b1de3b50acc0c9399f2e72`. New `.understand-anything` generated analysis files are excluded from source metrics.

| Source metric | Baseline |
| --- | ---: |
| Tracked files | 8,817 |
| Tracked text files | 8,522 |
| Total tracked text LOC | 21,924,909 |
| Program-source files (`admin/`, `admin_core/`, `tools/`) | 145 |
| Program-source LOC | 182,264 |
| Test files / LOC | 115 / 56,648 |
| Documentation files / LOC | 6,192 / 5,783,121 |
| Config/infra files / LOC under the stated projection | 1,522 / 15,502,763 |
| Python files / functions / classes in program+test projection | 129 / 3,541 / 125 |
| Tracked systemd service/timer declarations | 7 / 5 |

The categories overlap only where explicitly stated by the projection and are not summed to infer handwritten code. Before/after comparisons must reuse the same rules.

## Production runtime baseline

Read-only production target: existing manifest alias `v7-vps`. Capture date: 2026-08-13.

| Metric | Baseline |
| --- | ---: |
| Compatible Core-primary users | 124 |
| Routing classes | 6 |
| Core fwmark rules | 6 |
| Class default routes | 6 |
| Legacy per-user source rules | 0 |
| nft `user_class` elements | 124 |
| nft `class_egress` elements | 6 |
| All `ip rule` entries | 12 |
| All route entries across tables | 47 |
| Discovered V7-named loaded unit rows | 29 |
| Active V7-named unit rows | 19 |
| Snapshot V7-related processes at bounded census | 10 |

`/usr/local/bin/v7-routing-sync --core-primary-verify --json` returned `CORE_PRIMARY_VERIFY_PASS`, exact Authority contract `rcpp_6bfcaa2063bd7567c9554b6d`, `nft_table_present=true`, no missing mark rules, no legacy primary rules and `legacy_fallback_ready=true`.

## Topology finding

The expanded production census invalidates the earlier limited-snapshot wording that the draft planner unit was not loaded:

- `v7-autoswitch-planner.timer` is loaded and `active/running`;
- its service runs `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only`;
- the child path includes `v7-users-autoswitch --consume-passive-events-only`;
- this is a live Control/Engineering consumption path, not by itself a primary routing writer;
- `v7-routing-sync.service` remains the Core-primary apply owner and is `active/exited` after successful apply;
- `v7-users-autoswitch.service` and `.timer` remain inactive;
- additional active V7 timers include direct autosync, quality compact, path guard/sanity, Matrix refresh, Telegram sentinel and traffic collector.

Disposition: `HIDDEN_RUNTIME_DEPENDENCY_CANDIDATE` plus `RUNTIME_PACKAGE_CLASSIFICATION_REQUIRED` for PR2/PR3. No unit is disabled or modified by PR1. Exact caller, consumer, state and mutation effects must be proven before keep/shrink/remove disposition.

## Real traffic outcome

Two bounded read-only reads of nft ingress counters returned `packets=0`, `bytes=0`. Therefore:

- kernel/Core state = `PASS`;
- real ordinary client packet consumption through the class-mark path = `NOT_PROVEN` in this observation window;
- `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED` remains open;
- no traffic is generated and no user is moved to manufacture evidence;
- reentry is the next ordinary production packet observed by the existing nft/routing verification owner.

This real-world wait does not invalidate `PRE_MUTATION_BASELINE_CAPTURED` or prevent independent read-only PR2 analysis. It blocks any stronger PR1 production-outcome terminal and any mutation that depends on that proof.

## PR1 disposition

- `PRE_MUTATION_BASELINE_CAPTURED = PASS`.
- `RT2_PROFILE_ADMISSION = NOT_PROJECTED`; mutation cells remain blocked pending one consistent existing-owner OMP/CPS admission transaction.
- `CORE_PRIMARY_KERNEL_STATE = PASS`.
- `RUNTIME_PACKAGE_TOPOLOGY_BASELINE = CAPTURED_WITH_NEW_GAP`.
- `REAL_TRAFFIC_PATH_CONFIRMED = NOT_PROVEN`.
- `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED = NOT_PROVEN`.
- Exact safe successor: independent read-only `RT2-PR2` relationship/responsibility audit; PR1 remains open for natural traffic reentry and no mutation cell is admitted.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 118 -> +118`; no CPS/OMP contract line remained changed after the failed activation projection was reverted.

Test LOC: `0 -> 0 -> 0`.

Program files added / modified / deleted / moved: `0 / 0 / 0 / 0`.

Functions/classes/entrypoints added / removed / moved / merged / changed: `0 / 0 / 0 / 0 / 0`.

Runtime dependency/state/unit/routing edges changed: `0`; read-only evidence discovered existing edges only.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`
