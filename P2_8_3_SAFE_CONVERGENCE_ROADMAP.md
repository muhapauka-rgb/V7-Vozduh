# P2.8.3 Safe Convergence Roadmap

Project: V7 Vozduh
Block: P2.8.3

## Roadmap

1. Freeze runtime mutation.
   - Keep runtime as evidence only.
   - Do not deploy, restart, or write systemd/runtime files.

2. Review runtime-only features.
   - Capture route/function/UI diff.
   - Decide preserve/backport/replace for each execution read API.

3. Review local-only features.
   - Split P2.2-P2.7 local dirty work into feature packages.
   - Validate non-executable semantics and retention behavior.

4. Review GitHub-only and branch-only features.
   - Inspect `codex/dynamic-load-autoswitch-pr`.
   - Confirm no unique Admin API feature would be lost.

5. Build convergence branch in a future block.
   - Base on `Updatesystem`.
   - Apply reviewed feature packages only.
   - Preserve runtime read APIs or document replacement.

6. Run verification.
   - Static route inventory.
   - API read-only tests.
   - Candidate/approval/dry-run preview tests.
   - Fail-closed tests.
   - Secret scan for runtime-captured material.

7. Prepare release package.
   - Generate Admin API source hash.
   - Generate deploy manifest.
   - Define rollback package.

8. Future deployment block.
   - Only after explicit runtime mutation approval.
   - Verify post-deploy runtime hash.

safe_convergence_roadmap_defined=true
