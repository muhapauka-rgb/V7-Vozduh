# P5.1 Certification

## Certification State

`NOT_READY`

## Reason

The repository clearly identifies the canonical runtime truth model, but fresh live runtime truth was not accessible and could not be certified.

## Certified

- expected source model: `/opt/v7/egress/state`
- required files and domains
- hash algorithms
- freshness model
- fail-closed behavior
- implementation reuse path

## Not Certified

- live users registry hash
- live egress registry hash
- live selected moves hash
- live runtime snapshot hash
- live runtime freshness
- safe P5 retry

## Recommendation

Before retrying P5, provide a read-only, side-effect-conscious way to collect the live runtime state from the production runtime host.

Acceptable options:

- direct read-only shell access to `/opt/v7/egress/state`
- an authenticated read-only API session where login/audit side effects are explicitly approved for discovery
- a signed, freshly generated runtime truth bundle produced on the runtime host

## Verdicts

- runtime_truth_source_certified=false
- safe_to_rerun_p5=false
- certification=NOT_READY
