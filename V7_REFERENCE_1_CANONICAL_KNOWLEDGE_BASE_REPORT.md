# V7.REFERENCE.1 Canonical Knowledge Base Report

Date: 2026-06-18
Initial verified commit: `8ba2178f`
Runtime changes: none
Logic changes: none
UI changes: none
Planner/governance/execution changes: none

## 1. Created Files

| File | Purpose |
| --- | --- |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Canonical current truth for V7 concepts. |
| `docs/reference/SYSTEM_MAP.md` | Compact module-to-truth map. |
| `docs/decisions/ADR_TEMPLATE.md` | Standard ADR template. |
| `docs/decisions/ADR-001-canonical-reference-system.md` | Decision to make reference/ADR docs canonical memory. |
| `docs/decisions/ADR-002-channel-score-is-mixed-score.md` | Decision that Channel Score is diagnostics/quality, not assignment truth. |
| `docs/decisions/ADR-003-health-screen-diagnostics-only.md` | Decision that Technical Health is diagnostics only. |
| `docs/decisions/ADR-004-channel-drawer-is-primary-operator-surface.md` | Decision that Channel Drawer is the primary channel operator surface. |

## 2. Extracted Knowledge

| Concept | Stable conclusion extracted |
| --- | --- |
| Channels | Channels are operator objects backed by runtime registry, planner truth, service/route/runtime evidence, capacity, and assigned users. |
| Channel Decision V7 | Operator-facing decision must come from planner-derived assignment truth: Use, Evacuate, Keep Current Users, Emergency Only, Blocked. |
| Channel Score | Score is a mixed technical health score and must not be treated as assignment truth. |
| Technical Health | Health is nested diagnostics explaining why the score is what it is. |
| Route | Route is runtime/readiness/leak/mismatch evidence and planner gate input; it is not a standalone unsafe action path. |
| Capacity | Capacity bounds assignment/movement through current/projected users, limits, and load policy. |
| Service Matrix | Service Matrix is measurement/diagnostics with existing safe refresh handlers; it is not a business action owner. |
| Stability | Stability is a quality gate and score component; raw labels must be translated for operators. |
| Runtime Readiness | Runtime readiness can block trust/action even when UI health looks good. |
| History | History is evidence after problem selection, not first-line operator noise. |
| Planner | `tools/v7-users-autoswitch` remains the assignment/retention/evacuation authority. |
| Assignment | Assignment truth is planner-derived and separate from score. |
| Users | User Drawer answers who/problem/why/action using existing user/profile/route/recommendation truth. |
| Groups / Policies | Policy constrains users/actions/movement; full group/policy contract still needs a future dedicated audit. |
| Autonomy | Autonomy/intelligence must remain derived and governed, not a new execution path. |
| Truth / Convergence | Truth and convergence tools are mandatory gates for meaningful work. |
| Admin UI Operator Model | V7 uses a hybrid model: attention/problem-first when active work exists, object-first when healthy or object is known. |

## 3. Sections Completed

All required canonical reference sections were created:

1. Channels
2. Channel Decision V7
3. Channel Score
4. Technical Health
5. Route
6. Capacity
7. Service Matrix
8. Stability
9. Runtime Readiness
10. History
11. Planner
12. Assignment
13. Users
14. Groups / Policies
15. Autonomy
16. Truth / Convergence
17. Admin UI Operator Model

Each section includes meaning, truth source, calculation location, display location, affecting factors, non-affecting factors, operator meaning, engineer meaning, caveats, related reports/ADRs, and last verified commit.

## 4. Sections Marked UNKNOWN

| Section | UNKNOWN item |
| --- | --- |
| Groups / Policies | Full canonical group/policy contract beyond current channel/operator work requires future audit. |
| Autonomy | Full autonomy contract across all shadow/intelligence modules requires future audit. |

## 5. ADRs Created

| ADR | Decision |
| --- | --- |
| ADR-001 | Canonical reference and ADR system become durable project memory. |
| ADR-002 | Channel Score is a mixed technical score, not assignment truth. |
| ADR-003 | Health screen is diagnostics only. |
| ADR-004 | Channel Drawer is primary channel operator surface. |

## 6. Workflow Rule Added

Added a mandatory reference update rule to `docs/reference/V7_CANONICAL_REFERENCE.md` and a compact workflow integration rule to `docs/reference/SYSTEM_MAP.md`.

Rule:

1. Update canonical reference after major system-meaning changes.
2. Update or create ADR when a decision changed.
3. Run `tools/v7-truth-check --all --json`.
4. Run `tools/v7-convergence-status --json`.
5. Commit code and docs together.

## 7. Tests Run

Initial gate before documentation work:

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS / `FULLY_ALIGNED` |
| `tools/v7-convergence-status --json` | PASS / `ALIGNED` |
| `git diff --check` | PASS |

Final verification is required after commit/push.

## 8. Remaining Gaps

| Gap | Follow-up |
| --- | --- |
| Full Groups / Policies canonical contract | Future dedicated audit should map policy files, group/org model, UI surfaces, planner gates, and execution gates. |
| Full Autonomy canonical contract | Future dedicated audit should map shadow autonomy, intelligence platform, recommendation, and governed execution boundaries. |
| Runtime code/documentation commit mismatch | Existing truth/convergence tools can pass with docs-only local commits. Reports must state runtime alignment honestly. |

## 9. Final Verdict

REFERENCE_BASE_CREATED
