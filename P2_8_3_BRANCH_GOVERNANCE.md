# P2.8.3 Branch Governance

Project: V7 Vozduh
Block: P2.8.3

## Branch Roles

| Role | Branch | Policy |
| --- | --- | --- |
| Production branch | `main` | remains default/release history until explicitly changed |
| Development branch | `Updatesystem` | convergence development baseline |
| Archive branch | future `archive/*` or labels, no operation in this block | for stale experimental branches after audit |
| Experimental branch | `codex/*` | must not be treated as production source |
| Future release branch | future release branch from reviewed convergence package | created only after approval |

## Governance Rules

1. No branch operation in P2.8.3.
2. `Updatesystem` is the only reasonable current convergence base because it is closest to runtime and is the local upstream.
3. `main` should not receive direct dirty work.
4. Remote-only branches must be inspected before archive/delete decisions.
5. Release branch must include a deploy manifest and Admin API hash certification before runtime deployment.

branch_governance_defined=true
