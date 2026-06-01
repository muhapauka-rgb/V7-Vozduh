# P5R Observation Window

Project: V7 Vozduh

Block: P5 RETRY

## Observation Samples

Samples captured:

- before action
- immediately after action
- after 2 seconds
- after replay/fail-closed denial tests

## Before And After Invariants

| Field | Before | After denial tests | Unchanged |
| --- | --- | --- | --- |
| users registry hash | `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f` | `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f` | true |
| egress registry hash | `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5` | `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5` | true |
| selected moves hash | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | true |
| selected moves count | `0` | `0` | true |
| runtime snapshot hash | `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84` | `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84` | true |
| route table hash | `04b2279db976810ff7aaada7908dddc1d48c1aeaa7dfea371252798a434ccfe2` | `04b2279db976810ff7aaada7908dddc1d48c1aeaa7dfea371252798a434ccfe2` | true |
| ip rule hash | `e8902acd1be10b6f7df14c23f557136a8453ba5b8520393d63b4a689334354ff` | `e8902acd1be10b6f7df14c23f557136a8453ba5b8520393d63b4a689334354ff` | true |
| autoswitch timer | `inactive` | `inactive` | true |

## Final Store Counts

- audit records: `8`
- governance records: `1`

The additional audit records after the primary action are denial records from replay and fail-closed tests. No additional governance record was appended.

## Verdict

- observation_window_complete=true
- users_unchanged=true
- routing_unchanged=true
- autoswitch_unchanged=true
- runtime_state_preserved=true
