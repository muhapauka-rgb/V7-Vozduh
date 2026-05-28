# E24.1 Helper Deploy Manifest

Deploy time: 2026-05-28T08:37Z-08:38Z.

## Scope

Only missing governance helpers were deployed:

- `/usr/local/bin/v7-second-canary-target-readiness`
- `/usr/local/bin/v7-restore-settle-gate`

No services were restarted.
No runtime registry files were changed.
No routing commands were executed.
No autoswitch apply was executed.
No user movement command was executed.

## Before Deploy

- `/usr/local/bin/v7-second-canary-target-readiness`: MISSING
- `/usr/local/bin/v7-restore-settle-gate`: MISSING

## Deploy Method

1. Copied reviewed repo helpers to VPS temporary path:
   - `/tmp/v7-second-canary-target-readiness`
   - `/tmp/v7-restore-settle-gate`
2. Installed them to `/usr/local/bin` with:
   - owner=`root`
   - group=`root`
   - mode=`0755`

## After Deploy

- `/usr/local/bin/v7-second-canary-target-readiness`
  - mode/owner: `-rwxr-xr-x root root`
  - sha256=`75607c4e56740788cb8b1e160efa539059bcf4ca29f0d8978b8b6ae2b43aff8a`
  - shebang=`#!/usr/bin/env python3`
- `/usr/local/bin/v7-restore-settle-gate`
  - mode/owner: `-rwxr-xr-x root root`
  - sha256=`eb74101dd44b0bfe8df106719602a8318ba7593149f6535f0ec0dcb9fc6dfbdc`
  - shebang=`#!/usr/bin/env python3`

## Deploy Verdict

- helpers_deployed=true
- deployed_hashes_match_repo=true
- permission_executable=true
- deploy_scope_bounded=true
