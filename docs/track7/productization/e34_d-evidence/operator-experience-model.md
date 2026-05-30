# E34.D Operator Experience Model

operator_experience_defined=true

## Guided Flow

The installer experience must be:

```text
NEXT -> CHECK -> NEXT -> CHECK -> READY
```

Non-specialist operator requirements:

- clear stage name;
- plain-language check result;
- visible blocked reason;
- exact recovery hint;
- no hidden production mutation;
- explicit profile and release display;
- READY only after certification.

## Operator Screens

| Screen | Operator Sees |
| --- | --- |
| Profile | LAB/TEST/PRODUCTION/MULTI_SERVER selection and implications. |
| Release | release id, version, fingerprint, certification status. |
| Preflight | each check, PASS/WARN/FAIL, recovery hints. |
| Install | current stage, output, retry/rollback options. |
| Health | runtime, governance, routing, network, release, backup health. |
| Certification | final evidence, lineage, READY/FAILED status. |

## Diagnostic Visibility

Failures must show:

- what failed;
- why it matters;
- how to recover;
- whether retry is safe;
- whether human review is required.

## Safe Recovery

Operator can retry CHECK after remediation. Installer must not advance to READY while a blocking failure exists.

operator_experience_defined=true
