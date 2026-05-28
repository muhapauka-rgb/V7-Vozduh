# identity
v3119922.hosted-by-vdsina.ru
Thu May 28 11:39:19 UTC 2026
# users.registry hash
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
# egress.registry
id=vless protocol=vless type=proxy interface=tun0 test=socks5://127.0.0.1:1080 enabled=1 expected_ip=77.110.103.131 config_path=/etc/sing-box/config.json
id=awg0 protocol=amneziawg type=interface interface=awg0 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg0.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=60 weight=70 connect_timeout=12s
id=awg3 protocol=amneziawg type=interface interface=awg3 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg3.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=70 weight=75 connect_timeout=12s
id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=openvpn-1779388847-d2ad7c protocol=openvpn type=interface interface=v7edb0c189291 test=interface enabled=1 config=/etc/v7/egress-openvpn/v7edb0c189291.ovpn role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
# users-per-egress
1 4
awg0 3
awg3 9
# readiness
{
  "approval_status": "GO",
  "candidate": {
    "candidate_still_valid": true,
    "current_egress": "1",
    "enabled": true,
    "expected_current_egress": "1",
    "reasons": [],
    "table": "1009",
    "user": "10.7.0.11"
  },
  "candidate_still_valid": true,
  "candidate_user": "10.7.0.11",
  "current_egress": "1",
  "execution_allowed_now": false,
  "forbidden_commands_called": false,
  "mutation": false,
  "quality_floor": {
    "avg_mbps": 15.0,
    "min_mbps": 10.0,
    "stability": 0.45
  },
  "read_only": true,
  "rejected_targets": [
    {
      "egress_id": "vless",
      "reasons": [
        "interface state unknown",
        "load-state users=1",
        "diagnose SUSPECT",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "awg0",
      "reasons": [
        "occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13",
        "load-state users=3",
        "min_mbps below floor (9.16)",
        "stability below floor (0.283127)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "awg3",
      "reasons": [
        "occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8",
        "load-state users=9",
        "min_mbps below floor (2.42)",
        "stability below floor (0.0668957)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "openvpn-1779388847-d2ad7c",
      "reasons": [
        "interface state unknown",
        "diagnose SUSPECT"
      ]
    }
  ],
  "required_excluded_route_classes": [
    "DIRECT_RU",
    "TRUSTED_RU_SENSITIVE"
  ],
  "runtime_commands_executed": false,
  "schema_version": 1,
  "second_canary_readiness": "GO",
  "selected_target": "wireguard-1779454504-c43409",
  "should_e9_3_execute_now": false,
  "state_dir": "/opt/v7/egress/state",
  "target_1_current_user": [
    "10.7.0.11",
    "10.7.0.12",
    "10.7.0.14",
    "10.7.0.15"
  ],
  "target_candidates": [
    {
      "avg_mbps": 49.2527,
      "diagnose_detail": "protocol=vless",
      "diagnose_status": "SUSPECT",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "vless",
      "enabled": true,
      "exclude_route_classes": [],
      "interface": "tun0",
      "interface_up_lower_up": null,
      "load_status": "SOFT_FULL",
      "manual_only": false,
      "min_mbps": 44.21,
      "rejection_reasons": [
        "interface state unknown",
        "load-state users=1",
        "diagnose SUSPECT",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "",
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 49.2527,
        "min_mbps": 44.21,
        "stability": 0.897616
      },
      "stability": 0.897616,
      "status": "NO-GO",
      "users_count_from_load_state": 1,
      "users_count_from_registry": 0,
      "warnings": [
        "load_status=SOFT_FULL"
      ],
      "zero_user": false
    },
    {
      "avg_mbps": 32.353,
      "diagnose_detail": "handshake_age_seconds=98",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "awg0",
      "enabled": true,
      "exclude_route_classes": [],
      "interface": "awg0",
      "interface_up_lower_up": true,
      "load_status": "HARD_FULL",
      "manual_only": false,
      "min_mbps": 9.16,
      "rejection_reasons": [
        "occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13",
        "load-state users=3",
        "min_mbps below floor (9.16)",
        "stability below floor (0.283127)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "GLOBAL_STABLE",
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 32.353,
        "min_mbps": 9.16,
        "stability": 0.283127
      },
      "stability": 0.283127,
      "status": "NO-GO",
      "users_count_from_load_state": 3,
      "users_count_from_registry": 3,
      "warnings": [
        "load_status=HARD_FULL",
        "interface_state_inferred_from_diagnose"
      ],
      "zero_user": false
    },
    {
      "avg_mbps": 36.1757,
      "diagnose_detail": "handshake_age_seconds=43",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "awg3",
      "enabled": true,
      "exclude_route_classes": [],
      "interface": "awg3",
      "interface_up_lower_up": true,
      "load_status": "HARD_FULL",
      "manual_only": false,
      "min_mbps": 2.42,
      "rejection_reasons": [
        "occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8",
        "load-state users=9",
        "min_mbps below floor (2.42)",
        "stability below floor (0.0668957)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "GLOBAL_STABLE",
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 36.1757,
        "min_mbps": 2.42,
        "stability": 0.0668957
      },
      "stability": 0.0668957,
      "status": "NO-GO",
      "users_count_from_load_state": 9,
      "users_count_from_registry": 9,
      "warnings": [
        "load_status=HARD_FULL",
        "interface_state_inferred_from_diagnose"
      ],
      "zero_user": false
    },
    {
      "avg_mbps": 63.678,
      "diagnose_detail": "protocol=openvpn",
      "diagnose_status": "SUSPECT",
      "direct_ru_trusted_ru_risk": "low_excluded",
      "egress_id": "openvpn-1779388847-d2ad7c",
      "enabled": true,
      "exclude_route_classes": [
        "DIRECT_RU",
        "TRUSTED_RU_SENSITIVE"
      ],
      "interface": "v7edb0c189291",
      "interface_up_lower_up": null,
      "load_status": "OK",
      "manual_only": false,
      "min_mbps": 45.94,
      "rejection_reasons": [
        "interface state unknown",
        "diagnose SUSPECT"
      ],
      "reserve_only": false,
      "role": "GLOBAL_FAST",
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 63.678,
        "min_mbps": 45.94,
        "stability": 0.721442
      },
      "stability": 0.721442,
      "status": "NO-GO",
      "users_count_from_load_state": 0,
      "users_count_from_registry": 0,
      "warnings": [],
      "zero_user": true
    },
    {
      "avg_mbps": 23.705,
      "diagnose_detail": "handshake_age_seconds=9",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "low_excluded",
      "egress_id": "wireguard-1779454504-c43409",
      "enabled": true,
      "exclude_route_classes": [
        "DIRECT_RU",
        "TRUSTED_RU_SENSITIVE"
      ],
      "interface": "v7e06a394c478",
      "interface_up_lower_up": true,
      "load_status": "OK",
      "manual_only": false,
      "min_mbps": 20.1,
      "rejection_reasons": [],
      "reserve_only": false,
      "role": "GLOBAL_FAST",
      "safe_for_second_canary": true,
      "score": {
        "avg_mbps": 23.705,
        "min_mbps": 20.1,
        "stability": 0.847922
      },
      "stability": 0.847922,
      "status": "GO",
      "users_count_from_load_state": 0,
      "users_count_from_registry": 0,
      "warnings": [
        "interface_state_inferred_from_diagnose"
      ],
      "zero_user": true
    }
  ],
  "tool": "v7-second-canary-target-readiness",
  "zero_user_targets": [
    "openvpn-1779388847-d2ad7c",
    "wireguard-1779454504-c43409"
  ]
}
# load
updated=2026-05-28T14:39:01+03:00
vless_users=1
vless_soft_limit=1
vless_hard_limit=2
vless_load_status=SOFT_FULL
awg0_users=3
awg0_soft_limit=1
awg0_hard_limit=2
awg0_load_status=HARD_FULL
awg3_users=9
awg3_soft_limit=1
awg3_hard_limit=2
awg3_load_status=HARD_FULL
1_users=4
1_soft_limit=1
1_hard_limit=2
1_load_status=HARD_FULL
openvpn-1779388847-d2ad7c_users=0
openvpn-1779388847-d2ad7c_soft_limit=1
openvpn-1779388847-d2ad7c_hard_limit=2
openvpn-1779388847-d2ad7c_load_status=OK
wireguard-1779454504-c43409_users=0
wireguard-1779454504-c43409_soft_limit=1
wireguard-1779454504-c43409_hard_limit=2
wireguard-1779454504-c43409_load_status=OK
# stability
vless_avg_mbps=49.2527
vless_min_mbps=44.21
vless_stability=0.897616
vless_samples=30
awg0_avg_mbps=32.353
awg0_min_mbps=9.16
awg0_stability=0.283127
awg0_samples=30
awg3_avg_mbps=36.1757
awg3_min_mbps=2.42
awg3_stability=0.0668957
awg3_samples=30
1_avg_mbps=73.118
1_min_mbps=60.40
1_stability=0.826062
1_samples=30
openvpn-1779388847-d2ad7c_avg_mbps=63.678
openvpn-1779388847-d2ad7c_min_mbps=45.94
openvpn-1779388847-d2ad7c_stability=0.721442
openvpn-1779388847-d2ad7c_samples=30
wireguard-1779454504-c43409_avg_mbps=23.705
wireguard-1779454504-c43409_min_mbps=20.10
wireguard-1779454504-c43409_stability=0.847922
wireguard-1779454504-c43409_samples=30
# diagnose
updated=2026-05-28T11:39:01Z
vless_diagnose_reason=handshake_unsupported_for_protocol_vless
vless_diagnose_severity=SUSPECT
vless_diagnose_detail=protocol=vless
awg0_diagnose_reason=OK
awg0_diagnose_severity=OK
awg0_diagnose_detail=handshake_age_seconds=98
awg3_diagnose_reason=OK
awg3_diagnose_severity=OK
awg3_diagnose_detail=handshake_age_seconds=43
1_diagnose_reason=OK
1_diagnose_severity=OK
1_diagnose_detail=handshake_age_seconds=94
openvpn-1779388847-d2ad7c_diagnose_reason=handshake_unsupported_for_protocol_openvpn
openvpn-1779388847-d2ad7c_diagnose_severity=SUSPECT
openvpn-1779388847-d2ad7c_diagnose_detail=protocol=openvpn
wireguard-1779454504-c43409_diagnose_reason=OK
wireguard-1779454504-c43409_diagnose_severity=OK
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=9
# selected
ls: cannot access '/opt/v7/egress/state/*selected*': No such file or directory
# barriers
ls: cannot access '/opt/v7/egress/state/*generation*': No such file or directory
-rw-r--r-- 1 root root 598 May 27 16:13 /opt/v7/egress/state/autoswitch-restore-barrier.json
-rw-r--r-- 1 root root 598 May 27 16:13 /opt/v7/egress/state/autoswitch-restore-barrier.json.backup-e12-nonzero-20260527T171252Z
-rw-r--r-- 1 root root 447 May 27 13:52 /opt/v7/egress/state/autoswitch-restore-barrier.json.e11_17_backup_20260527T123920Z
# hidden
# checkers
user=10.7.0.13 enabled=1 current=awg0 table=1011
user=10.7.0.14 enabled=1 current=1 table=1012
user=10.7.0.15 enabled=1 current=1 table=1013

===== RESULT =====
warnings=0
errors=0
V7_RECONCILE_RESULT=OK
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 table=1013 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0 
OK: user=10.7.0.15 route_get uses v7e356a192b79

===== RESULT =====
V7_USER_ROUTE_CHECK=OK
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.14 route_get uses expected egress
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 route_get uses expected egress

===== RESULT =====
V7_KILLSWITCH_CHECK=OK
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.14 table=1012 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 

===== RESULT =====
V7_PROVISIONING_RECONCILE_CHECK=OK
