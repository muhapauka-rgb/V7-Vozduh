# PROGRAM CONV.1 - PERMANENT TRUTH, DEPLOYMENT AND PRODUCTION CONVERGENCE SYSTEM REPORT

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Date: 2026-06-03

## 1. Human Explanation

CONV.1 treats the repeated local/GitHub/production divergence as a process failure, not as a PERF.4-only issue.

The existing project already had the right foundations:

- `tools/v7-truth-check`
- `tools/v7-safe-deploy`
- `tools/v7-release-sync`
- deploy/release manifests in `tools/v7_sync_lib.py`

CONV.1 extends those mechanisms instead of creating a parallel release or truth system.

The operator now has one convergence view, one deploy allowlist owner, one manifest model, and one runtime fingerprint model.
If local, GitHub, production, manifest, deployed files, or snapshot subsystem truth is unknown, the system returns `NO-GO`.

## 2. Canonical Truth Model

| Truth item | Canonical owner |
| --- | --- |
| Canonical workspace | `/Users/ponch/Documents/New project` |
| Canonical branch | `Updatesystem` |
| Canonical deploy source | `origin/Updatesystem` plus approved safe deploy package |
| Canonical deploy tool | `tools/v7-safe-deploy` |
| Canonical release sync tool | `tools/v7-release-sync` |
| Canonical truth gate | `tools/v7-truth-check` |
| Canonical convergence view | `tools/v7-convergence-status` |
| Canonical deploy allowlist | `tools/v7_sync_lib.APPROVED_DEPLOY_FILES` |
| Canonical runtime fingerprint | `/opt/v7/runtime-fingerprint.json` |

## 3. Deploy Pipeline

Canonical path:

```text
commit
push
manifest
safe deploy
truth-check
verify
aligned
```

No alternate deploy path is introduced.

`tools/v7-safe-deploy` now fails before deploy if allowlist validation fails.

The safe deploy payload now includes:

- deploy manifest;
- release manifest;
- runtime linkage;
- allowlist validation;
- runtime fingerprint;
- runtime fingerprint validation.

## 4. Runtime Fingerprint

CONV.1 adds runtime fingerprint schema:

`v7-runtime-fingerprint/v1`

The fingerprint includes:

- branch;
- commit;
- deployment id;
- generated timestamp;
- runtime root;
- critical file hashes;
- service/systemd unit names;
- snapshot subsystem root;
- snapshot refresh CLI path;
- snapshot refresh systemd units;
- required snapshot files.

Deploy writes the fingerprint to:

`/opt/v7/runtime-fingerprint.json`

Truth checks can now distinguish "deployed but not fingerprinted" from "aligned".

## 5. Allowlist Governance

The previous SYNC.1 blocker was real: the safe deploy allowlist did not include the full current runtime package.

CONV.1 fixes that by:

- expanding the canonical allowlist to include current `admin_core` runtime dependencies;
- adding AST-based dependency discovery from runtime entrypoints;
- detecting required `admin_core` files missing from the allowlist;
- detecting local missing files;
- detecting duplicate remote deploy targets;
- blocking deploy if validation is not `PASS`.

Validation schema:

`v7-deploy-allowlist-validation/v1`

Observed local result:

```text
final_verdict=PASS
missing_required_paths=[]
missing_local_files=[]
duplicate_remote_paths=[]
```

## 6. Divergence Detection

`tools/v7-convergence-status` now gives one operator answer:

```text
LOCAL
GITHUB
PRODUCTION
STATUS ALIGNED|NOT_ALIGNED
```

Machine-readable mode:

```text
tools/v7-convergence-status --json
```

It detects:

- local dirty runtime-critical files;
- local branch mismatch;
- GitHub branch unreadable or commit mismatch;
- production commit mismatch;
- production file hash mismatch;
- missing runtime modules;
- missing or unknown runtime fingerprint;
- missing snapshot subsystem;
- missing snapshot refresh CLI;
- missing snapshot refresh service/timer truth.

## 7. PERF.4 Convergence Result

PERF.4 is not production-converged yet.

Current proven blocker:

Production still reports D.1-era runtime commit:

`c68aa5be569a2763ba00c2954182306a09c50d86`

The current runtime truth snapshot also lacks the new PERF.4/CONV.1 required checks:

- `sha256sum /usr/local/bin/v7-intelligence-snapshot-refresh`
- `systemctl status v7-intelligence-snapshot-refresh.service --no-pager`
- `systemctl status v7-intelligence-snapshot-refresh.timer --no-pager`
- `test -x /usr/local/bin/v7-intelligence-snapshot-refresh`
- `ls -la /opt/v7/egress/state/intelligence`

Therefore the correct answer is `NO-GO`, not silent continuation.

PERF.4 can be safely converged only after CONV.1 is committed, pushed, deployed through the canonical safe deploy path, and verified by `v7-convergence-status` plus `v7-truth-check`.

## 8. Future Operator Workflow

For future approved work:

```text
git status --short
python3 -m unittest discover tests
git commit
git push origin Updatesystem
tools/v7-safe-deploy
tools/v7-truth-check --all
tools/v7-convergence-status
```

If any step reports unknown production truth, missing runtime file, missing fingerprint, missing snapshot subsystem, or mismatch:

```text
STOP
```

No autoswitch action is part of this workflow.
No route mutation is part of this workflow.
No user movement is part of this workflow.

## 9. Tests

Added or extended tests for:

- deploy allowlist coverage for current runtime package and PERF.4 dependencies;
- missing runtime import detection;
- deploy manifest runtime fingerprint presence;
- runtime fingerprint validation fail-closed behavior;
- convergence status operator view;
- truth-check snapshot/fingerprint derived flags.

Verification:

```text
python3 -m py_compile tools/v7_sync_lib.py tools/v7-truth-check tools/v7-convergence-status tools/v7-safe-deploy tools/v7-release-sync
python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_v7_truth_check
python3 -m unittest discover tests
git diff --check
```

All passed.

## Final Verdicts

canonical_truth_model_complete=true
convergence_status_command_complete=true
deploy_manifest_model_complete=true
allowlist_governance_complete=true
runtime_fingerprint_complete=true
safe_release_pipeline_complete=true
divergence_detection_complete=true
perf4_production_converged=false
local_github_production_aligned=false
future_truth_drift_prevented=true

## Next Step

Commit CONV.1 as its own package.
Then push `Updatesystem`.
Then run the approved safe deploy path.
Then run:

```text
tools/v7-truth-check --all
tools/v7-convergence-status
```

Do not start RI.4 until convergence returns `ALIGNED`.

