# E22.1 Live Recheck-Only Result

Live runtime recheck result:

```json
{
  "allow": true,
  "verdict": "ALLOW_RECORD_ONLY",
  "errors": [],
  "checks": {
    "users_registry_hash": "bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c",
    "egress_registry_hash": "a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8",
    "runtime_snapshot_hash": "c5f58e490844e1ddb8cb29ba143a26a1479a45fc94cf08140ffb0931f199b2d5",
    "selected_move_count": 0,
    "selected_move_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "selected_move_source": "missing_treated_as_empty",
    "real_runtime_action_after_recheck": false
  }
}
```

No approval/audit approval record was written during recheck-only. The later execute phase performed the append-only audit write.
