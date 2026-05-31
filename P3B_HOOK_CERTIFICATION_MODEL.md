# P3.B Hook Certification Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Certification Goal

Prove that Runtime Hook Dry-Run is observe-only, read-only, non-authoritative and non-executable.

## Certification Checks

| Check | Required result |
| --- | --- |
| No execution authority | Hook cannot call execute/apply/move/route commands. |
| No runtime mutation | Hook does not write runtime state or decision state. |
| No routing mutation | Hook cannot change routing, nft, proxy runtime, route classes or user bindings. |
| No autoswitch authority | Hook cannot call autoswitch apply or sentinel action paths. |
| No user movement | Hook cannot call user switch/movement commands. |
| No policy apply | Hook cannot apply policy changes. |
| No deploy/systemd | Hook cannot deploy or control services. |
| Fail-closed behavior | Missing/stale/conflicting evidence blocks or requires review. |
| Retention bounded | Hook output is derived, TTL-bound and compactable. |
| Truth source clean | Hook output references canonical sources and does not replace them. |

## Certification Evidence

The repository already supports this certification direction through:

- Read-only execution preview routes.
- Tests that reject mutating execution routes.
- Read-only observability summary.
- Read-only proxy dry-run tools.
- Preview-only execution/candidate/gate/rollback/verification models.
- Operator observability with disabled action controls.

## Certification Verdict

`hook_certified_non_executable=true`

