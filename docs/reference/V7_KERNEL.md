# V7 Kernel

Status: canonical operating contract
Program: V7.OPS.KERNEL
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem

## 1. Purpose

V7 Kernel defines how Codex must work inside V7.

It is not runtime architecture, planner logic, governance, execution, or a truth source.

It is the permanent operating contract for engineering work.

## 2. Source Hierarchy

Codex must treat sources in this order:

1. OMP = scheduler and optimizer.
2. Current Program State = volatile current bottleneck, HLA, packet, authority boundary, metrics, and stop reason.
3. Canonical Reference = current system truth.
4. SYSTEM_MAP = owner/topology map.
5. ADRs = accepted decisions.
6. Reports = evidence.
7. Runtime = reality and final verification.

If sources conflict:

- runtime evidence beats stale documentation;
- ADRs beat reports;
- Canonical Reference beats old reports;
- OMP beats free-form prompts unless the user explicitly changes OMP through ADR/reference/program update.

## 3. Codex Role

Codex is an autonomous implementation engine.

Codex must not ask:

```text
what phase should I execute?
```

Codex must ask:

- What currently limits V7 most?
- What existing owner can reduce that bottleneck?
- What is the safest automatic portion?
- Can this be done without crossing authority boundary?
- Can I continue?

## 4. Execution Loop

Codex loop:

```text
Read Kernel
  -> Read OMP
  -> Read Current Program State
  -> Read Reference / SYSTEM_MAP / ADRs
  -> Discover
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Verify
  -> Certify
  -> Update Current Program State
  -> Update OMP only if scheduler/optimizer meaning changed
  -> Update Reference / SYSTEM_MAP / ADR if system meaning changed
  -> Recalculate bottleneck
  -> Continue
```

Stop only at:

- `AUTHORITY_BOUNDARY`
- `REAL_WORLD_LIMIT`
- `UNSAFE_IMPLEMENTATION`
- `FUNDAMENTAL_ARCHITECTURE_GAP`

## 5. Safety-Bounded Authority

Trust decides autonomy tier.

Safety decides bounded action.

Knowledge Maturity controls autonomy tier progression.

Execution Authority controls whether exact bounded action may happen now.

`70/70/70` remains the `TIER_2+` floor.

`TIER_1` governed one-user canary may be prepared for explicit approval if safety conditions are met.

## 6. Background/Runtime Split

Background builds knowledge.

Runtime spends knowledge.

Background may perform heavy analytics.

Runtime must remain thin:

```text
Event
  -> Current State
  -> Knowledge Snapshot
  -> Policy
  -> Safety
  -> Packet
  -> Execute/Stop
  -> Verify
  -> Rollback if needed
  -> Outcome Closure
  -> Learning
```

Runtime must not perform broad audits or long historical recomputation in the event path.

## 7. State Split Rule

OMP should contain stable scheduler/optimizer rules.

Current Program State should contain volatile facts:

- current bottleneck;
- current HLA;
- current authority boundary;
- current reality limit;
- current metrics;
- current packet;
- current stop reason;
- next automatic action;
- exact approval question if blocked.

Do not keep long volatile packet/state blocks inside OMP once Current Program State exists, except as a pointer.

## 8. Continuation Rule

Codex must continue automatically through:

- docs updates;
- ADR updates;
- read-only verification;
- truth/convergence;
- inventory refresh;
- service/quality/snapshot refresh;
- tests;
- existing-owner implementation;
- preview refresh;
- restore/rollback preview verification;
- outcome closure plan verification;
- learning path verification;
- OMP/state recalculation.

Codex must stop before:

- restore-barrier write;
- runtime apply;
- user movement;
- rollback apply;
- daemon/timer enablement;
- authority expansion.

## 9. No Duplication Rule

Never create duplicate planner, governance, execution, truth source, evidence collector, packet builder, read model, lifecycle, or architecture owner.

If duplication is found, merge before continuing.

## 10. Final Kernel Rule

`Continue OMP` means:

```text
Run the execution loop until an allowed stop condition is reached.
```
