# E8.6 Reconcile Expected vs Actual Matrix

Mode: read-only.

Fresh runtime sample: 2026-05-25T13:36:36Z.

Important context: this fresh E8.6 sample was captured after E8.5 restore, with
autoswitch authority active again. The quiet-window classification relies on
E8.5 samples. The fresh sample is used to confirm source semantics and live
expected/actual behavior.

## User Matrix

| User IP | Enabled | Assigned egress | Expected table | ip rule exists | route table default exists | user-route-check | reconcile complaint | Classification candidate |
|---|---:|---|---:|---|---|---|---|---|
| 10.0.0.2 | 1 | awg0 | 100 | yes | yes, `dev awg0` | OK | intermittent/no in primary | semantic false-positive candidate |
| 10.0.0.3 | 1 | awg0 | 101 | yes | yes, `dev awg0` | OK | yes | semantic false-positive |
| 10.0.0.6 | 1 | awg0 | 104 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.3 | 1 | awg0 | 1001 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.2 | 1 | awg0 | 1000 | yes | yes, `dev awg0` | OK | intermittent/no in primary | semantic false-positive candidate |
| 10.7.0.4 | 1 | awg0 | 1002 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.5 | 1 | vless | 1003 | yes | yes, `dev tun0` | OK | intermittent/no in primary | semantic false-positive candidate |
| 10.7.0.6 | 1 | awg0 | 1004 | yes | yes, `dev awg0` | OK | yes | semantic false-positive |
| 10.7.0.7 | 0 | vless | 1005 | not expected | not required | skipped | no | disabled-user exception |
| 10.7.0.8 | 1 | awg0 | 1006 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.9 | 1 | awg0 | 1007 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.10 | 1 | awg0 | 1008 | yes | yes, `dev awg0` | OK | intermittent | semantic false-positive |
| 10.7.0.11 | 1 | awg0 | 1009 | yes | yes, `dev awg0` | OK | yes | semantic false-positive |
| 10.7.0.12 | 1 | awg0 | 1010 | yes | yes, `dev awg0` | OK | yes | semantic false-positive |
| 10.7.0.13 | 1 | vless | 1011 | yes | yes, `dev tun0` | OK | yes | semantic false-positive |
| 10.7.0.14 | 1 | vless | 1012 | yes | yes, `dev tun0` | OK | yes | semantic false-positive |
| 10.7.0.15 | 1 | vless | 1013 | yes | yes, `dev tun0` | OK | intermittent | semantic false-positive |

## Egress Matrix

| Egress id | Interface | Enabled | NAT present | Route table references in fresh sample | Reconcile complaint |
|---|---|---:|---|---|---|
| awg0 | awg0 | 1 | yes | 100, 101, 104, 1000, 1001, 1002, 1004, 1006, 1007, 1008, 1009, 1010 | no egress complaint |
| awg3 | awg3 | 1 | yes | none in fresh users.registry | no egress complaint |
| vless | tun0 | 1 | yes | 1003, 1011, 1012, 1013 | no egress complaint |
| 1 | v7e356a192b79 | 1 | yes | none in fresh users.registry | no egress complaint |
| openvpn-1779388847-d2ad7c | v7edb0c189291 | 1 | yes | none in fresh users.registry | no egress complaint |
| wireguard-1779454504-c43409 | v7e06a394c478 | 1 | yes | none in fresh users.registry | no egress complaint |

## Aggregate Verdict

```text
all enabled users have ip rule=true
all enabled users have route table default=true
all enabled users pass route reality=true
all enabled users pass provisioning route/table checks=true
reconcile missing-rule complaints=false-positive
real stable runtime mismatch candidates=none for current reconcile failure class
```
