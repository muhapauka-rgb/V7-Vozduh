# Program Z1.5 Decision Tree

Date: 2026-06-01

## If Target Approval Retained

1. Generate exact target proposal.
2. Operator approves exact user and target.
3. Fresh recheck must match exact target.
4. If target changed, deny and request new approval.

Result:

- safest
- high stale-denial rate

## If Policy Approval Adopted

1. Generate target class proposal.
2. Operator approves user, budget, route class, and target class.
3. Fresh recheck can substitute target only within strict class gates.
4. If candidate/budget/route/trust/rollback changes, deny.

Result:

- practical
- needs strong fingerprints and UI explanation

## If Hybrid Model Preferred

1. Default to target approval for manual or high-risk actions.
2. Allow policy approval only for bounded autonomy:
   - budget `1`
   - one user
   - fixed route class
   - fixed rollback
   - allowed target class
   - short TTL
3. Deny all drift outside the approved class.

Result:

- recommended

