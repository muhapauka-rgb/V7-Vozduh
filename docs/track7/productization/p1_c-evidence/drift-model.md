# P1.C Drift Model

runtime_drift_model_defined=true

## Drift Types

| Drift type | Meaning | Severity | Visibility | Impact |
| --- | --- | --- | --- | --- |
| `runtime_drift` | Running process/files differ from expected runtime identity. | warn to bad | Visible on overview/check/security. | May block forward actions until explained. |
| `config_drift` | Runtime config differs from expected release or policy state. | info to bad | Visible when config affects safety or behavior. | May require review, backup or release reconciliation. |
| `release_drift` | Current runtime does not match expected release/provenance. | warn to bad | Always visible. | Blocks release trust and may block governance. |
| `lineage_drift` | Runtime lineage cannot be tied to known release, backup or restore chain. | bad | Visible as blocking if material. | Blocks forward action until reconciled. |

## Severity Model

| Severity | Operator meaning |
| --- | --- |
| `info` | Known intentional difference; continue with awareness. |
| `warn` | Needs inspection or refresh before risky action. |
| `bad` | Blocks forward movement or release trust. |
| `muted` | Unknown or not enough evidence. |

## Visibility Rules

Visible by default:

- release drift;
- blocking runtime drift;
- stale/unknown convergence status;
- drift affecting governance, backup or restore.

Advanced details:

- raw hash diff;
- file-level diff;
- lineage internals;
- fingerprint payload.

## Operator Guidance

Drift drawer must recommend one of:

- refresh convergence check;
- inspect release provenance;
- inspect backup/restore state;
- open evidence bundle;
- start recovery/containment;
- mark known intentional drift only through role-gated workflow.

## Drift Verdict

Drift is not a raw diff UI. It is an operator trust signal with explicit severity, impact and next safe action.
