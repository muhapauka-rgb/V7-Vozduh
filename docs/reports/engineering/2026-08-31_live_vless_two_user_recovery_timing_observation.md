# Live VLESS recovery timing observation

Date: 2026-08-31
Scope: read-only observation of the operator-initiated VLESS failure case.

## What V7 observed

- At `20:33:54.942 MSK`, the Matrix confirmed a VLESS failure affecting
  **13 services**.  This was a direct confirmed failure (`MODE_A_CONFIRMED`).
- The Matrix-derived ordinary production scope contained **2 active users**.
- The existing Planner selected `awg0`; no target was chosen or injected by
  Codex.

## Result

| Measure | Result |
| --- | --- |
| Confirmed failure -> execution lease | 14.205 s |
| Confirmed failure -> first route moved | 17.842 s |
| Confirmed failure -> all 2 routes moved | **18.457 s** |
| Target | `awg0` |
| Current enabled users on VLESS after recovery | **0** |

The two users were moved by the Runtime health actor, not by Codex:

- `10.7.0.127`: VLESS -> `awg0` at `20:34:12.784 MSK`.
- `10.7.0.125`: VLESS -> `awg0` at `20:34:13.399 MSK`.

The only remaining VLESS registry row is disabled (`10.7.0.7`), so it is not
an active customer placement.

## SLO verdict

The current production path **does not meet** the mandatory seven-second
limit.  It is not a case of no recovery: V7 selected and applied recovery for
both affected users, but it was too slow by 11.457 seconds.

## Measured dominant delay

The failure event was confirmed at `20:33:54.942`, while the obligation was
only made ready for its existing OMP consumer at `20:34:04.590` (9.648 s),
and the execution lease was created at `20:34:09.147` (14.205 s total).
During the same window the health loop had an `other_required` check running
for 9.608 s before it was pre-empted.  The immediate next repair frontier is
therefore the owner-backed handoff from confirmed Matrix failure to the
already-prepared execution transaction; route application itself accounts for
roughly the final four seconds.

No routing, Authority, Matrix, Planner, client, or policy state was changed
during this observation.
