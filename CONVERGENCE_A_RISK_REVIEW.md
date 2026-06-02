# Convergence A Risk Review

Project: V7 Vozduh
Block: Convergence A

| Risk Area | Severity | Reason | Mitigation |
| --- | --- | --- | --- |
| Lineage | CRITICAL | runtime Admin API hash is not in inspected Git history | preserve runtime read APIs first; require manifest |
| Runtime | HIGH | live behavior diverges from GitHub baseline | no runtime mutation; hash-gated migration |
| GitHub | HIGH | `main` behind; `Updatesystem` not deployed source | use `Updatesystem` as base only, not runtime truth |
| Admin | HIGH | Admin API contains operator and execution surfaces | route/API/UI verification per wave |
| Truth Sources | HIGH | runtime state truth and source truth are split | truth-source matrix and no live state copy |
| Package Decisions | HIGH | whole-file decisions would lose behavior or deploy unreviewed code | feature-by-feature waves |
| Unknown Ownership | HIGH | runtime-only patch owner/source unknown | classify as UNKNOWN until reviewed |

## Overall

Overall risk: HIGH with CRITICAL lineage risk.
