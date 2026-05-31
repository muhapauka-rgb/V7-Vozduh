# E35.1 Test Plan

Runtime mutation: NO
User movement: NO
Routing/apply/autoswitch apply: NO

test_plan_defined=true

## 1. Required Services Merge Tests

### Group baseline

Given:

- group `default.required_services=["telegram","google_auth"]`;
- user has no user-level services.

Expect:

- effective services include `telegram`, `google_auth`;
- no fallback defaults are added unless group policy says inherit defaults.

### User additions

Given:

- group baseline `telegram`;
- user services `youtube`, `chatgpt`.

Expect:

- effective services are `telegram`, `youtube`, `chatgpt`.

### No silent removal

Given:

- group requires `telegram`;
- user edits services to only `youtube`.

Expect:

- effective services still include `telegram`;
- any exemption requires explicit `required_service_exemptions` and audit.

### Unknown service

Given:

- user services include `unknown_service`.

Expect:

- write endpoint rejects it; or read model marks `UNKNOWN_SERVICE`;
- high-confidence proposal is blocked.

## 2. Group Allowed Channels Tests

### Default all allowed

Given:

- group `allowed_channels=[]`.

Expect:

- all otherwise eligible channels are allowed.

### Restricted list

Given:

- group `allowed_channels=["awg1"]`.

Expect:

- `awg1` can pass group gate;
- all other channels get hard block `not_in_group_allowed_pool`.

### Excluded channel

Given:

- group `excluded_channels=["vless"]`.

Expect:

- `vless` gets hard block `excluded_by_group_policy`.

### Disabled channel

Given:

- channel exists but `enabled=0`.

Expect:

- hard block `egress_disabled`.

## 3. Suitability Tests

### Required service down

Given:

- user requires `telegram`;
- Telegram state is `DOWN`.

Expect:

- candidate hard-blocked;
- speed score ignored.

### Required service degraded

Given:

- required service is degraded but not hard down.

Expect:

- behavior follows policy:
  - soft reason for warning/grace;
  - hard block if persistent or critical threshold reached.

### Speed cannot override hard block

Given:

- fastest channel is not allowed by group or fails Telegram.

Expect:

- channel remains hard-blocked.

### Capacity cannot be ignored

Given:

- channel has hard capacity full.

Expect:

- hard block `planned_hard_full` or capacity-equivalent reason.

### Stability can override speed

Given:

- faster channel stability below floor;
- slower channel stability OK.

Expect:

- faster channel hard-blocked;
- slower channel remains candidate.

## 4. Routing Modes Tests

### AUTO

Given:

- user mode `AUTO`.

Expect:

- any suitable group-allowed channel can be proposed after gates.

### OPERATOR_PINNED healthy

Given:

- user mode `OPERATOR_PINNED`;
- preferred channel suitable;
- another channel faster.

Expect:

- keep preferred channel;
- no movement proposal based solely on speed.

### OPERATOR_PINNED emergency move

Given:

- preferred channel hard-fails or required service unavailable.

Expect:

- emergency proposal may be generated;
- target must still satisfy group allowed channels and required services;
- governance still required.

### MANUAL reserved

Given:

- user mode `MANUAL`.

Expect:

- display only or reject as active behavior until future block.

## 5. Admin/API Tests

Read surfaces:

- `/api/routing-control/users`;
- `/api/routing-control/users/{ip}`;
- `/api/routing-control/groups`;
- `/api/routing-control/groups/{group_id}`;
- `/api/routing-control/suitability`;
- `/api/routing-control/services/summary`.

Expected:

- authenticated;
- redacted;
- stable response shape;
- no mutation.

Future mutation endpoints:

- require auth;
- require CSRF;
- require role;
- require confirmation for risky changes;
- append audit;
- respect safe mode;
- never call `v7-user-switch`, `v7-routing-sync`, autoswitch apply or policy apply.

## 6. Regression Tests

- Evidence APIs still read-only.
- Proposal APIs still read-only.
- Runtime Trust APIs still read-only.
- Release Trust APIs still read-only.
- Proposal remains non-authoritative.
- Policy remains admission logic, not mutation authority.
- Capacity remains a gate, not authority.
- Approval packet governance unchanged.

## 7. Dangerous-Call Scan

Scan must confirm E35.1 work does not introduce:

- `v7-user-switch`;
- `v7-routing-sync`;
- `v7-users-autoswitch --apply`;
- `v7-policy-apply`;
- Direct RU mutation;
- Trusted RU refresh/diagnostic mutation;
- kill switch mutation;
- service restart.

## 8. Suggested Immediate Checks For This Block

Since E35.1 is documentation/modeling only:

```text
git diff --check
rg -n "v7-user-switch|v7-routing-sync|v7-users-autoswitch --apply|v7-policy-apply|systemctl restart|kill switch mutation" docs/track7/productization/e35_1-required-services-routing-control BLOCK_E35_1_REQUIRED_SERVICES_ROUTING_CONTROL_MODEL_REPORT.md
```

If pure helper code is added later:

```text
python3 -m py_compile <touched python files>
python3 -m unittest <targeted tests>
```

## 9. Pass Criteria

tests_passed=true requires:

- all E35.1 docs created;
- model includes product/admin/runtime/storage/API/tests mapping;
- no runtime mutation;
- no movement command added/executed;
- no routing apply command added/executed;
- git diff whitespace check clean.
