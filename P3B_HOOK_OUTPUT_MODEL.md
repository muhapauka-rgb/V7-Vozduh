# P3.B Hook Output Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Allowed Outputs

| Output | Meaning |
| --- | --- |
| `NO_ACTION` | No dry-run action would be recommended. |
| `WOULD_MOVE` | The evaluated candidate would be eligible if execution were separately authorized in a future block. |
| `WOULD_BLOCK` | Safety, trust, freshness, capacity, policy or consistency gates would block. |
| `WOULD_REVIEW` | Human/operator review would be required. |
| `WOULD_ROLLBACK` | If the action had been real, rollback would be recommended. |

## Forbidden Outputs

- `MOVE`
- `EXECUTE`
- `APPLY`
- `ROUTE`
- `AUTOSWITCH_APPLY`

## Output Shape

Each hook output should include:

- Decision.
- Confidence.
- Gate results.
- Evidence refs.
- Freshness summary.
- Conflict summary.
- Simulation refs.
- Verification plan ref.
- Rollback simulation ref.
- Safety flags.
- Retention/expiry metadata.

## Fail-Closed Rules

- Missing safety evidence: `WOULD_BLOCK`.
- Missing trust evidence for trust-sensitive scope: `WOULD_BLOCK`.
- Conflicting truth sources: `WOULD_REVIEW` or `WOULD_BLOCK`.
- Stale candidate: `WOULD_REVIEW`.
- Hidden movement evidence: `WOULD_BLOCK`.
- Missing rollback path for movement-like decision: `WOULD_BLOCK`.

## Output Verdict

`hook_output_model_defined=true`

