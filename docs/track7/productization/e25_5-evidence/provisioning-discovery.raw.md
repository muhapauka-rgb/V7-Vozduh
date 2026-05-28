# identity
v3119922.hosted-by-vdsina.ru
Thu May 28 11:47:54 UTC 2026
# registry-hashes
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
# egress-registry
id=vless protocol=vless type=proxy interface=tun0 test=socks5://127.0.0.1:1080 enabled=1 expected_ip=77.110.103.131 config_path=/etc/sing-box/config.json
id=awg0 protocol=amneziawg type=interface interface=awg0 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg0.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=60 weight=70 connect_timeout=12s
id=awg3 protocol=amneziawg type=interface interface=awg3 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg3.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=70 weight=75 connect_timeout=12s
id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=openvpn-1779388847-d2ad7c protocol=openvpn type=interface interface=v7edb0c189291 test=interface enabled=1 config=/etc/v7/egress-openvpn/v7edb0c189291.ovpn role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
# wireguard-configs
total 312
drwx------   2 root root  4096 May 23 14:55 .
drwxr-xr-x 124 root root 12288 May 21 18:16 ..
-rw-------   1 root root   315 May 22 16:16 v7e06a394c478.conf
-rw-------   1 root root   315 May 22 16:16 v7e06a394c478.conf.backup.v7-existing-update.20260522-132115
-rw-rw-r--   1 1000 1000   238 Apr 24 15:38 vps.conf
-rw-------   1 root root   697 May 19 11:26 wg-client-test.conf
-rw-------   1 root root  2963 May 23 14:55 wg0.conf
-rw-r--r--   1 root root   416 Apr 29 17:50 wg0.conf.backup.20260506-163303
-rw-r--r--   1 root root   412 May  6 16:33 wg0.conf.backup.iphone.20260506-164945
-rw-r--r--   1 root root   523 May  6 16:49 wg0.conf.backup.nat-egress.20260506-165513
-rw-r--r--   1 root root   835 May  6 16:55 wg0.conf.backup.v7-user-create.20260506-171016
-rw-r--r--   1 root root   835 May  6 16:55 wg0.conf.backup.v7-user-create.20260506-195020
-rw-------   1 root root   836 May  6 19:51 wg0.conf.backup.v7-user-create.20260508-161819
-rw-------   1 root root   959 May  8 16:18 wg0.conf.backup.v7-user-create.20260508-161923
-rw-------   1 root root   837 May  8 16:26 wg0.conf.backup.v7-user-create.20260508-162703
-rw-------   1 root root   960 May  8 16:27 wg0.conf.backup.v7-user-create.20260509-095148
-rw-------   1 root root   961 May  9 09:51 wg0.conf.backup.v7-user-create.20260512-223215
-rw-------   1 root root  1084 May 12 22:32 wg0.conf.backup.v7-user-create.20260512-223355
-rw-------   1 root root  1207 May 12 22:33 wg0.conf.backup.v7-user-create.20260512-225923
-rw-------   1 root root  1330 May 12 22:59 wg0.conf.backup.v7-user-create.20260512-225941
-rw-------   1 root root  1453 May 12 22:59 wg0.conf.backup.v7-user-create.20260513-162145
-rw-------   1 root root  1576 May 13 16:21 wg0.conf.backup.v7-user-create.20260513-164331
-rw-------   1 root root  1543 May 13 16:49 wg0.conf.backup.v7-user-create.20260513-172826
-rw-------   1 root root  1666 May 13 17:28 wg0.conf.backup.v7-user-create.20260513-215434
-rw-------   1 root root  1790 May 13 21:54 wg0.conf.backup.v7-user-create.20260513-215821
-rw-------   1 root root  1791 May 13 22:11 wg0.conf.backup.v7-user-create.20260514-001900
-rw-------   1 root root  1916 May 14 00:19 wg0.conf.backup.v7-user-create.20260514-002854
-rw-------   1 root root  1792 May 14 00:33 wg0.conf.backup.v7-user-create.20260514-003507
-rw-------   1 root root  1793 May 14 00:35 wg0.conf.backup.v7-user-create.20260514-003834
-rw-------   1 root root  1794 May 14 00:40 wg0.conf.backup.v7-user-create.20260514-004008
-rw-------   1 root root  1795 May 14 00:46 wg0.conf.backup.v7-user-create.20260514-004618
-rw-------   1 root root  1796 May 14 00:46 wg0.conf.backup.v7-user-create.20260514-004748
-rw-------   1 root root  1797 May 14 12:34 wg0.conf.backup.v7-user-create.20260514-212852
-rw-------   1 root root  1920 May 14 21:28 wg0.conf.backup.v7-user-create.20260515-073929
-rw-------   1 root root  2043 May 15 07:39 wg0.conf.backup.v7-user-create.20260515-074517
-rw-------   1 root root  1085 May 17 16:32 wg0.conf.backup.v7-user-create.20260517-174520
-rw-------   1 root root  1207 May 17 17:45 wg0.conf.backup.v7-user-create.20260517-174942
-rw-------   1 root root  1329 May 17 17:49 wg0.conf.backup.v7-user-create.20260518-143340
-rw-------   1 root root  1762 May 20 23:10 wg0.conf.backup.v7-user-create.20260520-231105
-rw-------   1 root root  1885 May 20 23:11 wg0.conf.backup.v7-user-create.20260521-133329
-rw-------   1 root root  2008 May 21 13:33 wg0.conf.backup.v7-user-create.20260521-145816
-rw-------   1 root root  2132 May 21 14:58 wg0.conf.backup.v7-user-create.20260521-145831
-rw-------   1 root root  2256 May 21 14:58 wg0.conf.backup.v7-user-create.20260521-145841
-rw-------   1 root root  2380 May 21 14:58 wg0.conf.backup.v7-user-create.20260522-154617
-rw-------   1 root root  2505 May 22 15:46 wg0.conf.backup.v7-user-create.20260522-160728
-rw-------   1 root root  2630 May 22 16:07 wg0.conf.backup.v7-user-create.20260522-160743
-rw-------   1 root root  2755 May 22 16:07 wg0.conf.backup.v7-user-create.20260522-161435
-rw-------   1 root root  2880 May 22 16:14 wg0.conf.backup.v7-user-create.20260522-162731
-rw-------   1 root root  2838 May 23 14:54 wg0.conf.backup.v7-user-create.20260523-145551
-rw-r--r--   1 root root   955 May  6 19:50 wg0.conf.backup.v7-user-disable.20260506-195117
-rw-------   1 root root   926 May  8 16:26 wg0.conf.backup.v7-user-disable.20260508-162631
-rw-------   1 root root  1081 May  9 09:51 wg0.conf.backup.v7-user-disable.20260509-095150
-rw-------   1 root root  1699 May 13 16:43 wg0.conf.backup.v7-user-disable.20260513-164950
-rw-------   1 root root  1914 May 13 21:58 wg0.conf.backup.v7-user-disable.20260513-221130
-rw-------   1 root root  2041 May 14 00:28 wg0.conf.backup.v7-user-disable.20260514-003316
-rw-------   1 root root  1882 May 14 00:33 wg0.conf.backup.v7-user-disable.20260514-003317
-rw-------   1 root root  1915 May 14 00:35 wg0.conf.backup.v7-user-disable.20260514-003509
-rw-------   1 root root  1918 May 14 00:38 wg0.conf.backup.v7-user-disable.20260514-004007
-rw-------   1 root root  1917 May 14 00:40 wg0.conf.backup.v7-user-disable.20260514-004617
-rw-------   1 root root  1918 May 14 00:46 wg0.conf.backup.v7-user-disable.20260514-004619
-rw-------   1 root root  1919 May 14 00:47 wg0.conf.backup.v7-user-disable.20260514-004749
-rw-------   1 root root  1797 May 14 00:47 wg0.conf.backup.v7-user-disable.20260514-122954
-rw-------   1 root root  1797 May 14 12:29 wg0.conf.backup.v7-user-disable.20260514-123441
-rw-------   1 root root  2166 May 15 07:45 wg0.conf.backup.v7-user-disable.20260517-163115
-rw-------   1 root root  2166 May 17 16:31 wg0.conf.backup.v7-user-disable.20260517-163124
-rw-------   1 root root  2010 May 17 16:31 wg0.conf.backup.v7-user-disable.20260517-163131
-rw-------   1 root root  2010 May 17 16:31 wg0.conf.backup.v7-user-disable.20260517-163140
-rw-------   1 root root  1854 May 17 16:31 wg0.conf.backup.v7-user-disable.20260517-163203
-rw-------   1 root root  1765 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163217
-rw-------   1 root root  1642 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163221
-rw-------   1 root root  1552 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163241
-rw-------   1 root root  1429 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163247
-rw-------   1 root root  1306 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163256
-rw-------   1 root root  1183 May 17 16:32 wg0.conf.backup.v7-user-disable.20260517-163259
-rw-------   1 root root  1884 May 18 21:37 wg0.conf.backup.v7-user-disable.20260520-231014
-rw-------   1 root root  2996 May 22 16:27 wg0.conf.backup.v7-user-disable.20260523-145431
/etc/wireguard/v7e06a394c478.conf
/etc/wireguard/vps.conf
/etc/wireguard/wg-client-test.conf
/etc/wireguard/wg0.conf
# amnezia-configs
/etc/amnezia/amneziawg/awg-client-test.conf
/etc/amnezia/amneziawg/awg0.conf
/etc/amnezia/amneziawg/awg3.conf
/etc/amnezia/amneziawg/v7e19caebd878.conf
/etc/amnezia/amneziawg/v7e356a192b79.conf
/etc/v7/admin/auth.json
/etc/v7/admin/safe-mode.json
/etc/v7/awg-client-test/state.json
/etc/v7/direct/domains.conf
/etc/v7/direct/exclude.conf
/etc/v7/egress-drafts/.deleted/amneziawg-1779212551-5f2af4.20260519-220027/metadata.json
/etc/v7/egress-drafts/.deleted/amneziawg-1779227510-8c08e7.20260520-155023/metadata.json
/etc/v7/egress-drafts/.deleted/codex-openvpn-api-check-1184803-1779377269-5629a6.20260521-152750/metadata.json
/etc/v7/egress-drafts/.deleted/openvpn-1779352711-bc94ec.20260521-084303/metadata.json
/etc/v7/egress-drafts/.deleted/openvpn-1779352726-16e1ec.20260521-084252/metadata.json
/etc/v7/egress-drafts/1-1779291887-55965c/metadata.json
/etc/v7/egress-drafts/amneziawg-1779303737-a57ce8/metadata.json
/etc/v7/egress-drafts/amneziawg-1779305908-ed3889/metadata.json
/etc/v7/egress-drafts/openvpn-1779385423-2121b0/metadata.json
/etc/v7/egress-drafts/openvpn-1779387408-c42bdf/metadata.json
/etc/v7/egress-drafts/openvpn-1779388847-d2ad7c/metadata.json
/etc/v7/egress-drafts/openvpn-1779453676-42885e/metadata.json
/etc/v7/egress-drafts/subscription_url-1779462892-4d2cea/metadata.json
/etc/v7/egress-drafts/test1-1779352953-489ac4/metadata.json
/etc/v7/egress-drafts/wg-1779455931-ba621c/metadata.json
/etc/v7/egress-drafts/wireguard-1779454504-c43409/metadata.json
/etc/v7/egress-openvpn/v7edb0c189291.ovpn
/etc/v7/inbound-runtime/happ-test/bindings/user-10.0.0.2.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.0.0.3.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.0.0.6.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.14.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.15.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.3.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.5.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.6.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.8.json
/etc/v7/inbound-runtime/happ-test/bindings/user-10.7.0.9.json
/etc/v7/inbound-runtime/happ-test/metadata.json
/etc/v7/inbound-runtime/happ-test/public-candidate/metadata.json
/etc/v7/inbound-runtime/happ-test/public-candidate/sing-box.json
/etc/v7/inbound-runtime/happ-test/sing-box.json
/etc/v7/maintenance.conf
/etc/v7/org-egress-policy.json
/etc/v7/policy.json
/etc/v7/policy/direct_ru_domains.conf
/etc/v7/policy/global_fast_domains.conf
/etc/v7/policy/global_stable_domains.conf
/etc/v7/policy/low_latency_domains.conf
/etc/v7/policy/trusted_ru_sensitive_domains.conf
/etc/v7/policy/video_domains.conf
/etc/v7/traffic-accounting.json
# interfaces
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
ens3             UP             52:54:00:2f:9b:32 <BROADCAST,MULTICAST,UP,LOWER_UP> 
wg0              UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
tun0             UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> 
v7e356a192b79    UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
awg0             UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
awg3             UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
v7edb0c189291    UP             <POINTOPOINT,NOARP,UP,LOWER_UP> 
v7e06a394c478    UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
# wg-interfaces
interface: wg0
  public key: a9MNyFSM0anpyXlSo2DEn2Tt0NRhsIdGW3ncGO19ejo=
  private key: (hidden)
  listening port: 51820

peer: PTjnlK95nMK8nS8Iocucl1voY2RypMajqVCzkJP9jSo=
  endpoint: 178.176.73.117:24028
  allowed ips: 10.7.0.13/32
  latest handshake: 5 days, 19 hours, 22 minutes, 23 seconds ago
  transfer: 3.58 MiB received, 20.33 MiB sent

peer: leEcfiODElYb4zJ3DLPpn4tQObfnBiU4VYGJ3CueQGY=
  endpoint: 109.252.176.232:1108
  allowed ips: 10.7.0.14/32
  latest handshake: 5 days, 21 hours, 52 minutes, 34 seconds ago
  transfer: 57.64 MiB received, 1.54 GiB sent

peer: Ec0pY6QYlQVZSL0Tn3djy6t1mqTJw2EJDVCd+AKNzmQ=
  endpoint: 31.173.87.131:6589
  allowed ips: 10.0.0.3/32
  latest handshake: 7 days, 13 hours, 41 minutes, 28 seconds ago
  transfer: 3.78 GiB received, 22.66 GiB sent

peer: Oc9ECXADrmq1TuwK8SuQ7GHKMZqJ+8woxAfiQsqudmY=
  endpoint: 109.252.176.232:2357
  allowed ips: 10.0.0.2/32
  latest handshake: 21 days, 21 hours, 54 minutes, 16 seconds ago
  transfer: 77.86 KiB received, 1.23 KiB sent

peer: +SLwwhZrpGjlJFjG9jbxvyk2ecVaVFDC8ihfgkvZjVQ=
  allowed ips: 10.0.0.6/32

peer: W9q3F62RP7L8x+kgZDVjO2j8fEPKifXgmZjpMhtvMl0=
  allowed ips: 10.7.0.3/32

peer: YY4NbergrYyanEhD8UOc4NcDTap9X3y93msa5xz2Vmk=
  allowed ips: 10.7.0.2/32

peer: 4dvWrzIoUzwTeWOve4WfcVo477lDt3mCGSn45tH24xg=
  allowed ips: 10.7.0.4/32

peer: 4Iv3TqnTiVliapzX+alw/olS7mju8ojhEyvijNcE3wA=
  allowed ips: 10.7.0.5/32

peer: 3oVO7RkRQrmUZZ7o7+V8OSJO0RE4ObwwSruFL6oKuTI=
  allowed ips: 10.7.0.6/32

peer: iGlyKHlap8uQs+VZ0eGElvC5TnU+zRR+B+dJlaTJHWM=
  allowed ips: 10.7.0.8/32

peer: gStlgxSMk3PZQG+25MKJvDW+up1f39h6iOUvS30CiBQ=
  allowed ips: 10.7.0.9/32

peer: XUFA7GRkXXdWl7juuuznm3wAXQx9RuOLn4O2Kd6cCmM=
  allowed ips: 10.7.0.10/32

peer: rTDkqkpPvfVfTLvGYPP7WWdhEkB9c79b2LJSPT4Cc2g=
  allowed ips: 10.7.0.11/32

peer: P/GpQj9qVrKulh6gUX2Y+4BZKzrLr9pvlGSNxFsFQ34=
  allowed ips: 10.7.0.12/32

peer: M0nlK5PSBlwZtNRUWuBsnKKQUt9987RGA3dul6PNrgI=
  allowed ips: 10.7.0.15/32

interface: v7e06a394c478
  public key: 5JvoR9IwONdb9c5Sgz05XZrn4F9XISOwCYjuWYx2bno=
  private key: (hidden)
  listening port: 36540

peer: VdM0jVhWfgGV0PQwNm137orOY/51lDXg/sVwdcV+TSg=
  preshared key: (hidden)
  endpoint: 89.191.226.228:51820
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 50 seconds ago
  transfer: 9.69 GiB received, 391.74 MiB sent
# systemd wg units
  UNIT                 LOAD   ACTIVE   SUB  DESCRIPTION
  wg-quick@wg0.service loaded inactive dead WireGuard via wg-quick(8) for wg0

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

1 loaded units listed.
To show all installed unit files use 'systemctl list-unit-files'.
# selected
ls: cannot access '/opt/v7/egress/state/*selected*': No such file or directory
# hidden
