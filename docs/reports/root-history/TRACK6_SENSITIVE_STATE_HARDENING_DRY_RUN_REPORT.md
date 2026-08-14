# V7 Vozduh — Track 6 Sensitive-State Hardening Dry Run & Access Mapping Report

Generated: 2026-05-23

## Scope

Track 6 performed a sensitive-state hardening dry run.

No chmod/chown was applied.
No runtime state was changed.
No routing/datapath/autoswitch/Trusted RU/Gosuslugi logic was touched.
No live deploy was performed.

Added one read-only validator:

- `tools/v7-sensitive-state-check`

Added one access map:

- `docs/track6/SENSITIVE_STATE_ACCESS_MAP.md`

## 1. Sensitive-State Inventory

Track 6 target files:

| File | Sensitivity | Runtime Criticality | Current Known Live Baseline | Risk |
|---|---|---|---|---|
| `/opt/v7/egress/state/profile-delivery-tokens.json` | High | profile delivery / onboarding | Track 4: `0644 root:root` | Commercially unsafe until access model is confirmed |
| `/opt/v7/admin/v7-identity.db` | High | identity / devices / onboarding | Track 4: `0600 root:root` | Controlled |
| `/etc/v7/policy.json` | Medium | autoswitch hard policy | Track 4: `0644 root:root` | Legacy-operational, commercially weak |
| `/etc/v7/org-egress-policy.json` | Medium | org / egress eligibility | Track 4: `0644 root:root` | Legacy-operational, commercially weak |
| `/opt/v7/egress/state/users.registry` | Medium | active user routing assignments | Track 4: `0644 root:root` | Medium exposure, high runtime sensitivity |
| `/opt/v7/egress/state/egress.registry` | Medium | egress lifecycle / routing | Track 4: `0644 root:root` | Medium exposure, high runtime sensitivity |
| `/opt/v7/egress/state/autoswitch-safety.json` | Medium | anti-flap / freeze / quarantine memory | Track 4: `0644 root:root` | Medium exposure, writer-sensitive |
| `/opt/v7/egress/state/client-reconnect-state.json` | Medium | client experience / autoswitch signal | Track 4: `0644 root:root` | Medium exposure, writer-sensitive |

Local dry-run result:

```text
tools/v7-sensitive-state-check --pretty
total=8 existing=0 missing=8
```

This is expected on the local repo machine because live `/opt/v7` and `/etc/v7` state is not present locally.

Live re-check attempt:

```text
ssh BatchMode read-only metadata check -> Permission denied (publickey,password)
```

No live metadata was changed or read beyond the failed authentication attempt.

## 2. Runtime Access Map

### `profile-delivery-tokens.json`

Readers:

- `admin/v7-admin-api`:
  - `profile_delivery_state`
  - `profile_delivery_prune`
  - `profile_delivery_active_row`
  - `profile_delivery_rows`
  - public `/profile-import/<token>`
  - public `/profile-delivery/<token>`
- `tools/v7-identity-consistency-review` read-only validation.

Writers:

- `admin/v7-admin-api`:
  - `create_profile_delivery`
  - `consume_profile_delivery`
  - `revoke_profile_delivery`
  - `revoke_profile_deliveries_for_ip`
  - `profile_delivery_prune`

Access requirement:

- admin API/profile delivery process must be able to read/write.
- public delivery must not require world-readable token state if served by the same privileged admin process.

### `v7-identity.db`

Readers/writers:

- `admin/v7-admin-api` identity lifecycle:
  - users;
  - devices;
  - organizations;
  - groups;
  - pending profiles;
  - connect sessions;
  - provisioning jobs.

Readers:

- `tools/v7-identity-consistency-review`.

Access requirement:

- admin API must read/write SQLite.
- current `0600` is expected and already enforced by `identity_init_db`.

### `policy.json`

Readers:

- admin API;
- `tools/v7-users-autoswitch`;
- `tools/v7-autoswitch-safety-review`;
- `tools/v7-observability-summary`.

Writers:

- admin API policy update path;
- operator maintenance.

Access requirement:

- autoswitch timer must read.
- admin API must read/write.

### `org-egress-policy.json`

Readers:

- admin API;
- autoswitch;
- observability summary;
- identity consistency review.

Writers:

- admin API `org-egress-policy-update`;
- operator maintenance.

### `users.registry`

Readers:

- admin API;
- autoswitch;
- kill switch check;
- provisioning reconcile check;
- observability summary;
- identity consistency review;
- client speed API.

Writers:

- admin/provisioning/user lifecycle flows;
- external provisioning/user switch tools.

### `egress.registry`

Readers:

- admin API;
- autoswitch;
- service matrix;
- Telegram sentinel;
- kill switch/reconcile checks;
- observability summary.

Writers:

- admin egress lifecycle flows;
- egress state/provisioning tools.

### `autoswitch-safety.json`

Readers:

- autoswitch;
- autoswitch safety review;
- observability summary;
- admin diagnostics.

Writers:

- `tools/v7-users-autoswitch`.

### `client-reconnect-state.json`

Readers:

- autoswitch;
- autoswitch safety review;
- observability summary;
- admin diagnostics.

Writers:

- autoswitch planning/apply paths;
- client telemetry tools if enabled.

## 3. Permission Risk Matrix

| File Class | Current Posture | Classification | Why |
|---|---|---|---|
| Profile delivery tokens | Track 4: `0644` | Commercially unsafe | Token-bearing state should not be world-readable unless there is a proven runtime requirement. |
| Identity DB | Track 4: `0600` | Acceptable / controlled | Strong permission already in place; do not loosen. |
| Policy files | Track 4: `0644` | Legacy-but-tolerable, commercially weak | Reveals hard routing/autoswitch/org eligibility policy. |
| Registries | Track 4: `0644` | Legacy-but-tolerable, commercially weak | Reveals users, assignments, topology, active egress state. |
| Autoswitch safety | Track 4: `0644` | Medium | Reveals freeze/quarantine/anti-flap state. Writer-sensitive. |
| Reconnect state | Track 4: `0644` | Medium | Reveals user-impact/reconnect signals. Writer-sensitive. |

## 4. Commercial Exposure Analysis

Highest commercial risk:

- `profile-delivery-tokens.json`

Why:

- token-related delivery state;
- may link delivery token hints, profile paths, user IPs, adapters/modes, status timestamps;
- dangerous in multi-tenant/commercial context if readable beyond the service account.

Tenant/isolation risk:

- `users.registry`;
- `egress.registry`;
- `org-egress-policy.json`;
- identity DB if permissions ever loosen.

Operator trust risk:

- policy and autoswitch state exposed as world-readable creates weak operational boundaries.

## 5. Dry-Run Hardening Simulation

### `profile-delivery-tokens.json -> 0600`

Potential benefit:

- removes world-readable token-state exposure.

Potential breakage:

- breaks profile delivery if public delivery/import is served by a different non-root process;
- breaks profile issue/revoke/prune if admin API is not owner;
- breaks identity consistency review if that tool runs as non-owner.

Dry-run verdict:

- safest first candidate, but only after live service-user confirmation.

### `policy.json` and `org-egress-policy.json -> 0640`

Potential benefit:

- reduces world-readable hard policy exposure.

Potential breakage:

- autoswitch cannot read policy if timer user is outside group;
- admin API cannot update if owner/group wrong;
- observability summary loses policy context.

Dry-run verdict:

- good Stage 2 candidate after explicit service group model.

### `users.registry` and `egress.registry -> root-only`

Potential benefit:

- reduces topology/user assignment exposure.

Potential breakage:

- autoswitch, sentinel, service matrix, kill switch checks and reconciliation can fail.

Dry-run verdict:

- do not harden first. Requires full service-user and writer mapping.

### `autoswitch-safety.json` and `client-reconnect-state.json -> 0640`

Potential benefit:

- reduces visibility into safety/client instability state.

Potential breakage:

- autoswitch cannot update anti-flap/freeze or reconnect signals if writer lacks access.

Dry-run verdict:

- only after autoswitch writer identity is confirmed.

## 6. Safe Hardening Sequencing

Stage 1 — read-only confirmation:

- run `tools/v7-sensitive-state-check --pretty` on the VPS;
- collect live `systemctl show -p User -p Group -p ExecStart ...` for admin API, autoswitch, sentinel, service matrix, quality compactor, public gateway;
- confirm whether runtime is fully root-run or uses service users/drop-ins.

Stage 2 — first candidate preview:

- profile delivery token state only;
- prepare metadata backup:
  - path;
  - mode;
  - owner/group;
  - sha256;
  - mtime;
- test whether admin/profile delivery process can read/write as target owner.

Stage 3 — one-file apply with rollback:

- if confirmed root-owned/root-run, apply `0600` to `profile-delivery-tokens.json` only;
- verify create/download/revoke profile delivery;
- rollback immediately if any failure.

Stage 4 — policy/registry group model:

- introduce explicit service group only if needed;
- avoid recursive chmod/chown;
- change one file class per rollout.

## 7. Operator UX Warning Model

Recommended calm summary:

```text
Sensitive-state warnings: 2
Commercial exposure: medium/high
Profile token exposure: high
Runtime-safe hardening candidate: profile delivery tokens, pending service-user confirmation
Identity DB: controlled
Policy/registry hardening: staged only
```

Do not show:

- raw token data;
- full registry contents;
- noisy file list walls;
- secret-bearing JSON snippets.

## 8. Exact Files / Tools / Docs Created

Created:

- `tools/v7-sensitive-state-check`
- `docs/track6/SENSITIVE_STATE_ACCESS_MAP.md`
- `TRACK6_SENSITIVE_STATE_HARDENING_DRY_RUN_REPORT.md`

Changed:

- none of the production runtime files;
- no admin behavior files for Track 6.

## 9. Verification Results

Command:

```bash
tools/v7-run-tests
```

Result:

- OK;
- 28 tests discovered and passed;
- py_compile OK.

Command:

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py admin_core/events.py tools/v7-sensitive-state-check
```

Result:

- OK.

Command:

```bash
tools/v7-sensitive-state-check --pretty
```

Local result:

- OK;
- 8 target paths missing locally;
- no mutation.

Live check:

- read-only SSH BatchMode metadata check failed due authentication;
- no live change.

## 10. Whether Any Safe Live Hardening Is Justified Now

No live hardening should be applied yet.

The likely first safe hardening target is:

- `/opt/v7/egress/state/profile-delivery-tokens.json`

But only after:

1. live service-user/drop-in verification;
2. metadata backup;
3. explicit rollback command;
4. profile delivery create/download/revoke verification plan;
5. explicit approval for the chmod.

Current recommended action:

- run `tools/v7-sensitive-state-check --pretty` on the VPS;
- confirm admin API/profile delivery process ownership;
- then decide whether a single-file `0600` rollout is safe.
