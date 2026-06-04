# Runtime Nervous System Evidence 01 - Production Runtime Truth

Latest known production truth from read-only convergence and SSH inspection:

```text
local_commit=4905000186f74763e5f91c63ae44be2e3330816d
github_commit=4905000186f74763e5f91c63ae44be2e3330816d
production_commit=4905000186f74763e5f91c63ae44be2e3330816d
convergence_status=PASS
alignment=ALIGNED
truth=FULLY_ALIGNED
runtime_access=READY
runtime_truth=KNOWN
```

Host/time sample:

```text
host=v3119922.hosted-by-vdsina.ru
time=2026-06-04T16:46:51+03:00
```

## Systemd Reality

| Unit | Latest observed state | Operating implication |
| --- | --- | --- |
| `v7-autoswitch-planner.timer` | active/enabled, fires about every 30 seconds | Owns recurring non-apply planner cycle in current production reality. |
| `v7-autoswitch-planner.service` | static/inactive between runs | Executes `/usr/local/bin/v7-users-autoswitch` without `--apply`, with `V7_ACTOR=autoswitch-planner`. |
| `v7-users-autoswitch.timer` | loaded/enabled but inactive/dead in latest sample | Movement-capable apply timer is held, not current active cycle owner. |
| `v7-users-autoswitch.service` | loaded/static but inactive/dead in latest sample | Apply authority is not continuously active. |
| `v7-intelligence-snapshot-refresh.service` | not found | No sustained production snapshot refresh service. |
| `v7-intelligence-snapshot-refresh.timer` | not found | No sustained production snapshot refresh timer. |
| `v7-service-matrix-refresh.timer` | active | Existing signal refresh contributor. |
| `v7-egress-quality-compact.timer` | active | Existing quality signal contributor. |
| `v7-telegram-sentinel.timer` | active | Existing channel/service signal contributor. |
| `v7-traffic-collector.timer` | active | Existing runtime signal contributor. |

## Critical Reality Delta

Older Z6 reports treated the draft planner timer as dormant or "do not touch". Later E8/E9 production reports and the latest production inspection show a different reality:

```text
v7-autoswitch-planner.timer/service owns non-apply planner authority.
v7-users-autoswitch.timer/service owns apply authority when restored.
```

The active planner service reuses the canonical autoswitch tool, so this is not a new planner implementation. It is still an ownership and policy gap because runtime trigger policy must explicitly name this timer as the recurring planner trigger.

## Production Tool Surface

`v7-runtime-tool-enumerate --pretty` on production reported:

```text
total_v7_tools=166
production_only=166
repo_present=0
must_be_release_owned=93
operator_only_optional=20
safe_archive_candidate_future=52
```

This does not by itself prove unsafe behavior, but it keeps production tool ownership as an operating policy concern. Tools must be classified by release ownership before any authority promotion.

