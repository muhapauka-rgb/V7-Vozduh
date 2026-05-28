# E9.2.1 Target 1 Counting Matrix

Mode: read-only diagnostic only.

## User Matrix

| User IP | Enabled | Registry Current | Table | Table Default | Route-Get Dev | Counted By Target 1 Load | Classification |
|---|---:|---|---:|---|---|---|---|
| `10.0.0.2` | 1 | `vless` | 100 | `tun0` | `tun0` | no | baseline vless |
| `10.0.0.3` | 1 | `vless` | 101 | `tun0` | `tun0` | no | baseline vless |
| `10.0.0.6` | 1 | `vless` | 104 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.2` | 1 | `vless` | 1000 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.3` | 1 | `vless` | 1001 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.4` | 1 | `vless` | 1002 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.5` | 1 | `1` | 1003 | `v7e356a192b79` | `v7e356a192b79` | yes | real target-1 assignment |
| `10.7.0.6` | 1 | `vless` | 1004 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.8` | 1 | `vless` | 1006 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.9` | 1 | `vless` | 1007 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.10` | 1 | `vless` | 1008 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.11` | 1 | `vless` | 1009 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.12` | 1 | `vless` | 1010 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.13` | 1 | `vless` | 1011 | `tun0` | `tun0` | no | baseline vless |
| `10.7.0.14` | 1 | `vless` | 1012 | `tun0` | `tun0` | no | proposed second candidate remains baseline vless |
| `10.7.0.15` | 1 | `vless` | 1013 | `tun0` | `tun0` | no | first canary user remains rolled back |

Disabled user `10.7.0.7` is excluded from load/canary consideration.

## Assignment And Desired-State Evidence

```text
user-10.7.0.5.assign:
egress=1
last_switch=1779721663
fail_count=0

user-10.7.0.14.assign:
egress=vless
last_switch=1779695678
fail_count=0

user-desired-state:
10.7.0.5 current=1 expected_dev=v7e356a192b79 assign=1 table_dev=v7e356a192b79 route_get_dev=v7e356a192b79 status=OK
10.7.0.14 current=vless expected_dev=tun0 assign=vless table_dev=tun0 route_get_dev=tun0 status=OK
```

## Count Source Verdict

`1_users=1` is explained by a real enabled registry assignment and matching route table:

```text
10.7.0.5 current=1 table=1003
table 1003 default dev v7e356a192b79
route_get from 10.7.0.5 dev v7e356a192b79 table 1003
```

No hidden/non-registry load source is required to explain the count.
