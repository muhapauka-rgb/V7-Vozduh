# E30.2 Capacity Requalification

capacity_requalification_attempted=true
capacity_requalification_successful=true
backup_path=/opt/v7/egress/state/e30_2-backups/egress.registry.20260529T143441Z
old_egress_registry_hash=0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689
new_egress_registry_hash=f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5
soft_limit_before=4
hard_limit_before=4
soft_limit_final=10
hard_limit_final=10
runtime_checkers_ok_after=true
readiness_after=GO
rollback_plan=restore /opt/v7/egress/state/e30_2-backups/egress.registry.20260529T143441Z to /opt/v7/egress/state/egress.registry and rerun runtime checkers

## Diff
--- /tmp/e30_2/egress.before.requalification	2026-05-29 09:39:51.503914254 +0300
+++ /tmp/e30_2/egress.after.requalification	2026-05-29 17:34:41.495998606 +0300
@@ -4,4 +4,4 @@
 id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
 id=openvpn-1779388847-d2ad7c protocol=openvpn type=interface interface=v7edb0c189291 test=interface enabled=1 config=/etc/v7/egress-openvpn/v7edb0c189291.ovpn role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
 id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
-id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=4 hard_limit=4 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
+id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=10 hard_limit=10 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
