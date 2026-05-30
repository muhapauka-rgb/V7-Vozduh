# E32.3.B Fail-Closed Matrix

policy_fail_closed_matrix_defined=true

| Failure Mode | Allow | Deny | Review Required | Additional Gates Required | Human Review Required |
| --- | --- | --- | --- | --- | --- |
| `POLICY_STALE` | false | true | false | true | false |
| `POLICY_EXPIRED` | false | true | false | true | false |
| `POLICY_CONFLICT` | false | true for hard/unresolved | true for soft | false | true |
| `POLICY_SCOPE_UNKNOWN` | false | true | true | false | true |
| `POLICY_METADATA_INVALID` | false | true | true | false | true |
| `POLICY_EVIDENCE_MISSING` | false | true | false | true | false |
| `POLICY_PRIORITY_CONFLICT` | false | true | true | false | true |
| `POLICY_EVALUATION_ERROR` | false | true | true | false | true |

## Matrix Rules

No policy failure mode can produce `ALLOW`.

Hard and unresolved conflicts deny forward admission.

Soft conflicts require review and block execution until resolved.

Missing evidence requires additional gates and blocks execution until satisfied.
