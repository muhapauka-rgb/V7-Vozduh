# E25.8 replacement profile source search raw evidence
timestamp_utc=2026-05-28T12:40:49Z
hostname=v3119922.hosted-by-vdsina.ru


## runtime_baseline
$ pwd
/root
$ ip -4 addr show scope global
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    altname enp0s3
    altname enx5254002f9b32
    inet 195.2.79.116/24 brd 195.2.79.255 scope global ens3
       valid_lft forever preferred_lft forever
3: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.0.0.1/24 scope global wg0
       valid_lft forever preferred_lft forever
13: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1400 qdisc fq state UNKNOWN group default qlen 500
    inet 172.19.0.1/30 brd 172.19.0.3 scope global tun0
       valid_lft forever preferred_lft forever
43: v7e356a192b79: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.10.120.8/32 scope global v7e356a192b79
       valid_lft forever preferred_lft forever
44: awg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.8.1.10/32 scope global awg0
       valid_lft forever preferred_lft forever
45: awg3: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.8.1.13/32 scope global awg3
       valid_lft forever preferred_lft forever
432: v7edb0c189291: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    inet 10.0.70.4/24 brd 10.0.70.255 scope global v7edb0c189291
       valid_lft forever preferred_lft forever
439: v7e06a394c478: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.8.0.17/24 scope global v7e06a394c478
       valid_lft forever preferred_lft forever
$ ip route show default
default via 195.2.79.1 dev ens3 proto static onlink 
$ ip rule show
0:	from all lookup local
50:	from all fwmark 0x77 lookup 70
55:	from 195.2.79.116 lookup main
60:	from all uidrange 995-995 lookup 100
100:	from 10.0.0.2 lookup 100
101:	from 10.0.0.3 lookup 101
104:	from 10.0.0.6 lookup 104
1000:	from 10.7.0.2 lookup 1000
1001:	from 10.7.0.3 lookup 1001
1002:	from 10.7.0.4 lookup 1002
1003:	from 10.7.0.5 lookup 1003
1004:	from 10.7.0.6 lookup 1004
1006:	from 10.7.0.8 lookup 1006
1007:	from 10.7.0.9 lookup 1007
1008:	from 10.7.0.10 lookup 1008
1009:	from 10.7.0.11 lookup 1009
1010:	from 10.7.0.12 lookup 1010
1011:	from 10.7.0.13 lookup 1011
1012:	from 10.7.0.14 lookup 1012
1013:	from 10.7.0.15 lookup 1013
32766:	from all lookup main
32767:	from all lookup default
$ test ! -e /etc/wireguard/v7execwg0.conf
$ ip link show v7execwg0
Device "v7execwg0" does not exist.
exit=1
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1

## candidate_paths
/etc/wireguard/v7e06a394c478.conf 315 bytes
/etc/wireguard/v7execwg0.conf.e25_7_before_keepalive 319 bytes
/etc/wireguard/v7execwg0.conf.e25_7_before_mtu1200 319 bytes
/etc/wireguard/vps.conf 238 bytes
/etc/wireguard/wg-client-test.conf 697 bytes
/etc/wireguard/wg0.conf 2963 bytes
/etc/wireguard/wg0.conf.backup.20260506-163303 416 bytes
/etc/wireguard/wg0.conf.backup.iphone.20260506-164945 412 bytes
/etc/wireguard/wg0.conf.backup.nat-egress.20260506-165513 523 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260506-171016 835 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260506-195020 835 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-161819 836 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-161923 959 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-162703 837 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260509-095148 960 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-223215 961 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-223355 1084 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-225923 1207 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-225941 1330 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-162145 1453 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-164331 1576 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-172826 1543 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-215434 1666 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-215821 1790 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-001900 1791 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-002854 1916 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-003507 1792 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-003834 1793 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004008 1794 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004618 1795 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004748 1796 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-212852 1797 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260515-073929 1920 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260515-074517 2043 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260517-174520 1085 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260517-174942 1207 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260518-143340 1329 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260520-231105 1762 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-133329 1885 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145816 2008 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145831 2132 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145841 2256 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-154617 2380 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-160728 2505 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-160743 2630 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-161435 2755 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-162731 2880 bytes
/etc/wireguard/wg0.conf.backup.v7-user-create.20260523-145551 2838 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260506-195117 955 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260508-162631 926 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260509-095150 1081 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260513-164950 1699 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260513-221130 1914 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003316 2041 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003317 1882 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003509 1915 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004007 1918 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004617 1917 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004619 1918 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004749 1919 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-122954 1797 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-123441 1797 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163115 2166 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163124 2166 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163131 2010 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163140 2010 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163203 1854 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163217 1765 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163221 1642 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163241 1552 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163247 1429 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163256 1306 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163259 1183 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260520-231014 1884 bytes
/etc/wireguard/wg0.conf.backup.v7-user-disable.20260523-145431 2996 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-1779291888-b0b382/result.json 1747 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-1779292334-17bc7f/result.json 1747 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291888-968d6d/result.json 2501 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291888-968d6d/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291889-8e4594/result.json 15004 bytes
/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291889-8e4594/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779212551-5f2af4-1779212567-d21edc/result.json 1725 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779212551-5f2af4-1779227526-6b3483/result.json 1725 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-1779227953-9968ee/result.json 1740 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779229741-d72ffe/result.json 2306 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779229741-d72ffe/sanitized-runtime.conf 318 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230366-3b4957/result.json 2495 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230366-3b4957/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230578-730443/result.json 14998 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230578-730443/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230717-01826d/result.json 14942 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230717-01826d/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230774-51cf55/result.json 14982 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230774-51cf55/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-1779303737-cf3f93/result.json 1740 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303737-dd22ec/result.json 2494 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303737-dd22ec/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303739-2a8b85/result.json 14970 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303739-2a8b85/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-1779305909-440a3b/result.json 1740 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305909-f16c54/result.json 2494 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305909-f16c54/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305911-2fff97/result.json 14953 bytes
/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305911-2fff97/sanitized-runtime.conf 587 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779352711-bc94ec-1779352720-8888d9/result.json 1437 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779352711-bc94ec-1779352724-980fad/result.json 1437 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779352726-16e1ec-1779352770-db864f/result.json 1437 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-1779387408-07b64d/result.json 1597 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-quarantine-1779387409-966d63/openvpn-runtime.ovpn 9777 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-quarantine-1779387409-966d63/result.json 15157 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-runtime-1779387408-adb23c/openvpn-runtime.ovpn 9777 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-runtime-1779387408-adb23c/result.json 5642 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-1779388847-4cb017/result.json 1597 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-quarantine-1779388848-158247/openvpn-runtime.ovpn 9777 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-quarantine-1779388848-158247/result.json 16639 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-runtime-1779388847-af3427/openvpn-runtime.ovpn 9777 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-runtime-1779388847-af3427/result.json 5642 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-1779453676-d82055/result.json 1597 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779453676-afdc62/openvpn-runtime.ovpn 9739 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779453676-afdc62/result.json 2259 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454017-3049b4/openvpn-runtime.ovpn 9739 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454017-3049b4/result.json 2259 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454375-4f05cc/openvpn-runtime.ovpn 9739 bytes
/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454375-4f05cc/result.json 4711 bytes
/opt/v7/admin/egress-draft-tests/subscription_url-1779462892-4d2cea-1779462892-48c0db/result.json 1010 bytes
/opt/v7/admin/egress-draft-tests/test1-1779352953-489ac4-1779352997-9f7005/result.json 1413 bytes
/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-1779455931-4d4466/result.json 1771 bytes
/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455931-abf4ef/result.json 2155 bytes
/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455931-abf4ef/sanitized-runtime.conf 315 bytes
/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455932-39b6db/result.json 14573 bytes
/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455932-39b6db/sanitized-runtime.conf 315 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-1779454504-488966/result.json 1711 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454504-db9ec5/result.json 2095 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454504-db9ec5/sanitized-runtime.conf 315 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454505-0be4c3/result.json 14518 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454505-0be4c3/sanitized-runtime.conf 315 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779455648-10ab7e/result.json 14521 bytes
/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779455648-10ab7e/sanitized-runtime.conf 315 bytes
/opt/v7/backups/final-state-split-ok-20260505-234252/v7-run-amneziawg 293 bytes
/opt/v7/backups/stable-core-20260505-230621/v7-run-amneziawg 293 bytes
/opt/v7/backups/stable-state-split-20260505-233947/v7-run-amneziawg 293 bytes
/opt/v7/egress/amneziawg/awg-test-194.124.210.244.conf 456 bytes
/opt/v7/egress/amneziawg/awg2-94.241.139.241.conf 587 bytes
/opt/v7/egress/state/autoswitch-restore-barrier.json 598 bytes
/opt/v7/egress/state/autoswitch-safety.json 34510 bytes
/opt/v7/egress/state/awg-test-194.124.210.244.conf.state 197 bytes
/opt/v7/egress/state/awg2-94.241.139.241.conf.state 218 bytes
/opt/v7/egress/state/client-agents.json 421 bytes
/opt/v7/egress/state/client-commands.json 4079 bytes
/opt/v7/egress/state/client-reconnect-state.json 4755 bytes
/opt/v7/egress/state/client-speed-links.json 68 bytes
/opt/v7/egress/state/client-speed.json 18770 bytes
/opt/v7/egress/state/egress-labels.json 191 bytes
/opt/v7/egress/state/egress-load-summary.json 2034 bytes
/opt/v7/egress/state/egress-quality-ring.json 687344 bytes
/opt/v7/egress/state/egress-quality-summary.json 10355 bytes
/opt/v7/egress/state/egress-speed.json 2153 bytes
/opt/v7/egress/state/egress.registry.backup.awg3-20260519-2155 568 bytes
/opt/v7/egress/state/path-benchmark.json 19399 bytes
/opt/v7/egress/state/path-optimizer-advice.json 1801 bytes
/opt/v7/egress/state/path-samples.json 2796 bytes
/opt/v7/egress/state/profile-delivery-tokens.json 34217 bytes
/opt/v7/egress/state/profile-delivery-tokens.json.backup.awg2-smux-20260519-165553 24261 bytes
/opt/v7/egress/state/service-matrix-refresh-summary.json 16110 bytes
/opt/v7/egress/state/service-matrix.json 101028 bytes
/opt/v7/egress/state/service-matrix.json.backup.clear-telegram-awg2-20260519-135350 52470 bytes
/opt/v7/egress/state/service-preferences.json 466 bytes
/opt/v7/egress/state/telegram-sentinel.json 10589 bytes
/opt/v7/egress/state/v7-state.json 10179 bytes
/opt/v7/egress/state/vless-activity.json 1353 bytes
/opt/v7/legacy/bin/v7-run-amneziawg 293 bytes
/opt/v7/ops/deploy-baseline/20260523T122251Z/contract-summary.json 9671 bytes
/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json 313943 bytes
/opt/v7/ops/deploy-baseline/20260523T122251Z/unit-summary.json 46686 bytes
/root/amnezia_for_awg_direct.conf 462 bytes
/root/e25_7_continuation_v7execwg0.conf.removed.20260528T123323Z 319 bytes
/root/e25_7_v7execwg0.conf.removed.20260528T121350Z 319 bytes
/root/runtime-enumeration.json 312223 bytes
/root/v7-admin-api-effective-egress-wg-option-backup-20260521-204544 1671968 bytes
/root/v7-admin-api-wg-label-backup-20260521-204901 1674233 bytes
/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.conf 430 bytes
/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.png 1523 bytes
/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.redacted.conf 322 bytes
/root/v7-awg2-smux-test.db 32768 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json 232501 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/skipped-files.json 3 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.backup.fix-vless-runtime-egress-20260519-185936 1460995 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.backup.karing-wg-endpoint-20260519-2120 1468276 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.bak.codex-20260519-vless-ops 1401784 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.bak.codex-20260519-vless-status 1398393 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.bak.codex-20260519-vless-status-2 1400968 bytes
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/v7-admin-api.bak.codex-20260519-vless-status-3 1401586 bytes
/root/v7-backups/usr-local-bin-archive/20260523T124646Z/archive-manifest.json 4724 bytes
/root/v7-clients/quick-040cad24-iphone/quick-040cad24-iphone.conf 250 bytes
/root/v7-clients/quick-154c65bb-iphone/quick-154c65bb-iphone.conf 250 bytes
/root/v7-clients/quick-19d80844-iphone/quick-19d80844-iphone.conf 250 bytes
/root/v7-clients/quick-3a12a3c5-iphone/quick-3a12a3c5-iphone.conf 250 bytes
/root/v7-clients/quick-5a74c0a3-iphone/quick-5a74c0a3-iphone.conf 250 bytes
/root/v7-clients/quick-65977141-iphone/quick-65977141-iphone.conf 250 bytes
/root/v7-clients/quick-7330cdec-iphone/quick-7330cdec-iphone.conf 250 bytes
/root/v7-clients/u000513-iphone-83aab2/u000513-iphone-83aab2.conf 250 bytes
/root/v7-clients/u001357-phone-2abf80/u001357-phone-2abf80.conf 251 bytes
/root/v7-clients/u001357-phone-7addd9/u001357-phone-7addd9.conf 250 bytes
/root/v7-clients/u001357-phone-9a5a0c/u001357-phone-9a5a0c.conf 251 bytes
/root/v7-clients/u001357-phone-bd0f69/u001357-phone-bd0f69.conf 250 bytes
/root/v7-clients/u001859-laptop-0ffdb7/u001859-laptop-0ffdb7.conf 251 bytes
/root/v7-clients/u002853-laptop-e5d569/u002853-laptop-e5d569.conf 251 bytes
/root/v7-clients/u003833-laptop-5d7eb2/u003833-laptop-5d7eb2.conf 251 bytes
/root/v7-clients/u234567-iphone-b8ebfc/u234567-iphone-b8ebfc.conf 250 bytes
/root/v7-clients/u234567-iphone-bbefcf/u234567-iphone-bbefcf.conf 250 bytes
/root/v7-clients/u234567-iphone-dabe50/u234567-iphone-dabe50.conf 250 bytes
/root/v7-clients/u497791-iphone-613cf0/u497791-iphone-613cf0.conf 251 bytes
/root/v7-clients/u497791-iphone-98f10b/u497791-iphone-98f10b.conf 251 bytes
/root/v7-clients/u497791-iphone-a12c00/u497791-iphone-a12c00.conf 250 bytes
/root/v7-clients/u497791-iphone-a9e43d/u497791-iphone-a9e43d.conf 250 bytes
/root/v7-clients/u497791-iphone-b0317e/u497791-iphone-b0317e.conf 251 bytes
/root/v7-clients/u497791-iphone-b2a87d/u497791-iphone-b2a87d.conf 250 bytes
/root/v7-clients/u497791-iphone-cf7147/u497791-iphone-cf7147.conf 251 bytes
/root/v7-clients/u497791-laptop-2e8c0c/u497791-laptop-2e8c0c.conf 250 bytes
/root/v7-clients/u497791-laptop-7ca2f7/u497791-laptop-7ca2f7.conf 250 bytes
/root/v7-clients/u500069-iphone-4e45ec/u500069-iphone-4e45ec.conf 250 bytes
/root/v7-clients/u597791-iphone-562fe0/u597791-iphone-562fe0.conf 250 bytes
/root/v7-clients/u597791-iphone-fa9458/u597791-iphone-fa9458.conf 250 bytes
/root/v7-clients/u614825-iphone-b1c407/u614825-iphone-b1c407.conf 251 bytes
/root/v7-clients/u721171-android-be4d23/u721171-android-be4d23.conf 250 bytes
/root/v7-clients/u721171-android-ca87f8/u721171-android-ca87f8.conf 250 bytes
/root/v7-clients/u721171-android-e4ad8e/u721171-android-e4ad8e.conf 250 bytes
/root/v7-clients/u741661-iphone-b000a5/u741661-iphone-b000a5.conf 250 bytes
/root/v7-clients/v7-iphone/v7-iphone.conf 250 bytes
/root/v7-clients/v7-lab-speed/v7-lab-speed.conf 251 bytes
/root/v7-clients/v7-subnet-test-1000/v7-subnet-test-1000.conf 250 bytes
/root/v7-deploy-backups/pasha-karing-wg-profile.20260518-221744.json 2066 bytes
/root/v7-deploy-backups/sing-box-happ-test-public.20260518-221632.json 1132 bytes
/root/v7-deploy-backups/v7-admin-api.20260519-003207.before-wg-restore 1396122 bytes
/root/v7-deploy-backups/v7-admin-api.20260519-010049.before-vless-awg2-bind 1396474 bytes
/root/v7-deploy-backups/wg0.conf.20260518-213646 1452 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/awg2-conf.txt 587 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/egress.registry.before-awg0 308 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/karing-wg-profile.txt 2066 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/pasha-vless-profile.txt 1915 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/runtime-vless.txt 1780 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/wg-dump.txt 1107 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/wg-show.txt 1467 bytes
/root/v7-diagnostics/2026-05-19-fix-all-routes/wg0-conf.txt 1884 bytes
/root/v7-diagnostics/2026-05-19-route-matrix/runtime-sing-box.json 1780 bytes
/root/v7-diagnostics/2026-05-19-route-matrix/service-preferences.before.json 267 bytes
/root/v7-diagnostics/2026-05-19-route-matrix/status-vless.service.txt 3039 bytes
/root/v7-diagnostics/2026-05-19-route-matrix/wg-show.txt 1477 bytes
/root/v7-dynamic-load-backup-20260518-150622/policy.json 504 bytes
/root/v7-e84-systemd-split-20260525T123450Z/backups/v7-health.service.d.before/10-routing-order.conf 67 bytes
/root/v7-e84-systemd-split-20260525T123450Z/v7-health.service.d/10-routing-order.conf 37 bytes
/root/v7-install-backups/proxy-identity-sync-happ-test-20260509-135604/bindings/user-10.0.0.2.json 778 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/bindings/user-10.0.0.2.json 704 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/metadata.json 647 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/sing-box.json 465 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.2.json 773 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.3.json 778 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.6.json 778 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/metadata.json 771 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/sing-box.json 463 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.2.json 848 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.3.json 852 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.6.json 852 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/metadata.json 771 bytes
/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/sing-box.json 695 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-112252/sing-box.json.before 693 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-112611/sing-box.json.before 807 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-130912/sing-box.json.before 807 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-134634/sing-box.json.before 775 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-135815/sing-box.json.before 666 bytes
/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-141254/sing-box.json.before 1132 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131030/sing-box.json.before 775 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131211/sing-box.json.before 775 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131345/sing-box.json.before 775 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-134806/sing-box.json.before 666 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-140332/sing-box.json.before 1132 bytes
/root/v7-install-backups/proxy-public-enable-happ-test-20260509-141307/sing-box.json.before 1132 bytes
/root/v7-journald-limits.conf 69 bytes
/root/v7-migration-extract/etc/amnezia/amneziawg/awg0.conf 420 bytes
/root/v7-migration-extract/etc/amnezia/amneziawg/awg2.conf 587 bytes
/root/v7-migration-extract/etc/amneziawg/awg0.conf 456 bytes
/root/v7-migration-extract/etc/sing-box/config.json 1259 bytes
/root/v7-migration-extract/etc/wireguard/vps.conf 238 bytes
/root/v7-migration-extract/etc/wireguard/wg0.conf 416 bytes
/root/v7-phase24-admin-roles-backup-20260507-002627/auth.json 418 bytes
/root/v7-phase25-admin-accounts-backup-20260507-004218/auth.json 418 bytes
/root/v7-smart-clients/quick-040cad24-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-154c65bb-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-19d80844-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-3a12a3c5-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-5a74c0a3-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-65977141-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/quick-7330cdec-iphone/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u000513-iphone-83aab2/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u001357-phone-2abf80/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u001357-phone-7addd9/karing-auto_travel.json 1962 bytes
/root/v7-smart-clients/u001357-phone-9a5a0c/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u001357-phone-bd0f69/karing-auto_travel.json 1962 bytes
/root/v7-smart-clients/u001859-laptop-0ffdb7/karing-auto_travel.json 1964 bytes
/root/v7-smart-clients/u002853-laptop-e5d569/karing-auto_travel.json 1964 bytes
/root/v7-smart-clients/u003833-laptop-5d7eb2/karing-auto_travel.json 1964 bytes
/root/v7-smart-clients/u234567-iphone-dabe50/karing-ru_local.json 1647 bytes
/root/v7-smart-clients/u497791-iphone-613cf0/karing_wg-ru_local.yaml 793 bytes
/root/v7-smart-clients/u497791-iphone-613cf0/karing_wg-ru_local.yaml.meta 513 bytes
/root/v7-smart-clients/u497791-iphone-98f10b/karing_wg-ru_local.yaml 1010 bytes
/root/v7-smart-clients/u497791-iphone-98f10b/karing_wg-ru_local.yaml.meta 513 bytes
/root/v7-smart-clients/u497791-iphone-a12c00/karing-ru_local.json 1915 bytes
/root/v7-smart-clients/u497791-iphone-a9e43d/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u497791-iphone-awg0-smux-test/karing-ru_local.json 1738 bytes
/root/v7-smart-clients/u497791-iphone-awg2-smux-test/karing-ru_local.json 1878 bytes
/root/v7-smart-clients/u497791-iphone-b0317e/karing_wg-ru_local.yaml 793 bytes
/root/v7-smart-clients/u497791-iphone-b0317e/karing_wg-ru_local.yaml.meta 513 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d-mux-test/karing-ru_local.json 1922 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d/karing-ru_local.json 1915 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.json 2277 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.json.meta 532 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.yaml 792 bytes
/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.yaml.meta 513 bytes
/root/v7-smart-clients/u497791-iphone-cf7147/karing_wg-ru_local.json 2144 bytes
/root/v7-smart-clients/u497791-iphone-cf7147/karing_wg-ru_local.json.meta 543 bytes
/root/v7-smart-clients/u497791-iphone-wg-endpoint/karing-ru_local.json 2003 bytes
/root/v7-smart-clients/u497791-laptop-2e8c0c/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u497791-laptop-7ca2f7/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u500069-iphone-4e45ec/karing-ru_local.json 1915 bytes
/root/v7-smart-clients/u597791-iphone-562fe0/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u597791-iphone-fa9458/karing-auto_travel.json 1963 bytes
/root/v7-smart-clients/u614825-iphone-b1c407/karing-ru_local.json 1915 bytes
/root/v7-smart-clients/u721171-android-ca87f8/karing-ru_local.json 1919 bytes
/root/v7-smart-clients/u721171-android-e4ad8e/hiddify-ru_local.json 1979 bytes
/root/v7-smart-clients/u741661-iphone-b000a5/karing-ru_local.json 1915 bytes
/root/v7-smart-clients/v7-iphone/karing-abroad_ru_via_v7.json 1739 bytes
/root/v7-smart-clients/v7-iphone/karing-auto_travel.json 1951 bytes
/root/v7-smart-clients/v7-iphone/karing-ru_local.json 1635 bytes
/root/v7-smart-clients/v7-lab-speed/karing-ru_local.json 1879 bytes
/root/v7-smart-clients/v7-lab-speed/karing_wg-ru_local.yaml 793 bytes
/root/v7-smart-clients/v7-lab-speed/karing_wg-ru_local.yaml.meta 486 bytes
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf 321 bytes
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.png 1132 bytes
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf 249 bytes
/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf 343 bytes
/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.png 1258 bytes

## candidate_classification
### candidate=/etc/wireguard/v7e06a394c478.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/etc/wireguard/v7execwg0.conf.e25_7_before_keepalive
sha256=c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed
size=319
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.89.0.2/32
MTU = 1280
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/etc/wireguard/v7execwg0.conf.e25_7_before_mtu1200
sha256=cf300a37917523ab6ba9975f175fac60bb5f0e9d93619c8197ddc6ef653e7e3a
size=319
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.89.0.2/32
MTU = 1280
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 10

### candidate=/etc/wireguard/vps.conf
sha256=dbc463e711667f2d8d6ed87f191f4b2c17bb5d2eada29e6f363bf6a28de3d3aa
size=238
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=0fd7d1aeb7daa3a96765cba18ac0e87419408dbea3b5e84fd7593c841f99b962
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.0.2/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.10.0.2/24
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/etc/wireguard/wg-client-test.conf
sha256=07c394ed0bd33f0b0877d11d8ba066587d588979c8ad5345dcc9b709313c2bb5
size=697
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.89.0.1/24
hooks_present=2
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.89.0.1/24
ListenPort = 51889
MTU = 1200
PostUp = sysctl -w net.ipv4.ip_forward=1; ip -4 rule add pref 189 from 10.89.0.0/24 lookup 189 2>/dev/null || true; ip -4 route replace 10.89.0.0/24 dev %i scope link table 189; ip -4 route replace default via 195.2.79.1 dev ens3 table 189
PreDown = ip -4 rule delete pref 189 2>/dev/null || true; ip -4 route flush table 189 2>/dev/null || true; nft delete table inet v7_wg_client_test 2>/dev/null || true
AllowedIPs = 10.89.0.2/32, fd89:89::2/128

### candidate=/etc/wireguard/wg0.conf
sha256=ada6054ff7e1804f9d3d5ebb0ac08878a528cca1f06e7e96282e329476f917e1
size=2963
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32
AllowedIPs = 10.7.0.12/32
AllowedIPs = 10.7.0.13/32
AllowedIPs = 10.7.0.14/32
AllowedIPs = 10.7.0.15/32

### candidate=/etc/wireguard/wg0.conf.backup.20260506-163303
sha256=693d11a9966026aed32a68e50ea268196047232b152e9a8786419791cb8d5965
size=416
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=4
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o enp0s1 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o enp0s1 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.iphone.20260506-164945
sha256=1ba82615f10904ee39f6373095eba07c7df6d6049e6fc4b48005a38dbebbcd54
size=412
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=4
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.nat-egress.20260506-165513
sha256=f5197f7ffef2d0aee24bb76771506bf71d244c98d5ccfe892e14f6f4eb052089
size=523
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=4
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260506-171016
sha256=79c964aba4b2865c447c23cd93823736cb66058b3d0ab29aea7dfb4925230f46
size=835
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260506-195020
sha256=79c964aba4b2865c447c23cd93823736cb66058b3d0ab29aea7dfb4925230f46
size=835
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-161819
sha256=74e46d4074f2fd01d0fc876b6420a56b24d8482bb72c00f892326624ac4db918
size=836
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-161923
sha256=d5ffb68feed7ecea8dcde7039c07f0cf484e260ba5605ce1efadce1698bc5d99
size=959
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.4/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260508-162703
sha256=a861b76c1e1cb8df2c63a0b4f11b11852d1279d0ac59cc5dd2ecb71cdd859de0
size=837
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260509-095148
sha256=5c7a3a2e4a07f2e8410de24d6e57bc0c715131832c9995cb6b15d6159fb486fb
size=960
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-223215
sha256=21653490a34df7cf5028a044d7fcc00b936f9a8bde08d0cc74df066393a0200d
size=961
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-223355
sha256=510fe5bb119e8a7c5f2e07223d782ba46b00165f3673a4cbd509ba5d6657254a
size=1084
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-225923
sha256=09d3dd71e5416a112af2f8ed14206bd90f8541d57932a3a9989b2ef14d3201f3
size=1207
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260512-225941
sha256=744e367414360445f6700fb3956ee3873149e5a5348e04b6ce5ad303f331d900
size=1330
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-162145
sha256=27e11b53168929aa40416389c6b1515d276d21960a0b64c7fe25c7604ed46bdb
size=1453
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-164331
sha256=54374cbd3d8b0d3160de1e028c09800686c0ab4af236defec3a934a39c483084
size=1576
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-172826
sha256=38f1132c47a6dc6d9f48fe43861a3da240a46ead8c2f4d0935600a34a81c88d2
size=1543
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-215434
sha256=9704329f16a1a23e762583cb059bd854c9597f0d8bf388b7923f7e2d90e0b167
size=1666
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260513-215821
sha256=389331a8c27e9399939b86c9586d33d0656031d9b2b956132a2a91e9c85247eb
size=1790
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-001900
sha256=40bd12faa1c6fca961675936cd9920814002ec9c6be6d554cf1790f08f0924d6
size=1791
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-002854
sha256=579cab29927fccd8aa80b4f6c6f2606af65a5f0316e9ca224f76f16fe7fa6bca
size=1916
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.0.0.11/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-003507
sha256=bf64ebf7c5c69921f0bc90831a305c22de2e4199cc13eb48dffe0e17435d5f9d
size=1792
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-003834
sha256=a675b141554f2bcc7a6dea0b161decd8c19fe4b77eaa54fba8f3ea099a4f46a4
size=1793
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004008
sha256=00ae1d157129c6bcc4493ee4242f535d781d4e581a03079032dcff0d672724da
size=1794
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004618
sha256=28cc024ea57ef1949ef27da99ecc86caef59d58cf6045814b8f817b03ed2e447
size=1795
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-004748
sha256=6cb303dfb5463e47512dc95d4553207288069134051af9ca8b99c31bbedeee21
size=1796
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260514-212852
sha256=896c06dba828e4983ce6816e133b9bd3bc0cb3fde2886c25293b66f808a0f20b
size=1797
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260515-073929
sha256=7cac3484a091114a280cc33222563cbb88c65c5bdf7f01f96cc162be81c3aecc
size=1920
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260515-074517
sha256=4074397744de16538ac47cff090f62e23cbb6f0f6ea033339072d83890e00c94
size=2043
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260517-174520
sha256=a9f9a09b01f537212b2e03728b921f7aaea3aad4c734b1e8ef8a7f9be20f7bad
size=1085
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260517-174942
sha256=b78e446f4d8eedf41f62d432965dd33cb3b767e146ce39cfaa707bf0e62b5783
size=1207
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260518-143340
sha256=c8e111343a91b5ff39b2eb5bf1d654df18fe4067c67c5036c46079ef30c0a3c4
size=1329
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260520-231105
sha256=935ab81d5eaaa90065da072adbb9937dbab7c071ef93256b64820adf208a7487
size=1762
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-133329
sha256=482e7686c04ce628ff22743653010ac99025a2b4b933c8558e7c711ca84aa607
size=1885
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145816
sha256=ecf304d7dffb9eb700558ce23f8f7f2316b9bc43e30fc0488c735f15a1682416
size=2008
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145831
sha256=4efee0cfe496c9a9035ada8389e39c5bf016cf4124d227eeb722faaa1af2e09a
size=2132
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260521-145841
sha256=d99fb66d2c47de63e171865e5f7cc77868c8cac2a58b4148f36ead1d5522af54
size=2256
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-154617
sha256=3641cee83af33c13c6d0adb6c7b65f00e219115f4a1e7c1d5fd6d1a2eb99514f
size=2380
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-160728
sha256=4201d40ff3ff3e19d454ebd722ad4dab0f807ef00b00e8a2439f4debbfa92932
size=2505
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-160743
sha256=f0e8d9a9259695e5573b2531fda1e450481cb656f46a01106ff92f2512efe474
size=2630
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-161435
sha256=5a6f55f5ebfa2625d3106b54a3a434250ff128bf4d95f1923bfdfd630a85b37d
size=2755
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32
AllowedIPs = 10.7.0.12/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260522-162731
sha256=4dc35631f39ad09c72c6d34f9d93f13c098460f0f22250bca19270dec536fe72
size=2880
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32
AllowedIPs = 10.7.0.12/32
AllowedIPs = 10.7.0.13/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-create.20260523-145551
sha256=eaa6cf3631d8a31a6d9c0f7fb9e3f2a666fe35908927fd28b984bba2a6720a5e
size=2838
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32
AllowedIPs = 10.7.0.12/32
AllowedIPs = 10.7.0.13/32
AllowedIPs = 10.7.0.14/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260506-195117
sha256=de0b9683224f143ffac8135560456609ca5d83d82c374cdcdb1ac8c43590b4ba
size=955
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.4/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260508-162631
sha256=8729c41a76f92a2e98ec3b4a3f3cd663f92f63688023ea658b3cddccf8521934
size=926
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.5/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260509-095150
sha256=fc660f5a9685357debc2719e30c13e1afd3d9fa3b1d5d6d728b302179905227f
size=1081
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260513-164950
sha256=69d5435e11e23f744198a26772d151c0cda012859da97a52a9d95f34c6dcaf84
size=1699
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.7/32
AllowedIPs = 10.0.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260513-221130
sha256=41565d476d0fd62a069e1c237d965f50e1aee9f0c637ce1f92a1a69a94ac8504
size=1914
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.0.0.11/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003316
sha256=3ed5e0f2c5705c28449f3ac5e8d855636568bccff5bf1d111321ace1b5730056
size=2041
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.0.0.11/32
AllowedIPs = 10.0.0.12/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003317
sha256=a25c89420fb2ab3d3f752fde347f58f87a746b29422eb9fb85333608d7cd40ce
size=1882
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.0.0.12/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-003509
sha256=614966a83e65f26405ed70a6506512c685e307923d1db2c6a56fc3974e9a3aed
size=1915
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004007
sha256=539b081f6d143f68df20b5f2141e3f5857e53a3465fa700ea89444e1d4eb20f0
size=1918
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.0.0.11/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004617
sha256=18286c20e1af8749fa08c40188c6c058b171152d95afedad26a5549a804e5531
size=1917
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004619
sha256=15ce5d4014b0e4f792008d603e48c62062a6bccd7fcdbcd034ed5bc327ae43a8
size=1918
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-004749
sha256=86ae98e47102436bb3f789ec424b2b14a9f45e0134115528f0ca23de91cfd262
size=1919
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.7/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-122954
sha256=896c06dba828e4983ce6816e133b9bd3bc0cb3fde2886c25293b66f808a0f20b
size=1797
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260514-123441
sha256=896c06dba828e4983ce6816e133b9bd3bc0cb3fde2886c25293b66f808a0f20b
size=1797
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163115
sha256=03821d1bd7348fe8e3f6d07dd0bb7aab019d90c47f5ac804a6eb8dcc31724ecf
size=2166
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163124
sha256=03821d1bd7348fe8e3f6d07dd0bb7aab019d90c47f5ac804a6eb8dcc31724ecf
size=2166
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163131
sha256=4655814f0aa0196ccd0f21f24293f38f102bdec7998c17bd699d6e870dffb878
size=2010
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163140
sha256=4655814f0aa0196ccd0f21f24293f38f102bdec7998c17bd699d6e870dffb878
size=2010
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163203
sha256=06002e750ba4944c4a8cc1a664e22f7d377bd5a85512c7f731b39ef70472ea36
size=1854
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.8/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163217
sha256=1a36463f784bca54690f477bfd3960905e497dd47d1dde805c0408dc06ca6266
size=1765
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163221
sha256=0ce2445852ba780b4d7200a3a9dacf1c62758b07d7b07d8ab20d6552fba38f4b
size=1642
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163241
sha256=d50dca0b7989ba2daf37320979df5cf9e0d52a2bb49a0d9ea39212ed27bdac3c
size=1552
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.0.0.8/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163247
sha256=13c17fa03969c2a62855d7ff7157ecb2fa727fc200d26aa2ff4944f8eded677e
size=1429
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.0.0.9/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163256
sha256=4c25ee342f93028a6baa1814f0770c0c4dcd9d5b09f7f1da645cdbbfbf1aabbf
size=1306
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.0.0.10/32
AllowedIPs = 10.7.0.2/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260517-163259
sha256=a10c8558316d982c248a545d0426db39036b096ea1f08723813b9bd2b53e537c
size=1183
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.0.0.10/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260520-231014
sha256=0d64f125656991f4417a4ab85e30f500e935c44223a5ff2b43f571e50f37a680
size=1884
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32

### candidate=/etc/wireguard/wg0.conf.backup.v7-user-disable.20260523-145431
sha256=1cef87092f4e6f9842abf2c56db62eee9683b497e2105fd339bb1a72d9974ab7
size=2996
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32
AllowedIPs = 10.7.0.6/32
AllowedIPs = 10.7.0.7/32
AllowedIPs = 10.7.0.8/32
AllowedIPs = 10.7.0.9/32
AllowedIPs = 10.7.0.10/32
AllowedIPs = 10.7.0.11/32
AllowedIPs = 10.7.0.12/32
AllowedIPs = 10.7.0.13/32
AllowedIPs = 10.7.0.14/32

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-1779291888-b0b382/result.json
sha256=305e14e296e246422b0a53fbae2c91fd1106527bd77f72cdc4343ba7f0e3563d
size=1747
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-1779292334-17bc7f/result.json
sha256=a364d8ee97c67e888ed41782595932b628d86de7a08c1f6f2a3c9b1aae526e11
size=1747
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291888-968d6d/result.json
sha256=9eb9869f545da610e63caf30c4cb148243df6417478b2cc934581f964c181e74
size=2501
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291888-968d6d/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291889-8e4594/result.json
sha256=a38a37127393dc43554157a81cf54f317131eb044fad46ff97ae61fa2537a1c5
size=15004
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/1-1779291887-55965c-runtime-1779291889-8e4594/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779212551-5f2af4-1779212567-d21edc/result.json
sha256=36f3bbfc569b06161a406ec67c0b2aa97f9b131921d9ac21f21faa25cc8b0a59
size=1725
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779212551-5f2af4-1779227526-6b3483/result.json
sha256=4eb0aab587ef2bf4fae3dcace9a10226aa0df9574bb326378ee855196cd5c57a
size=1725
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-1779227953-9968ee/result.json
sha256=6b320a2d88de44655e956e3fc7e977843d2dbacf42fe822b4a9a2a79cf8e4a2c
size=1740
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779229741-d72ffe/result.json
sha256=162e27616810763278f2e114c5f0dd2ac4c44991a05d4398eb89ec13921a8219
size=2306
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779229741-d72ffe/sanitized-runtime.conf
sha256=13c4581005bb0a85618f94b370f91ff2faa3deab63c7b505d2b32685386bc0b5
size=318
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230366-3b4957/result.json
sha256=9ec6795166802f02e72f06b5289fcff5c0762f6d82a2ce73ec502a65760514de
size=2495
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230366-3b4957/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230578-730443/result.json
sha256=3f1da2b9b117c02c21a39396da2ccbd61418024869044640973702491217baa1
size=14998
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230578-730443/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230717-01826d/result.json
sha256=7c2678ca96b3e0417c553962c70a76a529eb1115d803c28422aaa5bf66e83d63
size=14942
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230717-01826d/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230774-51cf55/result.json
sha256=ca29a42d13ed7348c656e3c61eadc3be82a369ed1ceed6cf1f757c728c4ff350
size=14982
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779227510-8c08e7-runtime-1779230774-51cf55/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-1779303737-cf3f93/result.json
sha256=895afbc952f0bcc16d84e453516779a88cf2fcdb78775e3ee17a51f8b3e7e3a0
size=1740
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303737-dd22ec/result.json
sha256=cb7f0153c58757c244ddc23bc47a17311759983ed6bdc9a655ba5977ead15a01
size=2494
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303737-dd22ec/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303739-2a8b85/result.json
sha256=da5fb53b860e019a07730b2f2a9dd35b00e05f85439426e630c7c6b6ca437b49
size=14970
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779303737-a57ce8-runtime-1779303739-2a8b85/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-1779305909-440a3b/result.json
sha256=dfd3ebeb398f2fc81aae40a7bb4f98d96236afdf218a0ad17b8f6823966ab250
size=1740
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305909-f16c54/result.json
sha256=9a6848e20e6cc3b6533355828818e83878a54c9ccbe222b25bc545331a93599f
size=2494
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305909-f16c54/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305911-2fff97/result.json
sha256=48f30e604acaa422ee2a75bea9e292fc983fe53078485acc616679f62f654cb8
size=14953
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/amneziawg-1779305908-ed3889-runtime-1779305911-2fff97/sanitized-runtime.conf
sha256=e3cb20eb64f288e521c7403082e0e7f24096ce49df575e48dace71e3934e62bb
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.10.120.8/32
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779352711-bc94ec-1779352720-8888d9/result.json
sha256=3408e1646bfbf3f0b1b28b0911765e6117857ba27bb22aeb52934229def7374f
size=1437
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779352711-bc94ec-1779352724-980fad/result.json
sha256=e4830a853dfa8220b4efa33553d44f3be57929a64a1f8829dc9c5794db6123bf
size=1437
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779352726-16e1ec-1779352770-db864f/result.json
sha256=6d7616754f5a7cdda004a5bd091ec832f2c645ddac6c7222d81f323a0f1a9027
size=1437
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-1779387408-07b64d/result.json
sha256=a322774b7ea6b49c9daa603e361a87aff3810e29a5df546f0eafe7e70213fb53
size=1597
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-quarantine-1779387409-966d63/openvpn-runtime.ovpn
sha256=0d671493f17fb5bb1c271985af10fb8807c40b15e7a24f25b61f7e0acf437cd7
size=9777
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=53f6933b6294945eb108a76ce34e9140d6763c623a45f3b9fef5234d70697e25
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ovf9f3b6ec
script-security 0
remote <redacted-endpoint> 60826 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-quarantine-1779387409-966d63/result.json
sha256=d273d4f19b97a59493c6c87a0bcc5754a5ba523ae35b6089448358d6ee0f3e0f
size=15157
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-runtime-1779387408-adb23c/openvpn-runtime.ovpn
sha256=ebb5fa39ca8f85a9557e76ce479f935f29ea0d582270cc1e53a3cadd9b5ce473
size=9777
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=53f6933b6294945eb108a76ce34e9140d6763c623a45f3b9fef5234d70697e25
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ov7283e3ff
script-security 0
remote <redacted-endpoint> 60826 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779387408-c42bdf-runtime-1779387408-adb23c/result.json
sha256=34b827a147fad59249d5f33f19ccca93cc871417e79ca00521e2cdb9e80e3d32
size=5642
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-1779388847-4cb017/result.json
sha256=bbb9b4be45fae750b1fca85d3c58af15525e67fd0360364040e520bad4f58d65
size=1597
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-quarantine-1779388848-158247/openvpn-runtime.ovpn
sha256=f6875f0f14d95b27e9e6c1a05d6caa79f315c36aa2175f47a2d9eb6e7b2da1c9
size=9777
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=53f6933b6294945eb108a76ce34e9140d6763c623a45f3b9fef5234d70697e25
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ov2e3132c2
script-security 0
remote <redacted-endpoint> 60826 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-quarantine-1779388848-158247/result.json
sha256=8c6604f29c845091bb559a6706b741e0d5f66724850b1b7b7e9b546ba9c26d4b
size=16639
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-runtime-1779388847-af3427/openvpn-runtime.ovpn
sha256=ab348eb5889fc21a10e1e314f8c99de376c1ac254ee1f777483b0cf537b55e80
size=9777
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=53f6933b6294945eb108a76ce34e9140d6763c623a45f3b9fef5234d70697e25
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ov62696376
script-security 0
remote <redacted-endpoint> 60826 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779388847-d2ad7c-runtime-1779388847-af3427/result.json
sha256=bb3245e2c1480dd83ce939204c404aba28708f24a1aae097a91c996ca593d7d1
size=5642
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-1779453676-d82055/result.json
sha256=361c81a1edb01b1eb491103ea2bbaa66e5d510011310168dbeee2ac10c645963
size=1597
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779453676-afdc62/openvpn-runtime.ovpn
sha256=bbd625b1290c9d19be9ee1ae99f0398108700414db18e83c8b1b2c7eb5bb07e0
size=9739
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=cf97918def748528f0dbf1ee9eb9245bea24f416bcd8076c986eb75b28238d51
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ov08bf2e12
script-security 0
remote <redacted-endpoint> 25065 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779453676-afdc62/result.json
sha256=f0ab6e90d430106e2d0a252ea480d41abc74f03611433d63b390369da8fe855f
size=2259
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454017-3049b4/openvpn-runtime.ovpn
sha256=ef99f100878e6ba481de3fc8b936ba07da91eab6fbf2728d9ccc57c14838a51b
size=9739
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=cf97918def748528f0dbf1ee9eb9245bea24f416bcd8076c986eb75b28238d51
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ov4fc11eb2
script-security 0
remote <redacted-endpoint> 25065 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454017-3049b4/result.json
sha256=8bd586ff416c56142e36ee29ebb931cfe3eaad89278d9d9fa5b6b957ee91e249
size=2259
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454375-4f05cc/openvpn-runtime.ovpn
sha256=2d09c50eb44e7df420bc93c817a715ff013a10247a4321dce0a3e13f0d2c6ec7
size=9739
protocol=openvpn
endpoint_present=true
endpoint_host_sha256=cf97918def748528f0dbf1ee9eb9245bea24f416bcd8076c986eb75b28238d51
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=NONE
hooks_present=1
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
dev v7ovea912cb7
script-security 0
remote <redacted-endpoint> 25065 udp

### candidate=/opt/v7/admin/egress-draft-tests/openvpn-1779453676-42885e-runtime-1779454375-4f05cc/result.json
sha256=70d6c0cd7e637e40d5dbdb471bd3fa19e43b68ee783fa3446d41e015943c4c61
size=4711
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/subscription_url-1779462892-4d2cea-1779462892-48c0db/result.json
sha256=28a743177b3932e127721ff9d0b4c7679aada3eeb05581567aae4cd0cf9f46f7
size=1010
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/test1-1779352953-489ac4-1779352997-9f7005/result.json
sha256=2c0f77a5473ac906ae02de105c3f62b35c86c837871f2e21b58d5b46b05e410a
size=1413
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-1779455931-4d4466/result.json
sha256=9481478ad2cb5d10ad9fde0c6b5c08f9d6a3d15181112da602b622656a849e13
size=1771
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455931-abf4ef/result.json
sha256=88944e2628202734789eb69383959641b16685c2fb757fcc986449d1d6400ed4
size=2155
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455931-abf4ef/sanitized-runtime.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455932-39b6db/result.json
sha256=a2a66f2242b435abcce3ed4ff35caa0b82feb7623957f3080f6d9bc3dd9d0995
size=14573
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wg-1779455931-ba621c-runtime-1779455932-39b6db/sanitized-runtime.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-1779454504-488966/result.json
sha256=2899950c38cb539b26260c91b7f5f075be3529400dac41d0e2e99dc2fc8664fc
size=1711
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454504-db9ec5/result.json
sha256=a9a40131d08a5c607c374b2d4d88e251430ab5949eaca518506f1432cae1dc6a
size=2095
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454504-db9ec5/sanitized-runtime.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454505-0be4c3/result.json
sha256=9e2d2e413985d0b9835e35b161b67ee777cb812a83f4152c64db623cb3309255
size=14518
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779454505-0be4c3/sanitized-runtime.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779455648-10ab7e/result.json
sha256=d2abe24ab1eb118e83f9230b3832221a270c9f18759dd44a1bab35c131898f8a
size=14521
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/admin/egress-draft-tests/wireguard-1779454504-c43409-runtime-1779455648-10ab7e/sanitized-runtime.conf
sha256=2aff3d45ee30e85cd01e156168cf16cfccdc97c17007e3ba0d0d49aad7aa32fe
size=315
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=ec8b7019d0775e65aaffee979d14ef014ad2a77cfe5ed9617a268a4475b9a2b5
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.0.17/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.8.0.17/24
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 0

### candidate=/opt/v7/backups/final-state-split-ok-20260505-234252/v7-run-amneziawg
sha256=777971dba3a054d8f1164caa9b149300f829502497ce85d45b3d044bcfea4c69
size=293
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/backups/stable-core-20260505-230621/v7-run-amneziawg
sha256=777971dba3a054d8f1164caa9b149300f829502497ce85d45b3d044bcfea4c69
size=293
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/backups/stable-state-split-20260505-233947/v7-run-amneziawg
sha256=777971dba3a054d8f1164caa9b149300f829502497ce85d45b3d044bcfea4c69
size=293
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/amneziawg/awg-test-194.124.210.244.conf
sha256=0267b9842bc1e0216c58fcd3bc2295b081b668f65ab51b7d6d81729c56ab47d4
size=456
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=b89a5f0aa892457a9ffc47fa76e2338d188090b92df54235f158c3d1126505f0
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.1.10/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.8.1.10/32
DNS = 1.1.1.1, 1.0.0.1
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/opt/v7/egress/amneziawg/awg2-94.241.139.241.conf
sha256=aae6505de98e57ff082e5369a6e69a3dba6d9bc6104f5b7da9b286e7247a3777
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Table = off
Address = 10.10.120.8/32
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/opt/v7/egress/state/autoswitch-restore-barrier.json
sha256=f5f37e9595f87233939ed067ef25e58c500adae687de4090a8c1832140571079
size=598
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/autoswitch-safety.json
sha256=e13fcf81c723247ac0781c95206fc8fdc55bc5791ca696b39fb5aa5768d50083
size=34510
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/awg-test-194.124.210.244.conf.state
sha256=cd4de3c65774b9e374fdaa91bc3557cbd765988b78a135658279b670f0d1607e
size=197
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/awg2-94.241.139.241.conf.state
sha256=d15987be53a99ea74059b542c5b27a29a4385401d9261a3bb683700465118c92
size=218
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/client-agents.json
sha256=89ff59912822f5c7e23c8252e5108394f111f7cc8ce1930ece928592e3a36eba
size=421
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/client-commands.json
sha256=a96d77a48ce8bfb00fe2c64ded8fd6123a2cd4019fca55eb0137d9b868dec2ad
size=4079
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/client-reconnect-state.json
sha256=6bd9d8d1e32c48eb36eb1c67d2ee163c2bc15358e63c56f8f758d3757c723ed6
size=4755
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/client-speed-links.json
sha256=3582a8b079fba1674e06906a60fb4e3e35f092868dbee953242b3ef4a0cdf453
size=68
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/client-speed.json
sha256=44eb12c56933e21fe11ef1bff98cc848e5e7935d9ebc0f6115d9ff77cfbb6ee9
size=18770
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/egress-labels.json
sha256=ea956faee2681a0d3fd8ab8ab4398648ed1369bf9448e5089dcbb1c2243f9b59
size=191
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/egress-load-summary.json
sha256=829efe0293d99aa1edab467ba8b1063743592b768437ac743086a628024d36eb
size=2034
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/egress-quality-summary.json
sha256=dd33c3659cbd901bc18ff0d86b4725fb026c08aeae025c0d0ca473e37e2c3e03
size=10355
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/egress-speed.json
sha256=b399b253cf2c9760e282f8d16a7a94ca7c788c9ddfbcd8f2ec7c471270e08641
size=2153
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/egress.registry.backup.awg3-20260519-2155
sha256=329778be4b658a2fa8eedb1be9c00b36557b9d34616cc50647940d4dcc109caa
size=568
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/path-benchmark.json
sha256=320d2ec0ce58bf1dfa2b6301df0713c041e766a634cc3d869aee99baa770e433
size=19399
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/path-optimizer-advice.json
sha256=36d74804de842f986d07649c0c3cd6ad2ff5ef61b47d092f8c7310ba57804948
size=1801
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/path-samples.json
sha256=48d968204edf7fe7063cee329d081d005be09533bf02e2219fa0f7cef4bd1ab1
size=2796
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/profile-delivery-tokens.json
sha256=32f852f0709ccb3922317484bfaedeef4a39815a7f68526dae193f26394fe58d
size=34217
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/profile-delivery-tokens.json.backup.awg2-smux-20260519-165553
sha256=67cc6cfdb556162cdd4b3f39346002903be464d6dec5fbc2e9604e63b7236a68
size=24261
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/service-matrix-refresh-summary.json
sha256=f570a2ccb3cd891fca58823ca9e12f24a396baaf3f21510b482b76830fd79360
size=16110
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/service-matrix.json
sha256=144638d27d6a86cdcf01beb657f4c25ceb3d2bf2f15e6d303f4a1f7256363e05
size=101064
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/service-matrix.json.backup.clear-telegram-awg2-20260519-135350
sha256=53180965c00363be53234c37bb5c24981dd8b11407e2faab8033e799c598e828
size=52470
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/service-preferences.json
sha256=4eaa0c3aea66c8b414d4b8fb44d01a19ff9e10ade17fcb568c0ee9d169b8c611
size=466
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/telegram-sentinel.json
sha256=6b927fb5f3fcc894ade6f8df026e399896bfa6fe3c8e87363aa4fe3c2609438a
size=10620
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/v7-state.json
sha256=755d2f7fadac27a5a1ba8e16b66fb86a33b338666c38134650659adb9456af47
size=10179
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/egress/state/vless-activity.json
sha256=b7068293eb77f8facd56894c282f4d09bdbd20b9f7162d7055db7aeb2a654a66
size=1353
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/legacy/bin/v7-run-amneziawg
sha256=777971dba3a054d8f1164caa9b149300f829502497ce85d45b3d044bcfea4c69
size=293
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/ops/deploy-baseline/20260523T122251Z/contract-summary.json
sha256=c8bb1593ca02643c89d042bc3e839104537ebf5196ad3a8bf1af963a1bd73e8b
size=9671
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/opt/v7/ops/deploy-baseline/20260523T122251Z/unit-summary.json
sha256=281927a4dc44f1c97a69220093fd520a9283e6a179e06fc38e49baebe0158a2c
size=46686
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/amnezia_for_awg_direct.conf
sha256=29f06a9a9f3950b515e7e1a453a503b0815eff1d0b583c383ede12acabd9a916
size=462
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=b89a5f0aa892457a9ffc47fa76e2338d188090b92df54235f158c3d1126505f0
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.1.13/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.8.1.13/32
DNS = 1.1.1.1, 1.0.0.1
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/root/e25_7_continuation_v7execwg0.conf.removed.20260528T123323Z
sha256=c8621f5b3a07a1753a1d4143783de32cd251350cea6e65d0f84ded487753b2e5
size=319
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.89.0.2/32
MTU = 1200
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 10

### candidate=/root/e25_7_v7execwg0.conf.removed.20260528T121350Z
sha256=c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed
size=319
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Address = 10.89.0.2/32
MTU = 1280
Table = off
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.conf
sha256=f88e8a35bcf3e3b8c718e91d5f2241dff3306bc683d6419f0f031a466ff7a4b2
size=430
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.88.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.88.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.png
sha256=4acd3f440b277be7f510712c6d19bd4eb3f0c2668a07e2ce7bdc60b29b6c63a4
size=1523
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.redacted.conf
sha256=ce651c190f205ce50f5d24d3cced8d80625f950578f07b2521b659aeb32e4fc6
size=322
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.88.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.88.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-awg2-smux-test.db
sha256=f7f6d9e9f34ea4bcdcfaaf472f624fc2bf67262cf14d1a4f8ac2c1c09f7b77ff
size=32768
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-backups/usr-local-bin-archive/20260523T122936Z/skipped-files.json
sha256=37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570
size=3
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-backups/usr-local-bin-archive/20260523T124646Z/archive-manifest.json
sha256=e61509bc62c8096b156dffa186626cc3bda7115a25b1154baf8a9b6bdfadd81a
size=4724
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-clients/quick-040cad24-iphone/quick-040cad24-iphone.conf
sha256=1a43c094c5774f823e5595364f07f02c12930a4fa5d4c0e5c1392095831f105d
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-154c65bb-iphone/quick-154c65bb-iphone.conf
sha256=25dd9a02822fd4898d2851df5e6517a7edccbb3093f254891c674b63ceb070c6
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-19d80844-iphone/quick-19d80844-iphone.conf
sha256=38bbe18999ea93c3d054be01557fa87cb9bc6ebde51acbc20424120fb4fdc2ad
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-3a12a3c5-iphone/quick-3a12a3c5-iphone.conf
sha256=1eafe754f00a98b8a3a0682da0f9b7ba0e4ffdfc89faa822c9310e208495a321
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-5a74c0a3-iphone/quick-5a74c0a3-iphone.conf
sha256=42fb078263075a1857fb69e878c6232b176d9e509c41124897dfb7109d8e96ac
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.4/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.4/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-65977141-iphone/quick-65977141-iphone.conf
sha256=be48e2ea4d1f394ab25e156e5653011cfc61462587fbe886f4b07030f78f8b43
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.8/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.8/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/quick-7330cdec-iphone/quick-7330cdec-iphone.conf
sha256=97f8de8e8744bef236614a06251fef7bf3f427bca93e7a772e6f42a3a6519966
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u000513-iphone-83aab2/u000513-iphone-83aab2.conf
sha256=cd191f0a89d586c44644dbcb145b675b7074a23c0d51ce38ad29c673603a41ed
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.9/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.9/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u001357-phone-2abf80/u001357-phone-2abf80.conf
sha256=7dfd3263b154b31abe7550a0f49abdcd33ac3a9c556bed0e34d801193739243f
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.11/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.11/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u001357-phone-7addd9/u001357-phone-7addd9.conf
sha256=bae34cda791c20198e1b042b27a66ebc90271d6a8d60c20018ac823bdd2e26f8
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.4/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.4/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u001357-phone-9a5a0c/u001357-phone-9a5a0c.conf
sha256=6ca985ec6773260dfcb81a5fc425981227cb605883d1e7cc11684be1362be958
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.10/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.10/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u001357-phone-bd0f69/u001357-phone-bd0f69.conf
sha256=be3044ab16db1686e6a5b2b34668a2a727f0be12d779eb4e527c6060a84e6fde
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.2/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u001859-laptop-0ffdb7/u001859-laptop-0ffdb7.conf
sha256=f09659ad39116c008c0e1b5e7c374d99c850d0f1c7e076c7f7a27bf5cb512a51
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.11/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.11/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u002853-laptop-e5d569/u002853-laptop-e5d569.conf
sha256=6c63db9702f0b3b28ab574f181634a13c1c527f2f3c8ae4810b119db9cbb5957
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.12/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.12/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u003833-laptop-5d7eb2/u003833-laptop-5d7eb2.conf
sha256=45ce3584bb10535e953e9cd3b257b4df8579514a264ad51953c72ea2b7e171da
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.11/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.11/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u234567-iphone-b8ebfc/u234567-iphone-b8ebfc.conf
sha256=5c4ab9bdd16e1afb4f760265f778205096d1defc45ff0b0565814c91e041843e
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.5/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.5/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u234567-iphone-bbefcf/u234567-iphone-bbefcf.conf
sha256=0d32a5d343560b2365f34152ada3abd2bf66c435574d2a508378814892853574
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.4/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.4/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u234567-iphone-dabe50/u234567-iphone-dabe50.conf
sha256=1de9235b2b40c0c42472f9ef967e4575b3cdebdecbb4856d8838c070da868a50
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.6/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.6/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-613cf0/u497791-iphone-613cf0.conf
sha256=fa15d6e41d38667105fcc0651e0d9cb347e22f67c172dba019cc13675963af8a
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.11/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.11/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-98f10b/u497791-iphone-98f10b.conf
sha256=4a38f93d163363375b014be21ea1851e8beea5354ce9b1137e16ecda40494967
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.13/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.13/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-a12c00/u497791-iphone-a12c00.conf
sha256=1da2925e49f0d6e006604c46bc4ebb782e822d18d693b93d9b7467a363ea73a3
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.5/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.5/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-a9e43d/u497791-iphone-a9e43d.conf
sha256=6edcc55bb12fa9feba35606613ad2d8843899e2b67b082640e62055c5df22bb7
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.2/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-b0317e/u497791-iphone-b0317e.conf
sha256=a8519e24c60f058f10b541e708fc837170d2277a3fe8b4b268f367a1ed647652
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.12/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.12/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-b2a87d/u497791-iphone-b2a87d.conf
sha256=a71efd8ac673764c63f2c179fc7426b76142845b8fa15acd978d9f58eca15dac
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.5/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.5/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-iphone-cf7147/u497791-iphone-cf7147.conf
sha256=53fc7ffb848ffbe7462564f2d2919cbc26414b0195907534413a8d2201fc3ddd
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.10/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.10/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-laptop-2e8c0c/u497791-laptop-2e8c0c.conf
sha256=03085bf2646d070ab374fc30a15f02a8853a99ad0b9a2269449501b1b8114cf6
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.8/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.8/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u497791-laptop-7ca2f7/u497791-laptop-7ca2f7.conf
sha256=fcde9f83e1162557166238724a5fd2b1e1f26848245e8ae220bdc26e489cc7d5
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u500069-iphone-4e45ec/u500069-iphone-4e45ec.conf
sha256=3fbb2401f8f1088b90b680ee953cebb0ee85bfeb144bfbd256dacc921d790942
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.3/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.3/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u597791-iphone-562fe0/u597791-iphone-562fe0.conf
sha256=e7fe59b0db4f54cd0ce9d748895e36b61b5b8cfb67d8df4655bef1e977f0b6bb
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.6/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.6/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u597791-iphone-fa9458/u597791-iphone-fa9458.conf
sha256=5517c0168051469203aa0a73d9b25976d1e5be2b8994ba36075f9174705c3869
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.5/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.5/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u614825-iphone-b1c407/u614825-iphone-b1c407.conf
sha256=13f9161eb53db9e1ca0f2918fe7e25d436cb247123a62189000602b323ff980c
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.15/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.15/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u721171-android-be4d23/u721171-android-be4d23.conf
sha256=820143df2710a4252cc505f6f2f6e44daca398fc8dffc04b84680be3b5bc6843
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.8/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.8/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u721171-android-ca87f8/u721171-android-ca87f8.conf
sha256=913f0ae7eb5b8c0e4c0f2a019185d372d3f976245f548f724a686723237d74f6
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.9/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.9/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u721171-android-e4ad8e/u721171-android-e4ad8e.conf
sha256=8900e5ed541d50a37f8b1e673a55775e93c027cc0250cf73dfdac71d05775bf0
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.7/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.7/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/u741661-iphone-b000a5/u741661-iphone-b000a5.conf
sha256=8894d8dcfed8a94494675398f3ef0bae4a0c77437162e0f3c77bfb21ca07e270
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.6/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.6/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/v7-iphone/v7-iphone.conf
sha256=131b2a2b9777e6bff539dd087b244e64001457c76a549c44f9cbf9d5f6f0e11b
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.0.0.3/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.0.0.3/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/v7-lab-speed/v7-lab-speed.conf
sha256=37dd384a80d1d7082a779fdae93212ea57bb237cef65f169c172df78258b9186
size=251
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.14/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.14/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-clients/v7-subnet-test-1000/v7-subnet-test-1000.conf
sha256=c40547b8201a87411e785f92c69d28313d6d88382ff9d08aa09c83a41028e56a
size=250
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.7.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.7.0.2/32
DNS = 10.0.0.1
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-deploy-backups/pasha-karing-wg-profile.20260518-221744.json
sha256=0cf4292d79c9a5feb518deda46a76e9204ecc534e854aef6e38e6ac42797b29b
size=2066
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-deploy-backups/sing-box-happ-test-public.20260518-221632.json
sha256=06f03610b797496b9482046d0935bdfbe26ac5fd0724f67943ad1fa2e37c2aeb
size=1132
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-deploy-backups/wg0.conf.20260518-213646
sha256=c7cb617e0bd3a12fd1be1487e7a8c2295c483b94b27d4e0382182ea34af6437e
size=1452
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=8
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/awg2-conf.txt
sha256=aae6505de98e57ff082e5369a6e69a3dba6d9bc6104f5b7da9b286e7247a3777
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Table = off
Address = 10.10.120.8/32
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/egress.registry.before-awg0
sha256=12154352807415f2e7ec535a5812dd3bb7199216b20dfa1e079baa1741509d79
size=308
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/karing-wg-profile.txt
sha256=0cf4292d79c9a5feb518deda46a76e9204ecc534e854aef6e38e6ac42797b29b
size=2066
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/pasha-vless-profile.txt
sha256=7166d45609ab9cce609627231c8bc988492bc0adf35561846cad86a8afef0e08
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/runtime-vless.txt
sha256=8f2ead834d536f63d4d5496432f0a95443d4207a0af4a254c3ffd28810e06dc7
size=1780
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/wg-dump.txt
sha256=a5921f6b1fa2565c457daddc3272138e376b50fcd3844eaa4b544e8327e1f14f
size=1107
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/wg-show.txt
sha256=3bfa2996a4ca7b32666c6fc18335bb73037fac386e060a9375bcfe25f6edc2c2
size=1467
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-fix-all-routes/wg0-conf.txt
sha256=0d64f125656991f4417a4ab85e30f500e935c44223a5ff2b43f571e50f37a680
size=1884
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=14
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = ip route replace 10.7.0.0/22 dev %i scope link
PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostUp = iptables -t nat -A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = ip route del 10.7.0.0/22 dev %i 2>/dev/null || true
PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32
AllowedIPs = 10.0.0.3/32
AllowedIPs = 10.0.0.6/32
AllowedIPs = 10.7.0.3/32
AllowedIPs = 10.7.0.2/32
AllowedIPs = 10.7.0.4/32
AllowedIPs = 10.7.0.5/32

### candidate=/root/v7-diagnostics/2026-05-19-route-matrix/runtime-sing-box.json
sha256=8f2ead834d536f63d4d5496432f0a95443d4207a0af4a254c3ffd28810e06dc7
size=1780
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-route-matrix/service-preferences.before.json
sha256=066a1311abfb14ae331bb20a404dfc40ea1dc12b956fbec4e308e46060b8c8bf
size=267
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-route-matrix/status-vless.service.txt
sha256=06805197c6aee96b496902702168def37d1d8d536e9ba703a81ae01a357939d1
size=3039
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-diagnostics/2026-05-19-route-matrix/wg-show.txt
sha256=673daf66ebe8df31c8f9fa21e0244c5582e934d903c7d887708b1a6812839fda
size=1477
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-dynamic-load-backup-20260518-150622/policy.json
sha256=bf1498f0ab48323e05d3c6ebd04aac5059c630269030dcaf6a2a0555babad8bf
size=504
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-e84-systemd-split-20260525T123450Z/backups/v7-health.service.d.before/10-routing-order.conf
sha256=a01d998f75c5f29ca7adc173bbb40ccb40263b561b726f4912a044f73c8dd085
size=67
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-e84-systemd-split-20260525T123450Z/v7-health.service.d/10-routing-order.conf
sha256=29addaba02918f2044a98bf3b78c62f662f8ed3b19905baf6cc8e5c9c7eb6504
size=37
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-identity-sync-happ-test-20260509-135604/bindings/user-10.0.0.2.json
sha256=ac5cad422d8b59d5abaf81deec01deaaf061a76cdef605cce1af861f8608eb5b
size=778
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/bindings/user-10.0.0.2.json
sha256=c2d06c505c903f6782b235c87e80107b35a119eaf64b71b8bc33be54de7b3127
size=704
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/metadata.json
sha256=a1a0ff68d692a6e2abb7b66e64fa86ada04eee1b147408e0875dc77881d4fe44
size=647
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-131509/sing-box.json
sha256=7c55156cc4cb66f9a1969cc59cb7b5025d9bcd8f8bbfa8886b6cd99ec45ff367
size=465
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.2.json
sha256=f35e3dfa805d9b377aa651b536f4cdf731bb142fbda07c5c81f9856ccb107a4b
size=773
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.3.json
sha256=5344806398106dd2624465f548c9ed5e5bc540dba41bb97defd64d1a35a36d4a
size=778
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/bindings/user-10.0.0.6.json
sha256=01312f4cbb4fb16965e9a3a40ee606a8b4a69642c1911664ca3d44051c748000
size=778
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/metadata.json
sha256=ee1263f2f52c44b9a2fa4221ce71fbc3eccfd6733927c51a965f39b4cbed998e
size=771
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-165726/sing-box.json
sha256=43bbef113ef95e4758419a2bba40e091cdd194abeb1a6837133b6538aecb0263
size=463
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.2.json
sha256=5fe88596ba26e1c3c4e1bf51941e5acf356c484a63231974886c91c61001b34e
size=848
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.3.json
sha256=e7896f8dffa9f5f9e2078b8fa0d97e0012b669ce74658747de429f30cc4cd24b
size=852
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/bindings/user-10.0.0.6.json
sha256=d7882dcf782a87c20d1a005cd23b913b663f8d06e4de39a6873c6a0339485250
size=852
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/metadata.json
sha256=1a5dda1afbbaa0b40691339a0e5bac525bd3af619e96e8fdba129a11bb55e236
size=771
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-inbound-render-happ-test-20260509-171253/sing-box.json
sha256=df40ba38f03643b5cafe7842772b4a09f1eaf94b5aca88cca36b2903e3ab5006
size=695
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-112252/sing-box.json.before
sha256=3c09d24455a4445e59c1379c291ba6239b738a457ae4cbb5d11f3c078f514349
size=693
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-112611/sing-box.json.before
sha256=1153a11eb7bdd4f38378d489325c6319fbcb938cbd915f712aacf17de01fc170
size=807
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-130912/sing-box.json.before
sha256=1153a11eb7bdd4f38378d489325c6319fbcb938cbd915f712aacf17de01fc170
size=807
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-134634/sing-box.json.before
sha256=1d5f46f75fa4afe8ec5fc4ff0b4351fb9a512945dba9699a8ae41b971cae5e1a
size=775
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-135815/sing-box.json.before
sha256=c17ea74e1ffcbeafca5a1f6e1e83d1a0b24aa1dbc5679202ef9d298f7318fa22
size=666
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-candidate-happ-test-20260509-141254/sing-box.json.before
sha256=06f03610b797496b9482046d0935bdfbe26ac5fd0724f67943ad1fa2e37c2aeb
size=1132
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131030/sing-box.json.before
sha256=1d5f46f75fa4afe8ec5fc4ff0b4351fb9a512945dba9699a8ae41b971cae5e1a
size=775
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131211/sing-box.json.before
sha256=1d5f46f75fa4afe8ec5fc4ff0b4351fb9a512945dba9699a8ae41b971cae5e1a
size=775
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-131345/sing-box.json.before
sha256=1d5f46f75fa4afe8ec5fc4ff0b4351fb9a512945dba9699a8ae41b971cae5e1a
size=775
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-134806/sing-box.json.before
sha256=c17ea74e1ffcbeafca5a1f6e1e83d1a0b24aa1dbc5679202ef9d298f7318fa22
size=666
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-140332/sing-box.json.before
sha256=06f03610b797496b9482046d0935bdfbe26ac5fd0724f67943ad1fa2e37c2aeb
size=1132
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-install-backups/proxy-public-enable-happ-test-20260509-141307/sing-box.json.before
sha256=06f03610b797496b9482046d0935bdfbe26ac5fd0724f67943ad1fa2e37c2aeb
size=1132
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-journald-limits.conf
sha256=2dd33e14b0a1da8bcd532fd7d71104ff31f10e2476e32f000b378c5bba08d330
size=69
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-migration-extract/etc/amnezia/amneziawg/awg0.conf
sha256=780e0f3609d790684f68af9f91db6f0eee359391ac65c5db456b8fee836171bd
size=420
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=b89a5f0aa892457a9ffc47fa76e2338d188090b92df54235f158c3d1126505f0
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.1.10/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Table = off
Address = 10.8.1.10/32
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/root/v7-migration-extract/etc/amnezia/amneziawg/awg2.conf
sha256=aae6505de98e57ff082e5369a6e69a3dba6d9bc6104f5b7da9b286e7247a3777
size=587
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=9ba2be63834e48aacdcfe6d61149b5d2720932ac185ead855751d7b4985d833c
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.120.8/32
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=1
redacted_core_fields:
Table = off
Address = 10.10.120.8/32
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/root/v7-migration-extract/etc/amneziawg/awg0.conf
sha256=0267b9842bc1e0216c58fcd3bc2295b081b668f65ab51b7d6d81729c56ab47d4
size=456
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=b89a5f0aa892457a9ffc47fa76e2338d188090b92df54235f158c3d1126505f0
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.8.1.10/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.8.1.10/32
DNS = 1.1.1.1, 1.0.0.1
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25

### candidate=/root/v7-migration-extract/etc/sing-box/config.json
sha256=f06bc772fa716a34fe3fcb4059ffa4c3fc6459baab57cc67b27eb90e3f5f6e99
size=1259
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-migration-extract/etc/wireguard/vps.conf
sha256=dbc463e711667f2d8d6ed87f191f4b2c17bb5d2eada29e6f363bf6a28de3d3aa
size=238
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=0fd7d1aeb7daa3a96765cba18ac0e87419408dbea3b5e84fd7593c841f99b962
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_is_self=false
address=10.10.0.2/24
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.10.0.2/24
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-migration-extract/etc/wireguard/wg0.conf
sha256=693d11a9966026aed32a68e50ea268196047232b152e9a8786419791cb8d5965
size=416
protocol=wireguard
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=10.0.0.1/24
hooks_present=4
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o enp0s1 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o enp0s1 -j MASQUERADE
PostUp = sysctl -w net.ipv4.ip_forward=1
PostDown = sysctl -w net.ipv4.ip_forward=0
AllowedIPs = 10.0.0.2/32

### candidate=/root/v7-phase24-admin-roles-backup-20260507-002627/auth.json
sha256=6c99f0841bf253bfbb54d4bbe6537d0a32e828034669e4705fd3ae3e8999b908
size=418
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-phase25-admin-accounts-backup-20260507-004218/auth.json
sha256=6c99f0841bf253bfbb54d4bbe6537d0a32e828034669e4705fd3ae3e8999b908
size=418
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-040cad24-iphone/karing-auto_travel.json
sha256=933f9261464398c285076c887da83457f0270b80c65eeda4600039d61f75b5b0
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-154c65bb-iphone/karing-auto_travel.json
sha256=396b4f902955c681c5d02b2a8ed31a33a3919f44aea6422c1d01f0ff895f329d
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-19d80844-iphone/karing-auto_travel.json
sha256=b9b0b520dcb7a703313c87b58861fa56ef8998a371e615bcf752f5ddd2c43d36
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-3a12a3c5-iphone/karing-auto_travel.json
sha256=36831c5bd22ab586e486d621295341a93250aa7e0d20fcdd1c230c21d588151c
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-5a74c0a3-iphone/karing-auto_travel.json
sha256=d625c4507c3f92d0456176438fc64b7f3d13adac6484400038a8158b49678a20
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-65977141-iphone/karing-auto_travel.json
sha256=233dcea55b751c9a6e25a64a4b2b284242f39f975e5a7805662d739fd071ce90
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/quick-7330cdec-iphone/karing-auto_travel.json
sha256=31249da06fd5ee3b64e99045499b62d10150cd20b232a6609c57630ebd6637dd
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u000513-iphone-83aab2/karing-auto_travel.json
sha256=09eb2e868622d172fc66b3f8ffc71acd9f76d1a8fd2c41113ddaef77b64b68f2
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u001357-phone-2abf80/karing-auto_travel.json
sha256=7c134b427ab41c14e4c1ff2d38101cf6b98bf7d506285f87ed3830848e319562
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u001357-phone-7addd9/karing-auto_travel.json
sha256=6a12a5a5c02f2815bdb53d699582674937f21da32a1ab839589b5c8d218ece6f
size=1962
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u001357-phone-9a5a0c/karing-auto_travel.json
sha256=af52c95bf3a190849dbe1ba459c5167c1cce1d5c5b030f6faefc29c3cfd41bff
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u001357-phone-bd0f69/karing-auto_travel.json
sha256=a71a2a292e409776e4d1eab814dd9a2dc62e3a99e4e9f04df41bb55fbea7558e
size=1962
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u001859-laptop-0ffdb7/karing-auto_travel.json
sha256=33cb3440f8ae0acb55310541e76c39fe099bd89d912d246000d70806f2a3182a
size=1964
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u002853-laptop-e5d569/karing-auto_travel.json
sha256=71b448267323b2b31cf311a49114fbae0c368c9e8bcdeb0a84234f03f22c71bb
size=1964
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u003833-laptop-5d7eb2/karing-auto_travel.json
sha256=33bfdb8924b8b8febbd38e6cee94b5e622b1910797fa1b112b8a80db18c1fe0a
size=1964
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u234567-iphone-dabe50/karing-ru_local.json
sha256=c5f9e13db7c6dfe15ee718ff7d5f0fdd21ab8e939c4d3a368243729bcb3fc583
size=1647
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-613cf0/karing_wg-ru_local.yaml
sha256=5cd2a743ffb4c2ec670e886190c3b226cc9ecfed5b6b58c1861739aef2e990d4
size=793
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-613cf0/karing_wg-ru_local.yaml.meta
sha256=409f862dbcd2aff8207630eea3da9bc8a04b887ea9a8142a19ac17e29af81332
size=513
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-98f10b/karing_wg-ru_local.yaml
sha256=8f16a0d2a32fc1156b98350d7e15986f3db4869dadc55f5db1b723f0a051bc10
size=1010
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=3
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-98f10b/karing_wg-ru_local.yaml.meta
sha256=b4e3eccfef65b60ac11f80b87adfba8eac74ff284e8c159a811fae8253d2c39a
size=513
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-a12c00/karing-ru_local.json
sha256=85847e2cfe6baae3770a5757b5cf976feb5d71658093c8fc662f828dddaabcc9
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-a9e43d/karing-auto_travel.json
sha256=4ecefa506f03e842fd04efb4ddc7a119ef174eeaa229271b84e0f78a94fdfd19
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-awg0-smux-test/karing-ru_local.json
sha256=1a90c8ff22f3fc37eed73fa5ce567e264d377d5a3b69d3788ec780446c400c8b
size=1738
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-awg2-smux-test/karing-ru_local.json
sha256=27d340150118fe5fa166a16368f863ba02d0ce0798480c2664f3ec23fbaf3f08
size=1878
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b0317e/karing_wg-ru_local.yaml
sha256=e10f8ba0302bf472cf4188cc4cc50b582c5d38648d175816181d59743ad2adb5
size=793
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b0317e/karing_wg-ru_local.yaml.meta
sha256=223c454f275c4ff69997e7253ef5b9e6adf9ccce1feb939cb24df4ac3c8fd8df
size=513
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d-mux-test/karing-ru_local.json
sha256=838bd1045bad7e8f3b88939ff83ef354595ba50caf6b6ac2c424d73d8cd25ed9
size=1922
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d/karing-ru_local.json
sha256=7166d45609ab9cce609627231c8bc988492bc0adf35561846cad86a8afef0e08
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.json
sha256=31213be3746721beff06de11cb178732eb868af3db8cb21209c95251bdab2a03
size=2277
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.json.meta
sha256=7db284085bfffd2520cee1e4fcd7096191af68e086f789706cd70bd948b5c28e
size=532
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.yaml
sha256=352164442c080381816516b50ed8e847ca89b0903bec3ee122a7cca6ab079c06
size=792
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-b2a87d/karing_wg-ru_local.yaml.meta
sha256=d5cf11418effaceaeeb469f29e2ae26ea154f2dacd4ce1b10d9439d53eb3c818
size=513
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-cf7147/karing_wg-ru_local.json
sha256=b5eeb873bf16d9c2988180b9f3c979d69a1a0809ad38395236a62c684c6955fc
size=2144
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-cf7147/karing_wg-ru_local.json.meta
sha256=c146eddf5f1d84f406ba93790c9426d51d751453441f4b0620c68fdefae83790
size=543
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-iphone-wg-endpoint/karing-ru_local.json
sha256=41a06307938223dcdec2df4707bede55fba869edd5722eefd882118b386d6769
size=2003
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-laptop-2e8c0c/karing-auto_travel.json
sha256=e84484ccd16ce588304d69da08b9f8189399bffdaab681be35b3e1199d9ca1fd
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u497791-laptop-7ca2f7/karing-auto_travel.json
sha256=e3ba7ca9283a6c91afa25d5725ad42d0f7a3e1e62b151e41c45f963d2521321e
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u500069-iphone-4e45ec/karing-ru_local.json
sha256=038b2309b09a5597a687ce5e07ba602b261d7d109f7aef1096ea2c9d8c299351
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u597791-iphone-562fe0/karing-auto_travel.json
sha256=33de9e5877150fd500318bbf3dff9626dfdb0d6e9778dcf0da87f81db985cd49
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u597791-iphone-fa9458/karing-auto_travel.json
sha256=ee3136850855617d460278618a0cd38d5d6fc9869c85eeea3623e53534c89501
size=1963
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u614825-iphone-b1c407/karing-ru_local.json
sha256=decea7639afce286acc0db594c7d6c51fb62d9f665fe79a4bb3839b59e454848
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u721171-android-ca87f8/karing-ru_local.json
sha256=7ed1638bc9fa29d16a90c3b15383ec5046974bf3584ba91a71980901136f70b2
size=1919
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u721171-android-e4ad8e/hiddify-ru_local.json
sha256=29dba89a219735f655657b1297f233f0486ef94572ca204007d085f1cf01c651
size=1979
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/u741661-iphone-b000a5/karing-ru_local.json
sha256=2ce361f7a22154b0ab5bacec3d304e87a8fa4ee15b356d17d04dfa85bc1ad450
size=1915
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-iphone/karing-abroad_ru_via_v7.json
sha256=99a28912faebfc671a42c970647f1c51b0a751ecf13e4924524b013e2e3788dd
size=1739
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-iphone/karing-auto_travel.json
sha256=a1e547c8582fb084c36010f9684de53d8f7c6d90811a822dc8a04a12f92e6f37
size=1951
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-iphone/karing-ru_local.json
sha256=06120a3363d86ab1e28577da60f096d12b096364e29895fa464c70aec92846de
size=1635
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-lab-speed/karing-ru_local.json
sha256=e7c1f14470b15f09943252c7fbfd93235a45cb5b2417b52cff932173ac548ee1
size=1879
protocol=vless_or_json
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-lab-speed/karing_wg-ru_local.yaml
sha256=a74770fcc5a96846cc042f981b59a1d3022c4a4bcdf7d9c62e20938a164becfd
size=793
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-smart-clients/v7-lab-speed/karing_wg-ru_local.yaml.meta
sha256=4744c24a7b3a18978e4d57820999e9ccba160a18b6a042a03b05285e750c5998
size=486
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
sha256=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1
size=321
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.89.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.png
sha256=bc41aa75e6e309a2bc7780cabbf72bc22ee0741ab9076a0a2c7f5dd617c9f29f
size=1132
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:

### candidate=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf
sha256=7df64e1dcf3adab44bc92d08e1f89256f48344e31045c6fb330619297be8dc3c
size=249
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.89.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

### candidate=/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf
sha256=45f742717428217c8e3d55a9ba020f6546a0db34770026043b55605456be9445
size=343
protocol=wireguard
endpoint_present=true
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7
endpoint_route_summary=local <ip> dev lo table local src <ip> uid 0 
endpoint_is_self=true
address=10.89.0.2/32, fd89:89::2/128
hooks_present=0
dns_side_effect_present=1
full_tunnel_semantics=1
table_off_present=0
redacted_core_fields:
Address = 10.89.0.2/32, fd89:89::2/128
DNS = 1.1.1.1
MTU = 1200
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

### candidate=/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.png
sha256=ac909c8a7564207b0cc4c5b5f0c6efcc68203c4fd63bb5cf8116303de0df3730
size=1258
protocol=unknown
endpoint_present=false
endpoint_host_sha256=NONE
endpoint_route_summary=
endpoint_is_self=unknown
address=NONE
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=0
table_off_present=0
redacted_core_fields:


## existing_interface_peer_status
$ wg show all endpoints
wg0	Oc9ECXADrmq1TuwK8SuQ7GHKMZqJ+8woxAfiQsqudmY=	109.252.176.232:2357
wg0	Ec0pY6QYlQVZSL0Tn3djy6t1mqTJw2EJDVCd+AKNzmQ=	31.173.87.131:6589
wg0	+SLwwhZrpGjlJFjG9jbxvyk2ecVaVFDC8ihfgkvZjVQ=	(none)
wg0	W9q3F62RP7L8x+kgZDVjO2j8fEPKifXgmZjpMhtvMl0=	(none)
wg0	YY4NbergrYyanEhD8UOc4NcDTap9X3y93msa5xz2Vmk=	(none)
wg0	4dvWrzIoUzwTeWOve4WfcVo477lDt3mCGSn45tH24xg=	(none)
wg0	4Iv3TqnTiVliapzX+alw/olS7mju8ojhEyvijNcE3wA=	(none)
wg0	3oVO7RkRQrmUZZ7o7+V8OSJO0RE4ObwwSruFL6oKuTI=	(none)
wg0	iGlyKHlap8uQs+VZ0eGElvC5TnU+zRR+B+dJlaTJHWM=	(none)
wg0	gStlgxSMk3PZQG+25MKJvDW+up1f39h6iOUvS30CiBQ=	(none)
wg0	XUFA7GRkXXdWl7juuuznm3wAXQx9RuOLn4O2Kd6cCmM=	(none)
wg0	rTDkqkpPvfVfTLvGYPP7WWdhEkB9c79b2LJSPT4Cc2g=	(none)
wg0	P/GpQj9qVrKulh6gUX2Y+4BZKzrLr9pvlGSNxFsFQ34=	(none)
wg0	PTjnlK95nMK8nS8Iocucl1voY2RypMajqVCzkJP9jSo=	178.176.73.117:24028
wg0	leEcfiODElYb4zJ3DLPpn4tQObfnBiU4VYGJ3CueQGY=	109.252.176.232:1108
wg0	M0nlK5PSBlwZtNRUWuBsnKKQUt9987RGA3dul6PNrgI=	(none)
v7e06a394c478	VdM0jVhWfgGV0PQwNm137orOY/51lDXg/sVwdcV+TSg=	89.191.226.228:51820
$ wg show all latest-handshakes
wg0	Oc9ECXADrmq1TuwK8SuQ7GHKMZqJ+8woxAfiQsqudmY=	1778075618
wg0	Ec0pY6QYlQVZSL0Tn3djy6t1mqTJw2EJDVCd+AKNzmQ=	1779314786
wg0	+SLwwhZrpGjlJFjG9jbxvyk2ecVaVFDC8ihfgkvZjVQ=	0
wg0	W9q3F62RP7L8x+kgZDVjO2j8fEPKifXgmZjpMhtvMl0=	0
wg0	YY4NbergrYyanEhD8UOc4NcDTap9X3y93msa5xz2Vmk=	0
wg0	4dvWrzIoUzwTeWOve4WfcVo477lDt3mCGSn45tH24xg=	0
wg0	4Iv3TqnTiVliapzX+alw/olS7mju8ojhEyvijNcE3wA=	0
wg0	3oVO7RkRQrmUZZ7o7+V8OSJO0RE4ObwwSruFL6oKuTI=	0
wg0	iGlyKHlap8uQs+VZ0eGElvC5TnU+zRR+B+dJlaTJHWM=	0
wg0	gStlgxSMk3PZQG+25MKJvDW+up1f39h6iOUvS30CiBQ=	0
wg0	XUFA7GRkXXdWl7juuuznm3wAXQx9RuOLn4O2Kd6cCmM=	0
wg0	rTDkqkpPvfVfTLvGYPP7WWdhEkB9c79b2LJSPT4Cc2g=	0
wg0	P/GpQj9qVrKulh6gUX2Y+4BZKzrLr9pvlGSNxFsFQ34=	0
wg0	PTjnlK95nMK8nS8Iocucl1voY2RypMajqVCzkJP9jSo=	1779467131
wg0	leEcfiODElYb4zJ3DLPpn4tQObfnBiU4VYGJ3CueQGY=	1779458120
wg0	M0nlK5PSBlwZtNRUWuBsnKKQUt9987RGA3dul6PNrgI=	0
v7e06a394c478	VdM0jVhWfgGV0PQwNm137orOY/51lDXg/sVwdcV+TSg=	1779972006
$ wg show all transfer
wg0	Oc9ECXADrmq1TuwK8SuQ7GHKMZqJ+8woxAfiQsqudmY=	79732	1260
wg0	Ec0pY6QYlQVZSL0Tn3djy6t1mqTJw2EJDVCd+AKNzmQ=	4053483656	24334590692
wg0	+SLwwhZrpGjlJFjG9jbxvyk2ecVaVFDC8ihfgkvZjVQ=	0	0
wg0	W9q3F62RP7L8x+kgZDVjO2j8fEPKifXgmZjpMhtvMl0=	0	0
wg0	YY4NbergrYyanEhD8UOc4NcDTap9X3y93msa5xz2Vmk=	0	0
wg0	4dvWrzIoUzwTeWOve4WfcVo477lDt3mCGSn45tH24xg=	0	0
wg0	4Iv3TqnTiVliapzX+alw/olS7mju8ojhEyvijNcE3wA=	0	0
wg0	3oVO7RkRQrmUZZ7o7+V8OSJO0RE4ObwwSruFL6oKuTI=	0	0
wg0	iGlyKHlap8uQs+VZ0eGElvC5TnU+zRR+B+dJlaTJHWM=	0	0
wg0	gStlgxSMk3PZQG+25MKJvDW+up1f39h6iOUvS30CiBQ=	0	0
wg0	XUFA7GRkXXdWl7juuuznm3wAXQx9RuOLn4O2Kd6cCmM=	0	0
wg0	rTDkqkpPvfVfTLvGYPP7WWdhEkB9c79b2LJSPT4Cc2g=	0	0
wg0	P/GpQj9qVrKulh6gUX2Y+4BZKzrLr9pvlGSNxFsFQ34=	0	0
wg0	PTjnlK95nMK8nS8Iocucl1voY2RypMajqVCzkJP9jSo=	3753236	21312888
wg0	leEcfiODElYb4zJ3DLPpn4tQObfnBiU4VYGJ3CueQGY=	60444316	1648615384
wg0	M0nlK5PSBlwZtNRUWuBsnKKQUt9987RGA3dul6PNrgI=	0	0
v7e06a394c478	VdM0jVhWfgGV0PQwNm137orOY/51lDXg/sVwdcV+TSg=	10477203760	413489228

## runtime_checkers
v7-reconcile-check rc=0
===== V7 RECONCILE CHECK =====
2026-05-28T15:41:23+03:00
state_dir=/opt/v7/egress/state
users_registry=/opt/v7/egress/state/users.registry
egress_registry=/opt/v7/egress/state/egress.registry
wg_if=wg0

===== USERS =====
user=10.0.0.2 enabled=1 current=awg3 table=100
user=10.0.0.3 enabled=1 current=awg3 table=101
user=10.0.0.6 enabled=1 current=awg3 table=104
user=10.7.0.3 enabled=1 current=awg3 table=1001
user=10.7.0.2 enabled=1 current=awg3 table=1000
user=10.7.0.4 enabled=1 current=awg3 table=1002
user=10.7.0.5 enabled=1 current=awg3 table=1003
user=10.7.0.6 enabled=1 current=awg3 table=1004
user=10.7.0.7 enabled=0 current=vless table=1005
user=10.7.0.8 enabled=1 current=awg3 table=1006
user=10.7.0.9 enabled=1 current=awg0 table=1007
user=10.7.0.10 enabled=1 current=awg0 table=1008
user=10.7.0.11 enabled=1 current=1 table=1009
user=10.7.0.12 enabled=1 current=1 table=1010
user=10.7.0.13 enabled=1 current=awg0 table=1011
user=10.7.0.14 enabled=1 current=1 table=1012
user=10.7.0.15 enabled=1 current=1 table=1013

===== RESULT =====
warnings=0
errors=0
V7_RECONCILE_RESULT=OK
v7-user-route-check rc=0
route_get=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0 
OK: user=10.7.0.12 route_get uses v7e356a192b79

USER=10.7.0.13 TABLE=1011 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.13 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.13 table=1011 default dev awg0
route_get=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0 
OK: user=10.7.0.13 route_get uses awg0

USER=10.7.0.14 TABLE=1012 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.14 registry matches assignment
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.14 table=1012 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0 
OK: user=10.7.0.14 route_get uses v7e356a192b79

USER=10.7.0.15 TABLE=1013 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.15 registry matches assignment
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 table=1013 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0 
OK: user=10.7.0.15 route_get uses v7e356a192b79

===== RESULT =====
V7_USER_ROUTE_CHECK=OK
v7-killswitch-check rc=0
user=10.7.0.6 table=1004 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.6 route_get uses expected egress
user=10.7.0.8 table=1006 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.8 route_get uses expected egress
user=10.7.0.9 table=1007 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.9 route_get uses expected egress
user=10.7.0.10 table=1008 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.10 route_get uses expected egress
user=10.7.0.11 table=1009 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.11 route_get uses expected egress
user=10.7.0.12 table=1010 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.12 route_get uses expected egress
user=10.7.0.13 table=1011 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.13 route_get uses expected egress
user=10.7.0.14 table=1012 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.14 route_get uses expected egress
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 route_get uses expected egress

===== RESULT =====
V7_KILLSWITCH_CHECK=OK
v7-provisioning-reconcile-check rc=0
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.3 table=1001 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.2 table=1000 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.2 dev awg3 table 1000 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.4 table=1002 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.4 dev awg3 table 1002 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.5 table=1003 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.5 dev awg3 table 1003 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.6 table=1004 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.8 table=1006 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.9 table=1007 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.10 table=1008 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.11 table=1009 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.12 table=1010 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.13 table=1011 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.14 table=1012 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 

===== RESULT =====
V7_PROVISIONING_RECONCILE_CHECK=OK
