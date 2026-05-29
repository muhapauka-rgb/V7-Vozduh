# E26 Risk Matrix Review

| Risk | Occurred | Mitigated | Remaining | Severity After E25 |
|---|---:|---:|---|---|
| Registry drift | Yes | Yes | Still requires packet refresh before every execution. | Low with hash-bound packets |
| Target quality instability | Yes | Yes | Quality can drift; readiness must remain execution-time. | Medium |
| Dead profiles | Yes | Yes | Operator profile intake must keep quarantine/normalization path. | Low |
| Execution target integration gaps | Yes | Yes | NAT/MSS/readiness support is now proven for this target, but new target classes need repeat validation. | Medium |
| Replay attacks | Tested | Yes | Replay denial works for E25.15 packet; keep audit-backed replay set for future packet consumer. | Low |
| Hidden movers | Tested | Yes | Must be scanned before each execution. | Low |
| Delayed movement | Tested | Yes | No delayed movement observed after rollback. | Low for one-user case |
| Restore barrier/settle ambiguity | Yes earlier | Yes | Fresh sample windows are required; missing sample dir causes fail-closed NO-GO. | Low |
| Autoswitch interference | Tested | Yes | selected_moves remained 0 and autoswitch apply was not called. | Low |
| Runtime checker failures | Tested | Yes | Checkers remained OK before/after forward and rollback. | Low |
| Raw fallback execution path | Yes | Partially | Movement was governed but still uses approved raw fallback instead of movement-capable packet consumer. | Medium productization risk |
| UI execution exposure | Tested by boundary | Yes | UI execution stayed disabled; no POST/UI execution path was used. | Low |

## Residual Risk Summary

The one-user governance path is certified, but production hardening should still replace raw fallback with a movement-capable packet consumer and repeat all gates before scaling beyond one user.

