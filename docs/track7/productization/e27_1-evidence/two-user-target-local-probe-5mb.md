# E27.1 Target-Local Two-Probe Validation 5MB

date_utc=2026-05-28T21:38:24Z
interface=v7execwg0
url=https://speed.cloudflare.com/__down?bytes=5242880

## Pre Side Effect State
default via 195.2.79.1 dev ens3 proto static onlink 
default dev v7e356a192b79 scope link 
default dev v7e356a192b79 scope link 
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry

## Probes
round=1 ts=2026-05-28T21:38:25Z rc1=0 http=200 speed_bps=7924259 time_total=0.661624 rc2=0 http=200 speed_bps=7226524 time_total=0.725505
round=2 ts=2026-05-28T21:38:30Z rc1=0 http=200 speed_bps=2109150 time_total=2.485778 rc2=0 http=200 speed_bps=1627504 time_total=3.221422
round=3 ts=2026-05-28T21:38:39Z rc1=0 http=200 speed_bps=7048985 time_total=0.743778 rc2=0 http=200 speed_bps=8058121 time_total=0.650633
round=4 ts=2026-05-28T21:38:44Z rc1=0 http=200 speed_bps=2175728 time_total=2.409712 rc2=0 http=200 speed_bps=3156207 time_total=1.661133
round=5 ts=2026-05-28T21:38:52Z rc1=0 http=200 speed_bps=4590219 time_total=1.142185 rc2=0 http=200 speed_bps=3823146 time_total=1.371352

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
avg_mbps 38.192
min_mbps 13.02
max_mbps 64.465
all_samples_above_10 True
