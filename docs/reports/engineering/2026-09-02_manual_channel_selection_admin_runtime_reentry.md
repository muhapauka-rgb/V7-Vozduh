# Manual channel selection — admin Runtime re-entry — 2026-09-02

## User-visible symptom

The operator could not reliably choose a channel in the administration UI.  A
previous UI response had reported Safe Mode, although the current canonical
execution-control state was already `CLOSED` with `enabled=false`.

## Exact cause

The deployed file `/usr/local/bin/v7-admin-api` matched the current approved
source, but its actual systemd process had been running since 2026-09-01.  A
Python service keeps the imported endpoint and UI code in memory, so copying a
new file alone does not update a running admin process.

`v7-api.service` is a separate, minimal local state wrapper on port 7077.  It
does not serve the operator UI.  The real UI process is
`v7-admin-api.service` on port 7080.  Restarting only the wrapper cannot make
manual channel selection use new code.

The audit also proves that the existing governed manual-rebind endpoint itself
was live: three operator selections completed successfully at 12:21–12:22
MSK.  Older failed attempts were bounded route-writer timeouts and remain
visible as failures; none were silently treated as a completed route change.

## Repair and verification

1. Read the canonical execution-control file.  It was valid and closed, with
   no active operation, so Safe Mode was not a current blocker.
2. Restarted only `v7-admin-api.service`; no user, route, Candidate, Packet,
   Lease, Barrier or automatic recovery state was changed.
3. Verified the replacement process started at `2026-09-02 13:05:15 MSK`, is
   active, and serves the operator endpoint on `127.0.0.1:7080`.

## Preventive rule

When an approved deploy changes `admin/v7-admin-api`, deploy through
`tools/v7-safe-deploy --restart-admin-if-changed` in addition to any required
health-loop restart.  The safe-deploy owner already enforces that explicit
restart flag for a changed admin binary.  The execution remains controlled:
only the admin process is restarted, and route ownership stays with
`v7-user-switch`.

## Next step

Refresh the open administration page once.  The next manual channel selection
will use the current endpoint.  If it fails, its returned error and audit row
will distinguish an active route-writer window from a true route verification
failure; neither condition will be misreported as a successful move.
