# E35.A Implementation Readiness

## Classification

| Area | Classification | Reason |
|---|---|---|
| `users.registry` | Reuse | Current runtime assignment truth. |
| `egress.registry` | Reuse | Channel identity/static metadata truth. |
| Org policy | Extend | Already holds group/channel policy; add group defaults carefully. |
| Service preferences | Reuse | Required services already modeled; do not overload with authority. |
| Autoswitch | Extend | Add authority gate before selected move acceptance/apply. |
| Operator execution | Extend | Add authority check/override metadata before movement execution. |
| Approval packets | Extend | Include authority state hash and protected-user override fields. |
| Evidence | Extend | Link authority events/decisions. |
| Proposal | Extend | Show authority outcome and required review. |
| Runtime Trust | Reuse | Hard block input. |
| Release Trust | Reuse | Hard block/input when relevant. |
| Admin API | Extend | Add read/preview authority endpoints, later mutation endpoints. |
| Admin UI | Extend | Users/Channels/Settings/Logs/Home. |
| `pending_profiles.route_mode` | Do Not Touch | Not live routing ownership. |
| Sticky score | Do Not Touch | Keep as soft preference. |
| Group preferred egress | Do Not Touch/Reuse | Soft preference only. |
| Execution-only target isolation | Do Not Touch | Certified safety-critical model. |

## Implementation Order

### Step 1: Authority Store

- `routing-authority.json`
- `routing-authority-events.jsonl`
- loader/normalizer;
- effective authority resolver.

### Step 2: Read APIs

- list users authority;
- get one user authority;
- list events;
- decision preview.

### Step 3: Admin Visibility

- Users drawer authority section;
- Channels pinned users;
- Logs event filters;
- Home summaries.

### Step 4: Autoswitch Gate

- evaluate authority before selected moves become actionable;
- explain denied-by-authority candidates.

### Step 5: Governance Integration

- include authority hash in approval packet;
- include protected user override reason.

### Step 6: Write APIs

- set AUTO;
- set MANUAL;
- pin/unpin;
- expiry.

All write APIs must be non-movement authority-state mutations only.

## Build Readiness

Implementation can begin after E35.A because:

- current truth sources are identified;
- missing model is explicit;
- admin surfaces are known;
- runtime gate insertion points are known;
- test plan is defined.

Remaining decisions:

1. JSON store vs SQLite for first authority store.
2. Default pin expiry: none vs bounded default.
3. Whether `MANUAL` write action ships in first implementation or visible/read-only first.

Recommended:

- JSON store first;
- persistent pin by default;
- MANUAL modeled and visible, mutation gated behind explicit operator action.

## Verdict

```text
implementation_ready=true
e35_b_ready=true
```
