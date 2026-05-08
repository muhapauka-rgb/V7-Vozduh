# V7 Phase87 Kill Switch Read-only Admin Report

Date: 2026-05-08

## Goal

Expose kill switch state in Admin without changing firewall rules or risking SSH lockout.

## Changes

- Added read-only `/api/killswitch`.
- Added `Kill Switch Details` button in Route Reality.
- Admin modal now shows:
  - check result
  - VPN subnet
  - public interface
  - nft table presence
  - direct leak drop rule
  - direct whitelist rule
  - fwmark routing rule
  - direct route table
  - DNS capture rules
  - warning count
  - SSH lockout guard explanation

## Live VPS Validation

Authenticated Admin API response:

```text
result=OK
vpn_subnet=10.0.0.0/24
public_if=ens3
table=present
direct_leak_drop_rule=present
direct_whitelist_rule=present
direct_fwmark_rule=present
direct_fwmark_precedes_user_rules=OK
direct_route_table=present
direct_mark_rule=present
dns_capture_udp=present
dns_capture_tcp=present
warnings=0
check_rc=0
status_rc=0
```

User route check confirmed current users route through `awg2` or `tun0`, not directly through `ens3`.

## Safety Notes

- This phase did not run `v7-killswitch-enable`.
- This phase did not change nftables or routing.
- Admin SSH is not managed by the V7 forward-chain leak guard; the UI explicitly states this.

