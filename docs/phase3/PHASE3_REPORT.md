# V7 Phase 3 - Observability And Diagnostics Report

## Scope

Phase 3 was applied as a bounded, non-runtime-changing pass.

Implemented:

- unified health model for all platform objects;
- service matrix maturity model;
- route diagnostics engine contract;
- incident timeline model;
- client path awareness model;
- datapath visibility model;
- autoswitch explainability model;
- trusted RU observability model;
- alert/history model;
- compact operator UX model;
- read-only observability summary tool.

Not changed:

- datapath;
- nftables;
- route tables;
- autoswitch behavior;
- service matrix probe behavior;
- Telegram sentinel behavior;
- admin UI;
- systemd timers.

## Findings From Inspection

Current project already has strong observability foundations:

- `tools/v7-service-matrix-test` checks HTTP services and Telegram TCP endpoints per egress.
- `tools/v7-service-matrix-refresh-all` refreshes all enabled egress and writes summary/events.
- `tools/v7-telegram-sentinel` gives fast Telegram-specific degradation signal and cooldown-aware autoswitch hooks.
- `tools/v7-egress-quality-compact` builds bounded EMA/ring summaries.
- `tools/v7-path-benchmark` and `tools/v7-path-sample-ingest` cover server and client path awareness.
- `tools/v7-users-autoswitch` already emits explainable plan summaries, safety bounds, reconnect events, and quality history references.
- `admin/v7-admin-api` exposes service matrix, service recommendations, route-class dry-run, trusted RU/direct policy surfaces, and autoswitch dry-run/apply views.

Main gaps formalized:

- no single compact operator summary contract;
- incident/event model was implicit;
- trusted RU observability needed explicit unsafe-fallback-prevented language;
- diagnostics needed grouped cause categories;
- historical quality needed a bounded, decision-support framing.

## Verification Principle

Observability must answer:

`what is happening -> who is affected -> why likely -> what safe action is next`

It must not default to showing everything.

## Next Phase Gate

Do not proceed to Phase 4 until explicitly instructed.
