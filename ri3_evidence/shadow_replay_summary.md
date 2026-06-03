# RI.3 Shadow Replay Summary

Shadow output:

```text
ri3_evidence/ri3_shadow_replay.json
```

Command:

```text
tools/v7-routing-intelligence-shadow --state-dir ri2_evidence/shadow_fixture/state --service-matrix-file ri2_evidence/shadow_fixture/state/service-matrix.json --quality-summary-file ri2_evidence/shadow_fixture/state/egress-quality-summary.json --service-preferences-file ri2_evidence/shadow_fixture/state/service-preferences.json --audit-log ri2_evidence/shadow_fixture/state/client-reconnect-state.json --total-users 20 --affected-users 5 --output ri3_evidence/ri3_shadow_replay.json --pretty
```

Observed shadow facts:

- `schema_version=ri1.shadow-replay.v1`
- `mode=shadow_read_only`
- runtime mutation authority: none
- routing decision authority: none
- governance authority: none
- execution trust score: `70.0`
- dynamic blast radius recommendation: `3`
- service risk input: `24.783`
- platform health input: `75.217`

Planner integration shadow behavior is covered by unit replay:

- old equal-score ordering would keep the lexical/stable order and prefer `a_telegram`;
- RI.3 user-weight influence adds a larger `routing_intelligence` score part to `z_chatgpt`;
- planner selects `z_chatgpt` only because it is already eligible;
- when `z_chatgpt` is marked canary-reserved, planner keeps it blocked and selects `a_telegram` instead.

This proves:

```text
Brain influences ranking.
Planner still owns candidate selection.
Hard gates and reservation still win.
```

