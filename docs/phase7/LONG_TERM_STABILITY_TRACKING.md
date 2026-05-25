# V7 Phase 7 Long-Term Stability Tracking

## Purpose

Long-term operation needs compact history, not infinite telemetry.

## Track

- unstable channels;
- degradation frequency;
- restart frequency;
- maintenance history;
- quarantine history;
- autoswitch freeze history;
- chronic service instability;
- resource pressure episodes.

## Summary Windows

Use bounded summaries:

- last hour;
- last day;
- last week;
- last month.

## Operator Output

Examples:

- `awg2 unstable 4 times this week`;
- `Telegram degradation repeated on two egress`;
- `maintenance recurring on OpenVPN pool`;
- `resource pressure increasing during service matrix refresh`.

## Rule

History should help decide maintenance, quarantine, capacity, and upgrade timing. It should not become a telemetry dump.

