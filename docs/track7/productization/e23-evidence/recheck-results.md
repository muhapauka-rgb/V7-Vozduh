# E23 Validate And Live Recheck

## Validate Only

```text
verdict=PACKET_VALID
errors=[]
```

## Live Recheck Only

```text
allow=true
verdict=ALLOW_ZERO_MOVE_RUNTIME_ACTION
errors=[]
users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
runtime_snapshot_hash=c5f58e490844e1ddb8cb29ba143a26a1479a45fc94cf08140ffb0931f199b2d5
selected_move_count=0
selected_move_hash=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
restore_barrier_hash=f5f37e9595f87233939ed067ef25e58c500adae687de4090a8c1832140571079
autoswitch_safety_hash=e13fcf81c723247ac0781c95206fc8fdc55bc5791ca696b39fb5aa5768d50083
real_runtime_action_after_recheck=false
```

The recheck did not perform the runtime action. It only proved that execution could proceed to the selected zero-move governance state transition.
