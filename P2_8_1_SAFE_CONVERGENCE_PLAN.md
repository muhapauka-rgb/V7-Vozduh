# P2.8.1 Safe Convergence Plan

Project: V7 Vozduh
Block: P2.8.1

## Goal

Define a safe path from runtime/local/GitHub drift to a certified single source of truth without performing convergence during this block.

## Plan

1. Preserve current runtime.
   - No deploys.
   - No systemd changes.
   - No autoswitch, routing, user, policy, killswitch, trusted/direct RU mutations.

2. Create a signed runtime manifest in a future block.
   - Runtime path.
   - SHA256.
   - Size and mtime.
   - Source ref or UNKNOWN.
   - Deploy method or UNKNOWN.
   - Owner.

3. Resolve Admin API drift first.
   - Compare runtime `8d7adc...` against local dirty `8da1e...`, `origin/Updatesystem` `145f86...`, and `origin/main` `7f33f...`.
   - Decide whether runtime contains uncommitted production patch, older deploy, or locally generated variant.
   - Do not overwrite runtime until the decision is reviewed.

4. Classify production-only artifacts.
   - Map `/usr/local/bin/v7-api`.
   - Map `/usr/local/bin/v7-traffic-snapshot`.
   - Map missing local systemd units.
   - Classify `/etc/v7` as config/state/secret-sensitive before copying or committing anything.

5. Choose branch policy.
   - Either promote `Updatesystem` as convergence source through PR/review.
   - Or backport selected audited files to `main`.
   - Keep remote-only branches quarantined until inspected.

6. Only after review, perform a bounded convergence implementation block.
   - Commit selected local docs/tests/code.
   - Create deploy manifest.
   - Deploy only through an approved runtime mutation prompt.
   - Re-run full hash audit after deploy.

## Non-Goals

No sync, push, deploy, fetch, merge, rebase, runtime file write, or service reload was performed in P2.8.1.

safe_convergence_plan_defined=true
