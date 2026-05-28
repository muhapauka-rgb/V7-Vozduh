# E25.7 rollback/removal execution raw
generated_utc=2026-05-28T12:13:50Z

## before removal
v7execwg0        UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
config_exists_before=true
default_route_before=default via 195.2.79.1 dev ens3 proto static onlink ;
resolv_hash_before=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
users_hash_before=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_before=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
wg_quick_down_exit=0
[#] ip link delete dev v7execwg0
config_archived_to=/root/e25_7_v7execwg0.conf.removed.20260528T121350Z

## after removal
config_exists_after=false
default_route_after=default via 195.2.79.1 dev ens3 proto static onlink ;
resolv_hash_after=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
users_hash_after=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_after=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
candidate_table_after=default dev v7e356a192b79 scope link ;
candidate_route_after=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif wg0 ;

## hidden movers after
