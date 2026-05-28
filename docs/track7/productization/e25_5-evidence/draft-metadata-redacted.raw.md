--- /etc/v7/egress-drafts/wg-1779455931-ba621c/metadata.json
{
  "config_path": "<redacted>",
  "config_sha256": "<redacted>",
  "created_at": "2026-05-22T13:18:51.151366+00:00",
  "created_by": "admin",
  "detected_fields": {
    "address": "present",
    "endpoint_host": "89.191.226.228",
    "interface": "present",
    "peer": "present",
    "table": ""
  },
  "duplicate_of": {
    "config": "<redacted>",
    "egress": "wireguard-1779454504-c43409",
    "enabled": "0",
    "interface": "v7e06a394c478"
  },
  "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
  "hard_limit": "2",
  "id": "wg-1779455931-ba621c",
  "import_pipeline_finished_at": "2026-05-22T13:21:15.668657+00:00",
  "import_pipeline_started_at": "2026-05-22T13:18:51.151960+00:00",
  "import_pipeline_status": "UPDATED_EXISTING",
  "internal_import": true,
  "label": "wg \u0433\u0435\u0440\u043c\u0430\u0448\u043a\u0430, \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442",
  "last_preflight_at": "2026-05-22T13:18:51.154577+00:00",
  "last_preflight_run_id": "wg-1779455931-ba621c-1779455931-4d4466",
  "last_preflight_status": "PASS",
  "last_quarantine_at": "2026-05-22T13:18:52.177488+00:00",
  "last_quarantine_run_id": "wg-1779455931-ba621c-runtime-1779455932-39b6db",
  "last_quarantine_status": "PASS",
  "last_role_fit": {
    "reason": "all required services passed",
    "role": "GLOBAL_FAST",
    "status": "OK"
  },
  "last_route_class_fitness": {
    "DIRECT_RU": {
      "avg_first_byte_sec": 1.506,
      "missing": [],
      "missing_count": 0,
      "ok_count": 3,
      "reason": "some services passed and some failed",
      "services": [
        "yandex",
        "vk",
        "ozon",
        "lamoda"
      ],
      "status": "WARN",
      "tested_count": 4,
      "total": 4
    },
    "GLOBAL_FAST": {
      "avg_first_byte_sec": 0.265,
      "missing": [],
      "missing_count": 0,
      "ok_count": 4,
      "reason": "all required services passed",
      "services": [
        "cloudflare",
        "google",
        "telegram",
        "facebook"
      ],
      "status": "OK",
      "tested_count": 4,
      "total": 4
    },
    "GLOBAL_STABLE": {
      "avg_first_byte_sec": 0.309,
      "missing": [],
      "missing_count": 0,
      "ok_count": 5,
      "reason": "all required services passed",
      "services": [
        "cloudflare",
        "google",
        "telegram",
        "apple",
        "whatsapp"
      ],
      "status": "OK",
      "tested_count": 5,
      "total": 5
    },
    "LOW_LATENCY": {
      "avg_first_byte_sec": 0.267,
      "missing": [],
      "missing_count": 0,
      "ok_count": 3,
      "reason": "all required services passed",
      "services": [
        "cloudflare",
        "google",
        "telegram"
      ],
      "status": "OK",
      "tested_count": 3,
      "total": 3
    },
    "TRUSTED_RU_SENSITIVE": {
      "avg_first_byte_sec": 1.287,
      "missing": [],
      "missing_count": 0,
      "ok_count": 4,
      "reason": "some services passed and some failed",
      "services": [
        "gosuslugi",
        "esia",
        "nalog",
        "alfa_bank",
        "tbank",
        "sber"
      ],
      "status": "WARN",
      "tested_count": 6,
      "total": 6
    },
    "VIDEO_OPTIMIZED": {
      "avg_first_byte_sec": 0.42,
      "missing": [],
      "missing_count": 0,
      "ok_count": 4,
      "reason": "all required services passed",
      "services": [
        "youtube",
        "instagram",
        "spotify",
        "soundcloud"
      ],
      "status": "OK",
      "tested_count": 4,
      "total": 4
    }
  },
  "last_runtime_at": "2026-05-22T13:18:52.177488+00:00",
  "last_runtime_run_id": "wg-1779455931-ba621c-runtime-1779455932-39b6db",
  "last_runtime_status": "PASS",
  "last_service_matrix_status": "WARN",
  "lifecycle": {
    "blockers": [],
    "complete": true,
    "current": "add_disabled",
    "next_action": "add_disabled",
    "next_label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
    "steps": [
      {
        "detail": "detected_required_fields",
        "id": "detect",
        "label": "\u0420\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u0435",
        "status": "DONE"
      },
      {
        "detail": "existing_channel_updated",
        "id": "draft",
        "label": "\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f\u044f \u0437\u0430\u043f\u0438\u0441\u044c",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "preflight",
        "label": "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "runtime",
        "label": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "quarantine",
        "label": "\u0418\u0437\u043e\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430",
        "status": "DONE"
      },
      {
        "detail": "updated_existing",
        "id": "add_disabled",
        "label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
        "status": "ACTIVE"
      },
      {
        "detail": "READY",
        "id": "provision",
        "label": "\u0420\u0430\u0431\u043e\u0447\u0438\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c",
        "status": "DONE"
      },
      {
        "detail": "separate guarded action",
        "id": "enable",
        "label": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435",
        "status": "WAITING"
      }
    ]
  },
  "manual_only": "0",
  "missing": [],
  "next_step": "existing_channel_updated_disabled",
  "organization_scope": [
    "global"
  ],
  "pool_action": "updated_existing",
  "pool_egress_id": "wireguard-1779454504-c43409",
  "priority": "20",
  "protocol": "wireguard",
  "reserve_only": "0",
  "role": "GLOBAL_FAST",
  "runtime_mode": "interface",
  "runtime_profile_interface": "v7e06a394c478",
  "runtime_profile_path": "/etc/wireguard/v7e06a394c478.conf",
  "runtime_profile_status": "READY",
  "service_tags": "google,telegram,instagram,global",
  "soft_limit": "1",
  "status": "existing_channel_updated",
  "updated_existing_at": "2026-05-22T13:21:15.667936+00:00",
  "updated_existing_by": "admin",
  "updated_existing_config_backup": "<redacted>",
  "updated_existing_config_path": "<redacted>",
  "updated_existing_egress": "wireguard-1779454504-c43409",
  "usage_policy": {
    "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
    "hard_limit": "2",
    "manual_only": "0",
    "priority": "20",
    "reserve_only": "0",
    "role": "GLOBAL_FAST",
    "service_tags": "google,telegram,instagram,global",
    "soft_limit": "1",
    "weight": "100"
  },
  "user_visible": false,
  "validation": "detected_required_fields",
  "warnings": [
    "V7 will normalize this interface to Table = off in the isolated runtime copy because V7 owns routing."
  ],
  "weight": "100"
}
--- /etc/v7/egress-drafts/openvpn-1779453676-42885e/metadata.json
{
  "config_path": "<redacted>",
  "config_sha256": "<redacted>",
  "created_at": "2026-05-22T12:41:16.596635+00:00",
  "created_by": "admin",
  "detected_fields": {
    "auth_material": "present",
    "client": "present",
    "dev": "tun",
    "proto": "udp",
    "pull_filter": "not_configured",
    "redirect_gateway": "present",
    "remote": "138.16.179.194 25065 udp",
    "scripts": "absent"
  },
  "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
  "hard_limit": "2",
  "id": "openvpn-1779453676-42885e",
  "import_pipeline_started_at": "2026-05-22T12:41:16.597270+00:00",
  "import_pipeline_status": "RUNNING",
  "internal_import": true,
  "label": "openvpn-1779453676-42885e",
  "last_preflight_at": "2026-05-22T12:41:16.608221+00:00",
  "last_preflight_run_id": "openvpn-1779453676-42885e-1779453676-d82055",
  "last_preflight_status": "PASS",
  "last_runtime_at": "2026-05-22T12:52:55.151969+00:00",
  "last_runtime_run_id": "openvpn-1779453676-42885e-runtime-1779454375-4f05cc",
  "last_runtime_status": "FAIL",
  "lifecycle": {
    "blockers": [],
    "complete": false,
    "current": "run_runtime",
    "next_action": "run_runtime",
    "next_label": "\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
    "steps": [
      {
        "detail": "detected_required_fields",
        "id": "detect",
        "label": "\u0420\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u0435",
        "status": "DONE"
      },
      {
        "detail": "draft",
        "id": "draft",
        "label": "\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f\u044f \u0437\u0430\u043f\u0438\u0441\u044c",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "preflight",
        "label": "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
        "status": "DONE"
      },
      {
        "detail": "FAIL",
        "id": "runtime",
        "label": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
        "status": "ACTIVE"
      },
      {
        "detail": "",
        "id": "quarantine",
        "label": "\u0418\u0437\u043e\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430",
        "status": "WAITING"
      },
      {
        "detail": "not_added",
        "id": "add_disabled",
        "label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
        "status": "WAITING"
      },
      {
        "detail": "",
        "id": "provision",
        "label": "\u0420\u0430\u0431\u043e\u0447\u0438\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c",
        "status": "WAITING"
      },
      {
        "detail": "separate guarded action",
        "id": "enable",
        "label": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435",
        "status": "WAITING"
      }
    ]
  },
  "manual_only": "0",
  "missing": [],
  "next_step": "inspect_runtime_failure",
  "organization_scope": [
    "global"
  ],
  "pool_action": "not_added",
  "priority": "20",
  "protocol": "openvpn",
  "reserve_only": "0",
  "role": "GLOBAL_FAST",
  "runtime_mode": "interface",
  "service_tags": "google,telegram,instagram,global",
  "soft_limit": "1",
  "status": "draft",
  "usage_policy": {
    "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
    "hard_limit": "2",
    "manual_only": "0",
    "priority": "20",
    "reserve_only": "0",
    "role": "GLOBAL_FAST",
    "service_tags": "google,telegram,instagram,global",
    "soft_limit": "1",
    "weight": "100"
  },
  "user_visible": false,
  "validation": "detected_required_fields",
  "warnings": [
    "OpenVPN \u0440\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u043d. V7 \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442 \u0435\u0433\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043a\u0430\u043a \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0439 \u043a\u0430\u043d\u0430\u043b: \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b, DNS \u0438 \u0441\u043a\u0440\u0438\u043f\u0442\u044b \u0431\u0443\u0434\u0443\u0442 \u043d\u043e\u0440\u043c\u0430\u043b\u0438\u0437\u043e\u0432\u0430\u043d\u044b \u043f\u0435\u0440\u0435\u0434 \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u043e\u0439."
  ],
  "weight": "100"
}
--- /etc/v7/egress-drafts/openvpn-1779385423-2121b0/metadata.json
{
  "config_path": "<redacted>",
  "config_sha256": "<redacted>",
  "created_at": "2026-05-21T17:43:43.285697+00:00",
  "created_by": "admin",
  "detected_fields": {
    "auth_material": "present",
    "client": "present",
    "dev": "tun",
    "proto": "udp",
    "pull_filter": "not_configured",
    "redirect_gateway": "present",
    "remote": "80.85.245.161 60826 udp",
    "scripts": "absent"
  },
  "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
  "hard_limit": "2",
  "id": "openvpn-1779385423-2121b0",
  "label": "openvpn-1779385423-2121b0",
  "lifecycle": {
    "blockers": [],
    "complete": false,
    "current": "run_preflight",
    "next_action": "run_preflight",
    "next_label": "\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
    "steps": [
      {
        "detail": "detected_required_fields",
        "id": "detect",
        "label": "\u0420\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u0435",
        "status": "DONE"
      },
      {
        "detail": "draft",
        "id": "draft",
        "label": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0447\u0435\u0440\u043d\u043e\u0432\u0438\u043a",
        "status": "DONE"
      },
      {
        "detail": "",
        "id": "preflight",
        "label": "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
        "status": "ACTIVE"
      },
      {
        "detail": "",
        "id": "runtime",
        "label": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
        "status": "WAITING"
      },
      {
        "detail": "",
        "id": "quarantine",
        "label": "\u0418\u0437\u043e\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430",
        "status": "WAITING"
      },
      {
        "detail": "not_added",
        "id": "add_disabled",
        "label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
        "status": "WAITING"
      },
      {
        "detail": "",
        "id": "provision",
        "label": "\u0420\u0430\u0431\u043e\u0447\u0438\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c",
        "status": "WAITING"
      },
      {
        "detail": "separate guarded action",
        "id": "enable",
        "label": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435",
        "status": "WAITING"
      }
    ]
  },
  "manual_only": "0",
  "missing": [],
  "next_step": "isolated_test_profile",
  "organization_scope": [
    "global"
  ],
  "pool_action": "not_added",
  "priority": "20",
  "protocol": "openvpn",
  "reserve_only": "0",
  "role": "GLOBAL_FAST",
  "runtime_mode": "interface",
  "service_tags": "google,telegram,instagram,global",
  "soft_limit": "1",
  "status": "draft",
  "usage_policy": {
    "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
    "hard_limit": "2",
    "manual_only": "0",
    "priority": "20",
    "reserve_only": "0",
    "role": "GLOBAL_FAST",
    "service_tags": "google,telegram,instagram,global",
    "soft_limit": "1",
    "weight": "100"
  },
  "validation": "detected_required_fields",
  "warnings": [
    "OpenVPN \u0440\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u043d. V7 \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442 \u0435\u0433\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043a\u0430\u043a \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0439 \u043a\u0430\u043d\u0430\u043b: \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b, DNS \u0438 \u0441\u043a\u0440\u0438\u043f\u0442\u044b \u0431\u0443\u0434\u0443\u0442 \u043d\u043e\u0440\u043c\u0430\u043b\u0438\u0437\u043e\u0432\u0430\u043d\u044b \u043f\u0435\u0440\u0435\u0434 \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u043e\u0439."
  ],
  "weight": "100"
}
--- /etc/v7/egress-drafts/openvpn-1779387408-c42bdf/metadata.json
{
  "config_path": "<redacted>",
  "config_sha256": "<redacted>",
  "created_at": "2026-05-21T18:16:48.978293+00:00",
  "created_by": "admin",
  "detected_fields": {
    "auth_material": "present",
    "client": "present",
    "dev": "tun",
    "proto": "udp",
    "pull_filter": "not_configured",
    "redirect_gateway": "present",
    "remote": "80.85.245.161 60826 udp",
    "scripts": "absent"
  },
  "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
  "hard_limit": "2",
  "id": "openvpn-1779387408-c42bdf",
  "import_pipeline_started_at": "2026-05-21T18:16:48.978847+00:00",
  "import_pipeline_status": "RUNNING",
  "internal_import": true,
  "label": "openvpn-1779387408-c42bdf",
  "last_preflight_at": "2026-05-21T18:16:48.984289+00:00",
  "last_preflight_run_id": "openvpn-1779387408-c42bdf-1779387408-07b64d",
  "last_preflight_status": "PASS",
  "last_quarantine_at": "2026-05-21T18:16:49.794432+00:00",
  "last_quarantine_run_id": "openvpn-1779387408-c42bdf-quarantine-1779387409-966d63",
  "last_quarantine_status": "BLOCKED",
  "last_role_fit": {
    "reason": "\u0447\u0430\u0441\u0442\u044c \u0441\u0435\u0440\u0432\u0438\u0441\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442, \u0447\u0430\u0441\u0442\u044c \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443",
    "role": "GLOBAL_FAST",
    "status": "WARN"
  },
  "last_route_class_fitness": {
    "DIRECT_RU": {
      "avg_first_byte_sec": null,
      "missing": [],
      "missing_count": 0,
      "ok_count": 0,
      "reason": "\u0435\u0449\u0451 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u043b\u043e\u0441\u044c",
      "services": [],
      "status": "UNKNOWN",
      "tested_count": 0,
      "total": 0
    },
    "GLOBAL_FAST": {
      "avg_first_byte_sec": 0.31,
      "missing": [],
      "missing_count": 0,
      "ok_count": 4,
      "reason": "\u0447\u0430\u0441\u0442\u044c \u0441\u0435\u0440\u0432\u0438\u0441\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442, \u0447\u0430\u0441\u0442\u044c \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443",
      "services": [
        "google",
        "google_auth",
        "telegram",
        "facebook",
        "chatgpt",
        "openai_auth"
      ],
      "status": "WARN",
      "tested_count": 6,
      "total": 6
    },
    "GLOBAL_STABLE": {
      "avg_first_byte_sec": 0.313,
      "missing": [
        "apple",
        "whatsapp"
      ],
      "missing_count": 2,
      "ok_count": 3,
      "reason": "\u0447\u0430\u0441\u0442\u044c \u0441\u0435\u0440\u0432\u0438\u0441\u043e\u0432 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442, \u0447\u0430\u0441\u0442\u044c \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443",
      "services": [
        "google",
        "google_auth",
        "telegram",
        "apple",
        "whatsapp",
        "chatgpt",
        "openai_auth"
      ],
      "status": "WARN",
      "tested_count": 5,
      "total": 7
    },
    "LOW_LATENCY": {
      "avg_first_byte_sec": 0.313,
      "missing": [],
      "missing_count": 0,
      "ok_count": 3,
      "reason": "\u0432\u0441\u0435 \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0441\u0435\u0440\u0432\u0438\u0441\u044b \u043f\u0440\u043e\u0448\u043b\u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443",
      "services": [
        "google",
        "google_auth",
        "telegram"
      ],
      "status": "OK",
      "tested_count": 3,
      "total": 3
    },
    "TRUSTED_RU_SENSITIVE": {
      "avg_first_byte_sec": null,
      "missing": [],
      "missing_count": 0,
      "ok_count": 0,
      "reason": "\u0435\u0449\u0451 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u043b\u043e\u0441\u044c",
      "services": [],
      "status": "UNKNOWN",
      "tested_count": 0,
      "total": 0
    },
    "VIDEO_OPTIMIZED": {
      "avg_first_byte_sec": null,
      "missing": [
        "youtube",
        "instagram",
        "spotify",
        "soundcloud"
      ],
      "missing_count": 4,
      "ok_count": 0,
      "reason": "\u0435\u0449\u0451 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u043b\u043e\u0441\u044c",
      "services": [
        "youtube",
        "instagram",
        "spotify",
        "soundcloud"
      ],
      "status": "UNKNOWN",
      "tested_count": 0,
      "total": 4
    }
  },
  "last_runtime_at": "2026-05-21T18:16:49.794432+00:00",
  "last_runtime_run_id": "openvpn-1779387408-c42bdf-quarantine-1779387409-966d63",
  "last_runtime_status": "PASS",
  "last_service_matrix_status": "WARN",
  "lifecycle": {
    "blockers": [],
    "complete": false,
    "current": "run_quarantine",
    "next_action": "run_quarantine",
    "next_label": "\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043a\u0430\u0440\u0430\u043d\u0442\u0438\u043d",
    "steps": [
      {
        "detail": "detected_required_fields",
        "id": "detect",
        "label": "\u0420\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u0435",
        "status": "DONE"
      },
      {
        "detail": "draft",
        "id": "draft",
        "label": "\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f\u044f \u0437\u0430\u043f\u0438\u0441\u044c",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "preflight",
        "label": "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "runtime",
        "label": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
        "status": "DONE"
      },
      {
        "detail": "BLOCKED",
        "id": "quarantine",
        "label": "\u0418\u0437\u043e\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430",
        "status": "ACTIVE"
      },
      {
        "detail": "not_added",
        "id": "add_disabled",
        "label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
        "status": "WAITING"
      },
      {
        "detail": "",
        "id": "provision",
        "label": "\u0420\u0430\u0431\u043e\u0447\u0438\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c",
        "status": "WAITING"
      },
      {
        "detail": "separate guarded action",
        "id": "enable",
        "label": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435",
        "status": "WAITING"
      }
    ]
  },
  "manual_only": "0",
  "missing": [],
  "next_step": "service_matrix_quarantine_test",
  "organization_scope": [
    "global"
  ],
  "pool_action": "not_added",
  "priority": "20",
  "protocol": "openvpn",
  "reserve_only": "0",
  "role": "GLOBAL_FAST",
  "runtime_mode": "interface",
  "service_tags": "google,telegram,instagram,global",
  "soft_limit": "1",
  "status": "draft",
  "usage_policy": {
    "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
    "hard_limit": "2",
    "manual_only": "0",
    "priority": "20",
    "reserve_only": "0",
    "role": "GLOBAL_FAST",
    "service_tags": "google,telegram,instagram,global",
    "soft_limit": "1",
    "weight": "100"
  },
  "user_visible": false,
  "validation": "detected_required_fields",
  "warnings": [
    "OpenVPN \u0440\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u043d. V7 \u0437\u0430\u043f\u0443\u0441\u0442\u0438\u0442 \u0435\u0433\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043a\u0430\u043a \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0439 \u043a\u0430\u043d\u0430\u043b: \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b, DNS \u0438 \u0441\u043a\u0440\u0438\u043f\u0442\u044b \u0431\u0443\u0434\u0443\u0442 \u043d\u043e\u0440\u043c\u0430\u043b\u0438\u0437\u043e\u0432\u0430\u043d\u044b \u043f\u0435\u0440\u0435\u0434 \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u043e\u0439."
  ],
  "weight": "100"
}
--- /etc/v7/egress-drafts/subscription_url-1779462892-4d2cea/metadata.json
{
  "config_path": "<redacted>",
  "config_sha256": "<redacted>",
  "created_at": "2026-05-22T15:14:52.676194+00:00",
  "created_by": "admin",
  "detected_fields": {
    "host": "91.198.220.178",
    "path": "/sub/z6cyoe08town0e03",
    "scheme": "https",
    "url": "<redacted>"
  },
  "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
  "hard_limit": "2",
  "id": "subscription_url-1779462892-4d2cea",
  "import_pipeline_started_at": "2026-05-22T15:14:52.676567+00:00",
  "import_pipeline_status": "RUNNING",
  "internal_import": true,
  "label": "subscription_url-1779462892-4d2cea",
  "last_preflight_at": "2026-05-22T15:14:52.678664+00:00",
  "last_preflight_run_id": "subscription_url-1779462892-4d2cea-1779462892-48c0db",
  "last_preflight_status": "PASS",
  "lifecycle": {
    "blockers": [
      "subscription_url_adapter_required"
    ],
    "complete": false,
    "current": "expand_or_convert_config",
    "next_action": "expand_or_convert_config",
    "next_label": "\u0420\u0430\u0437\u0432\u0435\u0440\u043d\u0443\u0442\u044c \u0432 \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0439 \u0447\u0435\u0440\u043d\u043e\u0432\u0438\u043a",
    "steps": [
      {
        "detail": "detected_required_fields",
        "id": "detect",
        "label": "\u0420\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u0435",
        "status": "DONE"
      },
      {
        "detail": "draft",
        "id": "draft",
        "label": "\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f\u044f \u0437\u0430\u043f\u0438\u0441\u044c",
        "status": "DONE"
      },
      {
        "detail": "PASS",
        "id": "preflight",
        "label": "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0431\u0435\u0437 \u0437\u0430\u043f\u0443\u0441\u043a\u0430",
        "status": "DONE"
      },
      {
        "detail": "",
        "id": "runtime",
        "label": "\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u0441\u0442",
        "status": "BLOCKED"
      },
      {
        "detail": "",
        "id": "quarantine",
        "label": "\u0418\u0437\u043e\u043b\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430",
        "status": "BLOCKED"
      },
      {
        "detail": "not_added",
        "id": "add_disabled",
        "label": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u043c",
        "status": "BLOCKED"
      },
      {
        "detail": "",
        "id": "provision",
        "label": "\u0420\u0430\u0431\u043e\u0447\u0438\u0439 \u043f\u0440\u043e\u0444\u0438\u043b\u044c",
        "status": "BLOCKED"
      },
      {
        "detail": "separate guarded action",
        "id": "enable",
        "label": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435",
        "status": "BLOCKED"
      }
    ]
  },
  "manual_only": "0",
  "missing": [],
  "next_step": "isolated_runtime_test",
  "organization_scope": [
    "global"
  ],
  "pool_action": "not_added",
  "priority": "20",
  "protocol": "subscription_url",
  "reserve_only": "0",
  "role": "GLOBAL_FAST",
  "runtime_mode": "subscription",
  "service_tags": "google,telegram,instagram,global",
  "soft_limit": "1",
  "status": "draft",
  "usage_policy": {
    "exclude_route_classes": "TRUSTED_RU_SENSITIVE,DIRECT_RU",
    "hard_limit": "2",
    "manual_only": "0",
    "priority": "20",
    "reserve_only": "0",
    "role": "GLOBAL_FAST",
    "service_tags": "google,telegram,instagram,global",
    "soft_limit": "1",
    "weight": "100"
  },
  "user_visible": false,
  "validation": "detected_required_fields",
  "warnings": [
    "Subscription URL is recognized. Runtime use is blocked until V7 fetches, validates, and lets the operator choose concrete endpoints."
  ],
  "weight": "100"
}
