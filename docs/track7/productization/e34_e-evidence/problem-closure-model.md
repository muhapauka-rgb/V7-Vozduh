# E34.E Problem Closure Model

problem_closure_defined=true

## Closure Principle

A problem is not closed because a command succeeded. It is closed when evidence proves the system is in the intended state or safely fail-closed.

## Required Closure Steps

1. Identify all plausible theories that fit the initial symptom.
2. Collect evidence for each plausible theory.
3. Compare evidence and eliminate unsupported theories.
4. Determine root cause or explicitly mark root cause unknown.
5. Choose safe remediation, containment, rollback, or escalation.
6. Verify post-action state.
7. Produce closure verdict.

## Closure Verdicts

| Verdict | Meaning | Forward execution allowed? |
| --- | --- | --- |
| `CLOSED_FIXED` | Root cause remediated and verification passed. | Only if normal gates pass. |
| `CLOSED_NO_ACTION_NEEDED` | Evidence shows no unsafe condition remains. | Only if normal gates pass. |
| `CLOSED_FAIL_CLOSED` | System is intentionally blocked for safety. | No. |
| `CLOSED_ESCALATED` | Safe action requires higher authority or product decision. | No. |
| `CLOSED_REQUIRES_ARCHITECTURE_DECISION` | Architecture does not yet define a safe behavior. | No. |

## Anti-Patterns

Invalid closure statements:

- “Looks OK.”
- “Probably network.”
- “Retried and it worked.”
- “Ignored because user is unaffected.”
- “Operator knows this system.”

Valid closure must reference evidence.

## Closure Record

Each closure record should include:

```text
problem_id
evidence_bundle_id
root_cause
remediation
verification_result
closure_verdict
operator
timestamp
remaining_risk
next_review
```
