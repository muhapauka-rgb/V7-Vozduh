# E35.B Authority Domains

## Final Domains

E35.B defines these domains:

1. Safety Domain
2. Containment Domain
3. Governance Domain
4. Operator Domain
5. Group Domain
6. User Domain
7. Autoswitch Domain
8. Scheduler Domain

## Safety Domain

Purpose:

Protect runtime and users from unsafe movement.

Owner:

Runtime trust, safety gates, kill-switch state, restore-settle, checker health.

Scope:

All forward movement and emergency eligibility.

Maximum authority:

May block all forward movement.

Non-negotiable limits:

Cannot be bypassed by operator, autoswitch, scheduler, group or proposal.

Override rights:

Can override every other domain for forward denial.

Audit requirements:

Every safety block must be explainable and visible.

## Containment Domain

Purpose:

Reduce harm when current state is unsafe.

Owner:

Containment/rollback logic, emergency authority.

Scope:

Emergency escape, rollback, return to known safe state.

Maximum authority:

May override operator pin/manual only for hard safety/service/runtime failure.

Non-negotiable limits:

Cannot use emergency authority for speed, score, convenience or normal rebalance.

Override rights:

May override Operator/Group/User/Autoswitch only for containment.

Audit requirements:

Must record trigger, scope, source target, emergency target, expiry and return plan.

## Governance Domain

Purpose:

Bound approved execution.

Owner:

Approval packets, execution-time recheck, replay protection, audit chain.

Scope:

Exact allowed users, targets, budget, expiry and rollback.

Maximum authority:

May authorize movement inside packet scope after all hard gates pass.

Non-negotiable limits:

Cannot bypass Safety.

Override rights:

May override Operator/Group only when packet explicitly declares that override and safety allows.

Audit requirements:

Every decision must be append-only and replay-resistant.

## Operator Domain

Purpose:

Human ownership of routing intent.

Owner:

Admin operator.

Scope:

Pin, unpin, manual mode, explicit target intent, direct manual action.

Maximum authority:

Can block autoswitch and set per-user routing intent.

Non-negotiable limits:

Cannot bypass Safety or invalid/stale governance packet checks.

Override rights:

Can override Autoswitch and User preference. Can override Group only if group policy permits operator exception or governance records explicit override.

Audit requirements:

Actor, reason, evidence/proposal link and expiry must be recorded.

## Group Domain

Purpose:

Define routing/policy boundaries for sets of users.

Owner:

Operator-managed group policy.

Scope:

Allowed/excluded channels, required services, default routing mode, isolation.

Maximum authority:

Can block channel eligibility for group members.

Non-negotiable limits:

Cannot override Safety, Governance scope or Containment.

Override rights:

Can constrain Autoswitch. May constrain Operator unless operator override is explicitly allowed and audited.

Audit requirements:

Group policy changes and group/user conflict outcomes must be visible.

## User Domain

Purpose:

Represent user needs without giving user direct routing control.

Owner:

Operator-managed user preferences; future user requests only.

Scope:

Required services, maybe future route request/feedback.

Maximum authority:

May influence suitability and proposals.

Non-negotiable limits:

Cannot move self, pin self or override operator/group/safety/governance.

Override rights:

None for routing mutation.

Audit requirements:

User-driven input must be distinguishable from operator authority.

## Autoswitch Domain

Purpose:

System-managed movement for AUTO users.

Owner:

Autoswitch planner/apply path.

Scope:

AUTO users only, eligible targets only, bounded by all hard gates.

Maximum authority:

May propose and later apply movement for AUTO users.

Non-negotiable limits:

Cannot override Safety, Governance, Operator pin/manual, Group hard constraints, required services or capacity.

Override rights:

None over higher domains.

Audit requirements:

Must explain selected and denied moves.

## Scheduler Domain

Purpose:

Future timing/orchestration of already authorized work.

Owner:

Future scheduler.

Scope:

Queue, reserve, start recheck for approved batches.

Maximum authority:

May launch only work already admitted by authority/governance/policy.

Non-negotiable limits:

Cannot create movement authority.

Override rights:

None.

Audit requirements:

Must record scheduling decisions and skipped/expired work.

## Verdict

```text
authority_domains_defined=true
```
