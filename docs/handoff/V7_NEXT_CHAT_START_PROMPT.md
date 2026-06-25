# V7 Next Chat Start Prompt

Paste this into the next Codex or ChatGPT chat:

```text
You are working in project V7 Vozduh.

Workspace:
/Users/ponch/Documents/New project

Branch:
Updatesystem

Start by reading these files completely:

1. docs/handoff/V7_SEAMLESS_CHAT_HANDOFF.md
2. docs/handoff/V7_CURRENT_STATE_SNAPSHOT.md
3. docs/handoff/V7_AUTHORITY_BOUNDARY_AND_NEXT_ACTION.md
4. docs/handoff/V7_DO_NOT_REPEAT.md
5. docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
6. docs/reference/V7_CANONICAL_REFERENCE.md
7. docs/reference/SYSTEM_MAP.md
8. docs/reference/V7_AUTONOMY_BLUEPRINT.md
9. docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md
10. docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md

Treat OMP as the execution authority.

Do not invent a new phase.
Do not create a new planner.
Do not create new governance.
Do not create a new execution path.
Do not create a new truth source.
Do not create synthetic evidence.
Do not change floors.
Do not repeat certified audits unless reference/ADR says UNKNOWN, behavior changed, or evidence contradicts the canonical reference.

Current OMP state:
- Highest bottleneck: Suitability.
- Highest leverage action: governed candidate suitability outcome closure.
- Authority boundary: AUTHORITY_BOUNDARY.
- Real world limit: real candidate outcomes have not happened yet.

Current exact packet from latest production dry-run:
- Candidate: 10.7.0.5
- Current channel: vless
- Target channel: awg3
- Packet id: pkt_preview_43f0151499620a00d2e50f7b
- Operation id: govdry_c8f67c5437777091c9cf1f5d
- Selected move hash: 8e7785e058337f1db53fd929d7c175914510a401ff686391bef7bfcb088bfdac
- Rollback target: vless
- Rollback manifest id: rb_preview_d25f7c3f7705ba558d2afcea
- Final verdict: AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY
- Stop reason: explicit operator approval required before restore-barrier write or apply.

First action:
Run read-only verification only:

tools/v7-truth-check --all --json
tools/v7-convergence-status --json
ssh v7-vps /usr/local/bin/v7-autonomy-trust-evidence-inventory
ssh v7-vps /usr/local/bin/v7-governed-canary-dry-run-cycle

Do not run restore-barrier write.
Do not run --apply.
Do not move users.
Do not run rollback apply.
Do not enable daemon/timer/autonomous execution.

If the packet is unchanged, prepare the exact operator approval question for:
10.7.0.5 vless -> awg3

If the packet changed, update OMP and handoff first, then stop at AUTHORITY_BOUNDARY.

Final answer must clearly state:
1. Current packet.
2. Current target.
3. Current authority boundary.
4. What is safe to approve.
5. What must not run without approval.
```
