# V7 Phase90 Installer Preflight Report

Date: 2026-05-08

## Goal

Start the installer wizard safely with read-only server diagnostics.

The installer section must not install packages, change firewall rules, or rewrite configs yet.

## Changes

- Added `/usr/local/bin/v7-installer-check`.
- Added `v7-installer-check` to `v7-safe-run` read-only whitelist.
- Added Admin endpoint:
  - `GET /api/installer`
- Added Installer card in Admin with `Run Preflight`.

## Preflight Checks

The check reports:

- OS and architecture
- kernel and hostname
- root access
- disk and memory
- default route and interface
- public IP
- IPv4 forwarding
- `/dev/net/tun`
- required commands
- key V7/system services
- listening ports

## Live VPS Validation

```text
os_id=ubuntu
os_version=26.04
arch=x86_64
default_if=ens3
public_ip=195.2.79.116
tun_device=present
V7_INSTALLER_PREFLIGHT=WARN
```

Current warning:

```text
amneziawg-go missing
```

This is informational for the future installer. No package installation was attempted.

## Safety Notes

- No packages were installed.
- No services were restarted except `v7-admin-api` for deployment.
- No firewall/routing rules were changed.
- No configs were rewritten by the installer check.

