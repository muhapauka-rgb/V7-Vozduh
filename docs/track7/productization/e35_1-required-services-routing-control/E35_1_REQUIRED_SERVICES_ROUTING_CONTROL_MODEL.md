# E35.1 Required Services & Routing Control Model

Block: E35.1
Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

## Model Decision

required_services_model_defined=true
channel_suitability_model_defined=true
group_model_defined=true
routing_modes_semantics_defined=true

E35.1 defines Required Services and Groups as routing-control inputs. They are not execution authority. They constrain proposal, suitability, admission and future execution-time recheck.

## 1. Required Services Model

Product meaning:

Required Services are the services a user or group expects to work through V7. Examples: YouTube, Instagram, Telegram, Google, Google Auth, ChatGPT, Claude, OpenAI Auth.

Operator meaning:

When an operator selects required services, V7 must treat them as suitability and admission inputs, not cosmetic preferences.

Runtime mapping:

- Existing per-user preferences: `SERVICE_PREFS_FILE` via `service_preferences_state()`.
- Existing known services: `SERVICE_CATALOG`.
- Existing route-class map: `ROUTE_CLASS_SERVICE_MAP`.
- Existing matrix evidence: `service_matrix_state()`.
- Existing autoswitch service gates: `_required_services()`, `_important_services()`, `_gate_service()`.

### Required Service Sources

1. System fallback default:

```text
DEFAULT_USER_PRIORITY_SERVICES = youtube, instagram, telegram, google, google_auth
```

2. Group baseline required services:

```text
group.required_services[]
```

3. User additions:

```text
user.required_services[]
```

4. Future explicit exception:

```text
user.required_service_exemptions[]
```

Exemptions must be explicit, audited and visible. Silent removal is forbidden.

### Merge Rule

Effective required services:

```text
effective_required_services =
  normalize(
    group.required_services
    UNION user.required_services
    UNION fallback_default_when_no_group_or_user_services_exist
  )
  MINUS explicit_user_exemptions_if_allowed_and_audited
```

Recommended behavior:

- Group defines a baseline.
- User may add extra services.
- User cannot silently remove group-required services.
- If group has required services, fallback defaults are not automatically added unless group policy says `inherit_defaults=true`.
- Unknown service IDs are rejected at write time or marked `UNKNOWN_SERVICE` and block high-confidence proposal.

### Service State Semantics

| Service state | Meaning | Suitability impact |
|---|---|---|
| OK | Service works on channel. | Pass |
| DEGRADED | Service works poorly or in grace. | Soft penalty or hard block if policy says strict |
| DOWN | Service unavailable. | Hard block |
| NOT_STARTED | Telegram/sentinel not ready or unavailable. | Hard block for Telegram-required users |
| UNKNOWN | Evidence missing/stale. | Review required; no high-confidence autonomous movement |
| MISSING | Service not present in matrix for candidate. | Hard block for strict required service; review for advisory mode |

## 2. Channel Suitability Model

Channel Suitability answers:

```text
Can this channel safely serve this user now?
```

A channel is suitable only if all hard gates pass.

Hard gates:

1. Runtime safety:
   - runtime trust not blocking;
   - release trust not blocking when forward movement depends on release provenance;
   - kill switch/routing trust safe;
   - no selected moves;
   - no hidden movers.

2. Channel basics:
   - channel enabled;
   - channel not maintenance/disabled/quarantine;
   - channel health code acceptable;
   - channel severity not failing;
   - channel not `manual_only` for automation;
   - reserved/canary/execution-only target not used outside explicit governance.

3. Group constraints:
   - group allows channel;
   - channel not excluded by group;
   - channel exclusive_group compatible;
   - channel group ACL compatible;
   - group isolation not violated.

4. Required services:
   - every effective required service is available or acceptable under policy;
   - Telegram hard states block Telegram-required users;
   - persistent service failure blocks;
   - multiple critical service failures block;
   - route-class fitness FAIL blocks.

5. Route compatibility:
   - candidate role/service tags match route class or route-class fitness is acceptable;
   - Trusted RU requires trusted path;
   - route class not excluded by channel metadata.

6. Capacity:
   - hard limit not exceeded;
   - available capacity sufficient;
   - capacity status certified/fresh enough for forward movement.

7. Safety:
   - egress not quarantined;
   - target not blocked for user;
   - anti-flap pair reversal window not violated;
   - user not frozen by switch history.

Soft preferences only apply after all hard gates pass.

## 3. Hard Block vs Soft Preference

### Hard Blocks

Hard Block means: candidate must not be selected for forward movement even if faster.

Hard blocks:

- channel disabled;
- channel maintenance/disabled/quarantine;
- manual-only channel for automated assignment;
- execution-only/canary reserved target without explicit governance;
- group does not allow channel;
- group excludes channel;
- channel exclusive to another group;
- group isolation violation;
- required service unavailable in hard state;
- Telegram required and hard down;
- persistent service failure;
- multiple critical services failed;
- route-class fitness FAIL;
- Trusted RU required but target not trusted;
- avg Mbps below floor;
- min Mbps below floor;
- stability below floor;
- target hard capacity exceeded;
- safety quarantine;
- target blocked for user;
- pair reversal stability window;
- runtime trust blocking;
- kill switch/routing trust unsafe;
- missing execution governance for movement.

### Soft Preferences

Soft Preference means: can influence score only after hard gates pass.

Soft preferences:

- better speed;
- better latency;
- lower load;
- better service score;
- route role exact match;
- group preferred egress;
- current sticky channel;
- higher stability above floor;
- improving quality history;
- preferred protocol/geography if not a hard rule.

Rule:

```text
hard_blocks > safety > capacity > required_services > routing_mode > stability > sticky > speed
```

Speed never overrides hard blocks.

## 4. Group Model

E35.1 evolves the current Organizations concept into a clearer Groups routing-control model.

Existing reality:

- `organizations` are identity/admin metadata.
- `groups` already exist in identity DB and carry `route_policy`.
- `org-egress-policy.json` already has group and egress policy sections.

Final product meaning:

Group is a routing/policy container for users.

Canonical fields:

```json
{
  "group_id": "default",
  "display_name": "Default",
  "allowed_channels": [],
  "excluded_channels": [],
  "preferred_channels": [],
  "required_services": [],
  "default_routing_mode": "AUTO",
  "isolation": "shared",
  "future_policies": {},
  "audit": {
    "created_at": "",
    "updated_at": "",
    "updated_by": ""
  }
}
```

Default behavior:

- all channels allowed when `allowed_channels=[]`;
- no group-specific required services unless configured;
- default routing mode `AUTO`;
- isolation `shared`;
- existing organization can link to group;
- user can be assigned to group through identity/user mapping.

Mapping to existing storage:

- Existing `groups` table remains identity source.
- Existing `org-egress-policy.json.groups` becomes routing policy source.
- E35 implementation should either:
  - extend `groups` table with routing-control columns; or
  - keep identity in SQLite and routing policy in `org-egress-policy.json`, but expose one merged read API.

Do not create a third parallel group source.

## 5. Final Priority Chain

The E35.1 priority chain:

```text
Safety / runtime trust
-> group allowed channels
-> user/group required services
-> route-class compatibility
-> capacity hard gates
-> operator routing mode constraints
-> stability
-> sticky preference
-> speed/score
-> proposal/governance admission
-> execution-time recheck later in E35.D/P2
```

Interpretation:

- Safety and trust are first because an unsafe runtime cannot execute forward movement.
- Group allowed channels come before scoring because group constraints are hard business boundaries.
- Required services come before speed because service availability is the user's product expectation.
- Capacity comes before score because an overloaded target is not suitable.
- Routing mode constrains whether the system may move a user or must keep a preferred channel.
- Stability precedes speed because V7 optimizes reliable access, not raw throughput alone.
- Proposal/governance never runs before suitability; it receives a bounded, explainable candidate set.

## 6. Routing Modes

### AUTO

System-managed routing.

Rules:

- System may choose any suitable allowed channel after proposal/admission/governance.
- Required services can hard-block unsuitable channels.
- Speed can help rank candidates after hard gates pass.
- Execution still requires future governance path.

### OPERATOR_PINNED

Operator-preferred channel with emergency escape.

Fields:

```text
routing_mode=OPERATOR_PINNED
preferred_channel=<egress_id>
```

Rules:

- If preferred channel is healthy and suitable, keep user there.
- Do not move only because another channel is faster.
- Emergency move is allowed only when:
  - preferred channel hard-fails;
  - preferred channel degrades below floor;
  - required services become unavailable;
  - capacity/safety/governance permits;
  - emergency target is group-allowed and required-service suitable.
- Emergency movement must be visible as proposal/governance, not hidden runtime mutation.

### MANUAL

Future reserved.

Do not activate runtime behavior in E35.1. If a legacy `MANUAL_ONLY` channel exists, treat it as channel metadata, not user routing mode.

Future semantics may be:

- operator-only movement;
- no autonomous movement except containment rollback;
- high-friction confirmation for every change.

## 7. Product Guarantees and Non-Guarantees

Guaranteed by this model:

- Required services become first-class suitability/admission inputs.
- Group allowed channels become hard constraints.
- Speed cannot override hard blocks.
- Pinned users do not move just because a faster channel exists.
- Current channel is distinguished from preferred channel.

Not guaranteed until later implementation blocks:

- Runtime execution-time recheck includes required-services and group constraints.
- Admin mutation endpoints fully implement group routing-control writes.
- Autoswitch planner fully consumes the new `routing_mode/preferred_channel` fields.
- Autonomous execution is enabled.

## 8. Reality-First Mapping

Product Capability:

- Required Services & Routing Control.

Admin Surface:

- Users drawer, Channel drawer, Routing, Settings/Groups, Main summary.

Runtime Service:

- service matrix, autoswitch planner, route dry-run, evidence/proposal, future batch/policy/concurrency gates.

Storage:

- service preferences store, identity DB groups/organizations, org-egress-policy, future user routing controls.

API:

- existing `/api/policy`, `/api/org-egress-policy`, `/api/users`, `/api/egress`, `/api/proposals`, `/api/evidence`;
- future read APIs for effective routing controls and suitability.

UI Component:

- chips, drawers, group editor, suitability cards, hard-block reason list.

Tests:

- merge rules, group gates, pinned behavior, hard/soft matrix, no mutation.
