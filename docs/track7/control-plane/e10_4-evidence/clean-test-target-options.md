# E10.4 Clean Test Target Options

Mode: strategy and approval design only.

## Option A — Dedicated Canary/Test Egress

Description:

- Add or designate one egress for canary/test use only.
- Mark it as reserved from production autoswitch assignment.
- Require Direct/RU and Trusted RU exclusions.
- Require zero users, diagnose OK, quality OK, route table preview, rollback to `vless`.

Risk:

- Requires future bounded mutation or provisioning block.
- If implemented as a new egress, it adds operational surface and must be covered by kill switch, route checks, and provisioning checks.

Blast radius:

- Best isolation when done correctly: one canary user only.

Mutation required:

- Yes, in a separate approval block. Possible changes include egress provisioning, egress metadata, autoswitch eligibility behavior, and target readiness rules.

Direct/RU / Trusted RU risk:

- Low if exclusions are mandatory before any canary.

Expected time to clean target:

- Highest setup work, highest long-term value.

Suitability for second canary:

- Best durable strategy.

## Option B — Temporarily Reserve Existing WireGuard Egress

Description:

- Use `wireguard-1779454504-c43409` as a conditional test target after resolving or explicitly waiving stale-handshake `SUSPECT`.
- Add reservation metadata only in a separately approved block.
- Keep autoswitch from assigning production users while the target is reserved.

Risk:

- Current blocker is `diagnose=SUSPECT`, not quality.
- A stale-handshake waiver can prove mechanics and target diversity, but it is not a clean target canary.

Blast radius:

- One canary user if reservation and quiet/restore lifecycle remain enforced.

Mutation required:

- For true reservation: yes, metadata/autoswitch policy in a separate block.
- For read-only next step: no, run stale-handshake diagnosis first.

Direct/RU / Trusted RU risk:

- Low; WireGuard already has `TRUSTED_RU_SENSITIVE,DIRECT_RU` exclusions.

Expected time to clean target:

- Shortest path to a conditional canary, if diagnose can be resolved or waived.

Suitability for second canary:

- Best short-term fallback. Not clean until `SUSPECT` is resolved.

## Option C — Remediate AWG0/AWG3 Quality and Exclusions

Description:

- Fix or wait for quality to clear on `awg0` / `awg3`.
- Add missing Direct/RU and Trusted RU exclusions only after quality is acceptable.
- Optionally reserve one AWG target for canary.

Risk:

- E10.3 shows both are below quality floor.
- Metadata exclusions alone do not make them clean targets.
- AWG egresses have recent production autoswitch churn.

Blast radius:

- If metadata-only changes are applied while production users are present later, blast radius becomes broader than canary.

Mutation required:

- Eventually yes: metadata exclusions and possibly quality remediation or reservation.

Direct/RU / Trusted RU risk:

- Medium until exclusions are added.

Expected time to clean target:

- Unknown; depends on quality recovery and autoswitch occupation.

Suitability for second canary:

- Not recommended as immediate path.

## Option D — Add New Egress Capacity

Description:

- Provision a new egress dedicated to canary/small-cohort testing.
- Keep it out of normal autoswitch assignment until promoted.

Risk:

- Provisioning and kill-switch/routing coverage must be verified.
- Requires a separate deploy/provisioning approval block.

Blast radius:

- Can be lowest if created as isolated canary-only target.

Mutation required:

- Yes, separate provisioning and metadata approval.

Direct/RU / Trusted RU risk:

- Low if exclusions and route-class policy are part of the initial definition.

Expected time to clean target:

- Medium/high setup cost, best long-term capacity path.

Suitability for second canary:

- Best if the project wants repeatable canaries and small cohorts.

## Option E — Accept Occupied Target Canary

Description:

- Use an already occupied target such as `1`.

Risk:

- Not clean isolation.
- Target behavior is already influenced by production load.
- It weakens attribution and can mix canary movement with autoswitch recovery.

Blast radius:

- Canary command can remain one-user, but target state is not isolated.

Mutation required:

- User movement if executed; forbidden in this block.

Direct/RU / Trusted RU risk:

- Low for target `1` metadata, but not an isolation-safe canary target.

Expected time to clean target:

- Immediate but weak evidence.

Suitability for second canary:

- Not preferred. Only acceptable for mechanics under explicit waiver, not for clean target validation.

## Recommendation

Primary:

```text
Option B next as read-only diagnosis: WireGuard stale-handshake root-cause and reservation feasibility packet.
```

Reason:

- WireGuard is zero-user.
- WireGuard quality passes floor.
- WireGuard already has Direct/RU + Trusted RU exclusions.
- The remaining blocker is focused: `SUSPECT` stale handshake.

Fallback:

```text
Option A/D: create a dedicated canary/test egress with reservation semantics.
```

Reason:

- Durable, repeatable, and better than waiting for production egresses to happen to be clean.

