# CT-M0F: correlated recovery and binding fail-closed repair

## Root cause

The post-deploy CT-M0F Packet-forwarding repair was installed correctly, but
the next ordinary Matrix cycle still produced an unbound outcome. Read-only
selection proved why: the L3 state owner exposed no active VLESS binding.

The existing Matrix producer emitted `SERVICE_RECOVERY_OBSERVED` when one
component service recovered, even while another service on the same channel
remained persistently failed. The passive owner consequently closed the
source incident. The CT-M0F selector still saw degraded Matrix truth and
attempted a controlled cutover with no incident lineage. The CT-M0F evidence
gate rejected that outcome, correctly, as `incident_id_missing`.

## Repair

- The existing Matrix event owner now defers source-level recovery events
  until the correlated source has no persistent failed components.
- When the existing L3 state file is present, absence or ambiguity of the
  active binding is now an explicit required binding. A real-source CT-M0F
  selection therefore reaches `STOP_SAFE` instead of creating an unbound
  Packet/outcome.
- Existing isolated controlled-condition lineage remains unchanged.

## Verification and successor

Focused tests: `183 PASS` (`test_service_failure_episode` and
`test_governed_canary_cli`), including a partial-component-recovery regression
and a missing-L3-binding fail-closed regression.

The next production verification must be one ordinary Matrix timer generation
after safe deployment. It must either retain/recreate the current active
incident binding from continuing correlated failure and create a fresh bound
CT-M0F sample, or return the exact safe live terminal. No historical Packet,
event or timing sample is reused. No Authority, Production Maturity or user
scope is expanded by this repair.
