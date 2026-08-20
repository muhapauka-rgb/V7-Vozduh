# V5.3 Matrix comparison — publication and Runtime verification

Date: 2026-08-20  
Scope: publication and safe deployment of the existing Planner-to-Matrix
short/full comparison; no route or client action.

## Outcome

The bounded comparison implementation was published and safely deployed.
GitHub, local branch and installed Runtime are aligned at
`0d8729a109dcc5b9a9a6bea689ec053311c01869` on `Updatesystem`.

Installed changed Runtime artifacts:

- `/usr/local/bin/v7-users-autoswitch`;
- `/usr/local/bin/v7-service-matrix-refresh-all`;
- `/etc/systemd/system/v7-service-matrix-refresh.service`.

`v7-safe-deploy` reports no remaining Runtime delta. `v7-truth-check --all`
reports `PASS`, matching authoritative binary hashes and
`RUNTIME_ALIGNED`. The existing Matrix timer is active and its live status is
known. No new timer, owner, queue, registry or state store was created.

## GitHub access correction

The earlier `GitHub unavailable` diagnosis was wrong for the repository. The
ordinary Codex sandbox could not resolve `github.com`, and its `gh` token was
invalid. A read outside that sandbox reached GitHub successfully and showed
the real initial condition: local commits were ahead of `Updatesystem`.

The two already reviewed commits were published:

- `8859041e v7: add planner matrix comparison shadow`;
- `0d8729a1 v7: record matrix comparison deploy boundary`.

After publication, independent branch verification passed and the safe deploy
guard allowed the installation. The separate local `gh` token remains stale,
but it is not required by the deployed system or by Git-based publication.

## Safety and evidence

The deployed comparison remains shadow-only:

- Planner supplies only its own exact source, eligible targets and required
  services;
- stale, missing, conflicting or multi-source input stops safely;
- the short Matrix observation is followed by the complete service catalogue
  for the same selected channels;
- the full result remains final canonical Matrix evidence;
- no comparison result creates a Candidate, Packet, lease, route change or
  client move.

Before deployment, focused wiring tests passed (4/4) and controlled Polygon
Matrix cases passed (3/3): healthy path, required-service failure and
methodology-limited HTTP response agreed between the exact and full checks.
The controlled probe measurement remains 3 instead of 14 selected services
(78.6% fewer) and 9.793 ms instead of 41.284 ms (76.3% shorter). These are
Polygon measurements, not a claim about production latency.

## Plan position and next action

Position: **step 5 of 6 is complete** — implementation, publication,
deployment and Runtime identity verification are complete.

Next action: run the existing controlled Polygon caller end-to-end through the
deployed short/full comparison receipt, then record its timing, check-count,
agreement and fallback fields. This does not wait for a natural incident and
does not change a route or client. Only after that evidence may Phase E update
the B/C architecture decision; the full Matrix remains the live fallback.
