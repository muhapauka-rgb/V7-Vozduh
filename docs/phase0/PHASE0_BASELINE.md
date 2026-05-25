# V7 Phase 0 Baseline

Purpose: freeze the current repository understanding without changing runtime behavior.

Phase 0 is documentation, inventory, boundaries, and cleanup planning only. It must not change routing logic, nftables behavior, provisioning behavior, autoswitch behavior, or production contracts.

## Current Repository Shape

```text
.
├── admin/
│   └── v7-admin-api
├── tools/
├── hardening/
├── systemd/
├── design/
├── artifacts/
├── test-results/
├── docs/phase0/
└── V7_*.md
```

## Current Operational Center

The operational center is still the existing shell/Python runtime:

- `admin/v7-admin-api` is the admin/control-plane monolith.
- `tools/` contains measurement, autoswitch, public gateway, client speed, lifecycle, and install helpers.
- `hardening/` contains kill switch, direct/RU, MTU, path guard, and reconciliation checks.
- `systemd/` contains timers and units for production scheduling.

## Current Baseline Counts

- `admin/v7-admin-api`: about 30067 lines.
- `tools/`: 13 executable scripts.
- `hardening/`: 8 executable scripts.
- `systemd/`: 9 unit/timer files.
- `design/`: 10 HTML snapshots/prototypes.
- `artifacts/`: test WireGuard/AmneziaWG configs and QR images.

## Dirty Worktree Baseline

Pre-existing modified runtime files were present before Phase 0 documentation work:

- `admin/v7-admin-api`
- `hardening/v7-killswitch-check`
- `hardening/v7-provisioning-reconcile-check`
- `systemd/v7-users-autoswitch.timer`
- `tools/v7-egress-import-regression`
- `tools/v7-egress-set-state`
- `tools/v7-service-matrix-test`
- `tools/v7-telegram-sentinel`
- `tools/v7-users-autoswitch`

Phase 0 must not revert or rewrite those changes. They are treated as the current working baseline.

## Proposed Future Repository Structure

This is a proposal only. No runtime-critical file should be moved until compatibility wrappers and deployment paths are designed.

```text
v7/
  admin_api/
    auth/
    state/
    identity/
    egress/
    policy/
    diagnostics/
    audit/
    routing/
    ui_legacy/
  web/
    operator_ui/
    public_connect/
  tools/
    measurement/
    autoswitch/
    lifecycle/
    public/
  hardening/
    killswitch/
    direct_routing/
    reconciliation/
  systemd/
  scripts/
    install/
    deploy/
    smoke/
  tests/
    regression/
    contract/
    safety/
  contracts/
  inventory/
  docs/
  legacy/
    design_snapshots/
    phase_reports/
    test_artifacts/
```

## Phase 0 Rule

The repository may gain documentation and non-invasive helper files. It must not gain hidden behavior changes.

