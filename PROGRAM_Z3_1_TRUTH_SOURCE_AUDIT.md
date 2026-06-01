# Program Z3.1 Truth Source Audit

Date: 2026-06-01

## Verdict

truth_source_audit_complete=true
live_truth_used=true

## Truth Sources

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Barrier | live `/opt/v7/egress/state/autoswitch-restore-barrier.json` | barrier status in planner output | Z3.1 reports |
| Clearance | live barrier clearance fields | generation match and selected hash match | clearance retest |
| Proposal | live `v7-users-autoswitch` dry-run | candidate/selected move summary | proposal sections |
| Approval | Z3.1 governance clearance in barrier | allowed user/target/budget fields | final report |
| Selected moves | live planner before and after guard | selected move hash | runtime audit |

## Rule

Live planner output is authoritative. Historical reports, fixtures, and repository snapshots were not substituted for live runtime truth.

## Safety

- fixture_used_as_runtime_truth=false
- historical_report_used_as_runtime_truth=false
- bypassed_live_planner=false

