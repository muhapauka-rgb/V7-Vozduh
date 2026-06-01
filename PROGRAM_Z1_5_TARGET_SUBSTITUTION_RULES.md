# Program Z1.5 Target Substitution Rules

Date: 2026-06-01

## Can `awg3` Become `awg0` Automatically?

Yes, but only under a policy approval model and only when all substitution gates pass.

## Required Gates

Target substitution may pass only if:

- same route class
- same trust class
- same policy class
- same service scope
- same organization/group eligibility
- both targets are enabled
- both targets have interfaces present
- new target is eligible in fresh planner output
- new target health is above floor
- new target capacity is within approved capacity band
- rollback target remains unchanged
- budget remains `1`
- no safety critical status
- no quarantine/block/freeze applies

## Must Deny

Substitution must be denied if:

- target class changes from `GLOBAL_STABLE` to another route class
- target becomes execution-only/reserve-only/manual-only unless explicitly approved
- trust/direct routing class changes
- target health drops below floor
- target capacity is full or unknown
- policy hash changed
- approved user changed under user-specific approval

## Program Evidence

F2 `awg3 -> awg0` could have been eligible under policy approval when both targets were eligible.

Z1 `awg0 -> awg3` should deny the stale `awg0` target because `awg0` became ineligible due `stability_below_floor`.

## Verdict

target_substitution_defined=true

