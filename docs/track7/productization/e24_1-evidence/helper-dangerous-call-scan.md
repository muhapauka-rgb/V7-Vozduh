# E24.1 Helper Dangerous Call Scan

Scanned:

- `tools/v7-second-canary-target-readiness`
- `tools/v7-restore-settle-gate`

Pattern classes:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`
- `systemctl start|stop|restart|enable|disable`
- `ip route/rule add|del|delete|replace`
- `nft add|delete|flush|insert`
- `iptables` / `ip6tables`
- file write APIs:
  - `write_text`
  - `write_bytes`
  - `open(..., "w")`
  - `os.open`
  - `unlink`
  - `rename`
  - `replace`
  - `shutil`
- unsafe file mode/owner mutation:
  - `chmod`
  - `chown`
  - `rm -`

## Findings

Matches:

- `tools/v7-restore-settle-gate:5`
  - docstring only: states it does not call forbidden runtime commands.
- `tools/v7-second-canary-target-readiness:5`
  - docstring only: states it never calls forbidden runtime commands.
- `.replace(...)` string methods in both files.

No executable dangerous calls found.

## Verdict

- Helper mutation risk: NOT OBSERVED.
- Runtime command execution risk: NOT OBSERVED.
- Registry write risk: NOT OBSERVED.
- Routing mutation risk: NOT OBSERVED.
- Safe for bounded helper deployment: YES.
