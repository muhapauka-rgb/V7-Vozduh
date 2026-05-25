# V7 Phase 3 - Autoswitch Explainability

## Purpose

Autoswitch is a stability preservation system. Observability must explain why it acted or did not act.

## Required Explanation Fields

Each switch decision should include:

- triggering service or health signal;
- duration of degradation;
- current egress state;
- candidate egress state;
- cooldown status;
- anti-flap status;
- confidence or eligibility reason;
- bounded impact;
- rollback context.

## Good Explanation

Example:

- Telegram degraded for 38 seconds;
- packet loss/reconnect signals increased;
- alternate path stable;
- cooldown satisfied;
- selected one user move;
- kill switch unchanged.

## Bad Explanation

Bad:

- `switched`;
- `AI recommends migration`;
- `latency better`;
- empty reason.

## Did-Not-Switch Reasons

Must explain:

- cooldown active;
- user frozen;
- no healthy target;
- target quarantined;
- route class mismatch;
- trusted RU unsafe fallback prevented;
- confidence too low.

## UI Boundary

Show the short reason first. Put full scoring and candidate lists in drill-down.
