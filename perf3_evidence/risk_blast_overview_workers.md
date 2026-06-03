# PERF.3 Risk, Blast Radius, and Overview Workers

## Risk Worker

Inputs:

- `service-scores` snapshot
- `channel-service-scores` snapshot
- quality summary

Output:

- `risk-summaries.json`

The producer is advisory-only and has no runtime authority. It computes:

- service_risk
- platform_health
- average_channel_score
- average_service_score
- high_risk_channels

## Blast Radius Worker

Inputs:

- `trust-summaries` snapshot
- `risk-summaries` snapshot
- total users
- affected candidates

Output:

- `blast-radius-summaries.json`

Reused logic:

- `DynamicBlastRadiusModel.recommend`

The output is a recommendation only and preserves:

- runtime_decision_authority=`none_snapshot_only`

## Overview Worker

Inputs:

- runtime state
- users registry
- egress registry
- snapshot statuses

Output:

- `overview-summary.json`

Purpose:

- future fast admin overview
- no current admin API integration

Failure behavior:

- missing runtime state yields warning `runtime_state_missing`
