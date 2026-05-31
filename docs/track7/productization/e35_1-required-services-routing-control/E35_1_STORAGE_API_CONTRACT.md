# E35.1 Storage and API Contract

Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

storage_api_contract_defined=true

## 1. Storage Strategy

Prefer extending existing truth sources. Do not introduce duplicate group, service or routing-mode truth.

Existing reusable stores:

- `SERVICE_PREFS_FILE` for per-user required services.
- Identity DB `groups` and `organizations` for identity/admin hierarchy.
- `ORG_POLICY_FILE` for group/egress routing policy.
- `users.registry` for current runtime assignment and route table.
- `egress.registry` for channel metadata.
- service matrix state for service health and route-class fitness.

## 2. Entities

### 2.1 Group Routing Controls

Logical object:

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
  "audit": {
    "updated": "",
    "updated_by": ""
  }
}
```

Mapping:

- `group_id`, `display_name` from identity DB `groups`.
- `allowed_channels`, `excluded_channels`, `preferred_channels`, `required_services`, `isolation`, `default_routing_mode` from `org-egress-policy.json.groups[group_id]` or future columns if migrated.

Default:

- `allowed_channels=[]` means all channels allowed.
- `required_services=[]` means no group-specific baseline.
- `default_routing_mode=AUTO`.
- `isolation=shared`.

### 2.2 User Routing Controls

Logical object:

```json
{
  "user_ip": "10.7.0.11",
  "group_id": "default",
  "routing_mode": "AUTO",
  "preferred_channel": "",
  "user_required_services": [],
  "required_service_exemptions": [],
  "effective_required_services": [],
  "current_channel": "1",
  "route_table": "1009"
}
```

Current mapping:

- `user_ip`, `current_channel`, `route_table` from `users.registry`.
- `group_id` from registry group/org fields, org policy user_groups, identity user/allowed-phone mapping or default group.
- `user_required_services` from `SERVICE_PREFS_FILE.users[ip].services`.

Future storage options:

Option A:

- Extend `SERVICE_PREFS_FILE.users[ip]` with `routing_mode`, `preferred_channel`, `required_service_exemptions`.

Option B:

- Add `user_routing_controls` SQLite table.

Recommended:

- Start with JSON-compatible shape in service preferences for low operational complexity.
- Move to SQLite only if query/reporting or audit volume requires it.

### 2.3 Channel Suitability

Derived object, not authoritative storage:

```json
{
  "user_ip": "10.7.0.11",
  "channel_id": "awg1",
  "status": "SUITABLE",
  "hard_blocks": [],
  "soft_preferences": [],
  "required_services": [],
  "service_results": {},
  "capacity": {},
  "safety": {},
  "score": null,
  "explanation": ""
}
```

Do not persist as source of truth. It can be cached with freshness metadata later.

## 3. Read APIs

All read APIs require auth and return redacted operator-safe data.

### `GET /api/routing-control/users`

Purpose:

- list effective routing controls for users.

Query:

- `ip` optional;
- `group_id` optional;
- `routing_mode` optional;
- `status` optional;
- `limit`, `cursor`.

Response:

```json
{
  "items": [
    {
      "user_ip": "10.7.0.11",
      "group_id": "default",
      "routing_mode": "AUTO",
      "preferred_channel": "",
      "current_channel": "1",
      "effective_required_services": ["youtube", "telegram"],
      "current_suitability": {
        "status": "SUITABLE",
        "hard_blocks": [],
        "soft_preferences": ["sticky_current"]
      }
    }
  ],
  "pagination": {}
}
```

### `GET /api/routing-control/users/{ip}`

Purpose:

- detail for one user.

Response includes:

- group;
- current;
- preferred;
- routing mode;
- effective required services;
- candidate channels;
- hard/soft reasons;
- Evidence/Proposal refs.

### `GET /api/routing-control/groups`

Purpose:

- group routing controls summary.

Response:

```json
{
  "items": [
    {
      "group_id": "default",
      "display_name": "Default",
      "allowed_channels": [],
      "required_services": [],
      "default_routing_mode": "AUTO",
      "user_count": 10
    }
  ]
}
```

### `GET /api/routing-control/groups/{group_id}`

Purpose:

- one group detail with channel constraints, linked orgs, users and audit summary.

### `GET /api/routing-control/suitability`

Purpose:

- evaluate user/channel suitability read-only.

Query:

- `user_ip` required;
- `channel_id` optional; if missing, evaluate all channels.

Response:

```json
{
  "user_ip": "10.7.0.11",
  "channels": [
    {
      "channel_id": "1",
      "status": "SUITABLE",
      "hard_blocks": [],
      "soft_preferences": ["sticky_current"],
      "score_summary": {
        "speed": "soft",
        "stability": "pass"
      }
    }
  ]
}
```

### `GET /api/routing-control/services/summary`

Purpose:

- required-services health summary across users/groups.

Response:

- degraded services;
- users affected;
- groups affected;
- channels with no suitable candidate;
- evidence/proposal refs.

## 4. Future Mutation APIs

Mutation endpoints are future/P2 unless a later block explicitly implements them.

Candidate endpoints:

- `POST /api/actions/routing-control/group-update`;
- `POST /api/actions/routing-control/user-mode-update`;
- `POST /api/actions/routing-control/user-required-services-update`;
- `POST /api/actions/routing-control/preferred-channel-set`;
- `POST /api/actions/routing-control/group-allowed-channels-update`.

All future mutations must require:

- auth;
- CSRF;
- role check;
- validation;
- confirmation for risky changes;
- audit append;
- safe mode compatibility;
- no direct runtime movement;
- no autoswitch apply;
- no routing sync.

API rule:

```text
Changing routing controls does not itself move users.
```

Movement may only happen in later blocks through:

```text
Proposal -> Authority Check -> Operator Boundaries -> Routing Mode -> Governance -> Execution -> Verification -> Rollback Capability
```

## 5. Validation Rules

Services:

- must be in `KNOWN_SERVICES`;
- unknown service rejected or quarantined as `UNKNOWN_SERVICE`;
- group-required service cannot be silently removed by user.

Channels:

- must exist in `egress.registry`;
- disabled channel cannot be added as effective candidate;
- execution-only/canary-reserved channels cannot be used as default group allowed channel unless explicitly marked for governed execution.

Routing mode:

- allowed values now: `AUTO`, `OPERATOR_PINNED`;
- `MANUAL` is accepted only as future/reserved display state, not active runtime behavior;
- `OPERATOR_PINNED` requires valid `preferred_channel`.

Group:

- unknown group rejected;
- default group must exist or be synthesized read-only;
- organization link must not imply routing authority unless group policy exists.

## 6. Tests Required For Contract

- Read endpoint shape tests.
- Unknown service validation.
- Group baseline + user additions merge.
- User cannot silently remove group service.
- Allowed channel empty means all.
- Restricted allowed channel blocks all others.
- Pinned mode requires preferred channel.
- Changing settings does not execute runtime movement.
- Safe mode blocks future mutation endpoints where applicable.
- Audit required for future mutation endpoints.
