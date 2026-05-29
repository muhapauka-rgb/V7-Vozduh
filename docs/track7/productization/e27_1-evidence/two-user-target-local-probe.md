# E27.1 Target-Local Two-Probe Validation

date_utc=2026-05-28T21:37:19Z
interface=v7execwg0
url=https://speed.cloudflare.com/__down?bytes=1048576

## Pre Side Effect State
default via 195.2.79.1 dev ens3 proto static onlink 
default dev v7e356a192b79 scope link 
default dev v7e356a192b79 scope link 
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry

## Probes
round=1 ts=2026-05-28T21:37:19Z rc1=0 http=200 speed_bps=2904232 time_total=0.361051 rc2=0 http=200 speed_bps=3178504 time_total=0.329896
round=2 ts=2026-05-28T21:37:24Z rc1=0 http=200 speed_bps=3689583 time_total=0.284199 rc2=0 http=200 speed_bps=3504634 time_total=0.299197
round=3 ts=2026-05-28T21:37:30Z rc1=0 http=200 speed_bps=1253403 time_total=0.836583 rc2=0 http=200 speed_bps=1230532 time_total=0.852132
round=4 ts=2026-05-28T21:37:35Z rc1=0 http=200 speed_bps=3820853 time_total=0.274435 rc2=0 http=200 speed_bps=3546908 time_total=0.295631
round=5 ts=2026-05-28T21:37:41Z rc1=0 http=200 speed_bps=3075237 time_total=0.340974 rc2=0 http=200 speed_bps=3487882 time_total=0.300634

## Post Side Effect State
default via 195.2.79.1 dev ens3 proto static onlink 
default dev v7e356a192b79 scope link 
default dev v7e356a192b79 scope link 
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry

## Runtime Checkers
### v7-reconcile-check
OK
### v7-user-route-check
OK
### v7-killswitch-check
OK
### v7-provisioning-reconcile-check
OK

## Parsed Summary
probe_count 10
avg_mbps 23.753
min_mbps 9.844
max_mbps 30.567
all_samples_above_10 False
