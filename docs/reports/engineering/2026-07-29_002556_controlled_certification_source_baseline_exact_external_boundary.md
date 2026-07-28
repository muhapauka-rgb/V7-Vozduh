# Engineering Report — точная граница baseline controlled certification source

Дата: `2026-07-29T00:25:56+07:00`

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: существующая `T48-M8`

## Результат

Выполнены discovery, knowledge reuse, точная production-диагностика, smallest
existing-owner repair диагностической проекции, safe deploy, production
caller/consumer и атомарное CPS reconciliation.

Healthy baseline восстановить внутри доступных V7 owners нельзя. Законный
terminal:

`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_SOURCE_BASELINE_REQUIRED`

Стадии `5 -> 10 -> 25 -> 48` не запускались: source `1` не имеет нормального
здорового baseline, поэтому deliberate failure неотличим от уже существующего
внешнего отказа и не может породить controlled production evidence.

## Discover → Reuse

Owner-backed production truth:

- exact approved source: `1`;
- protocol/interface: `amneziawg` / `v7e356a192b79`;
- 48 enabled dedicated certification identities;
- 0 ordinary users;
- Matrix: `0/14` reachable, `14` hard failures;
- interface: `UP,LOWER_UP`;
- address: `10.10.120.8/32`;
- все 48 user policy tables имеют default route через exact interface;
- endpoint routing идёт через production uplink, а не рекурсивно через tunnel;
- AWG transfer: `TX=344587`, `RX=0`;
- latest handshake: `0` / `handshake_age_seconds=999999`;
- bounded packet observation: 8 outbound peer datagrams, 0 inbound;
- существующий `v7-egress-diagnose`:
  `curl_failed_and_handshake_stale`, severity `FAIL`;
- текущий profile и сохранённый исторически рабочий profile семантически
  совпадают, включая endpoint, address, AWG parameters и key fingerprints;
- историческое owner-backed evidence фиксирует fresh handshake на этом exact
  interface, следовательно registry/interface contract раньше был рабочим;
- штатный lifecycle restart уже выполнялся и не восстановил peer; повтор без
  invalidation trigger не делался.

## Проверка альтернатив

Existing controlled-source projection не нашла ни одного
`healthy_isolated_source_candidate`.

- healthy WireGuard controlled source содержит 46 ordinary и 3 certification
  users, поэтому не изолирован;
- healthy execution-only egress свободен, но имеет `hard_limit=10`,
  `production_assignment_allowed=false` и owner reservation;
- остальные healthy sources заняты ordinary production;
- перемещение ordinary users, перепривязка exact-source approval или
  саморасширение Authority запрещены.

Следовательно, легально relocate существующий pool до 48 через текущий
approval невозможно.

## Точная классификация

`CONTROLLED_SOURCE_ROOT_CAUSE_CLASS`:
`EXTERNAL_INFRASTRUCTURE_OR_ACCESS_REQUIRED`.

Наблюдаемая локальная сторона не позволяет честно различить недоступный remote
peer и отозванный/несовпадающий remote key material: обе причины дают
исходящие handshake datagrams без ответа. Поэтому не заявляется более узкий
неподтверждённый диагноз.

- `EXACT_EXTERNAL_RESOURCE`:
  `AMNEZIAWG_REMOTE_PEER_OR_MATCHING_PROFILE_FOR_SOURCE_1`;
- `EXACT_EXTERNAL_OWNER`:
  `EXTERNAL_AMNEZIAWG_PEER_OR_CREDENTIAL_PROVIDER`;
- `EXACT_REQUIRED_INPUT`:
  `OWNER_VERIFIED_REACHABLE_REMOTE_PEER_WITH_MATCHING_KEY_MATERIAL_OR_REPLACEMENT_WORKING_PROFILE_FOR_THE_EXACT_APPROVED_SOURCE`;
- `WHY_EXISTING_OWNERS_CANNOT_SUPPLY_IT`:
  local V7 owners могут reload и проверить имеющийся profile, но не могут
  восстановить внешний peer либо выдать согласованную пару внешних ключей;
- failed link:
  `EXTERNAL_AMNEZIAWG_PEER_RESPONSE_OR_MATCHING_PROFILE -> LOCAL_HANDSHAKE -> MATRIX_BASELINE`.

## Existing-owner extension

Новый owner, registry, log store, watcher или scheduler не создавался.

Расширена существующая компактная проекция
`controlled_certification_source_health_status`:

- она потребляет уже существующие `service-matrix.json`,
  `egress-diagnose.state` и `egress.registry`;
- сохраняет только counts, fingerprints и bounded causal classification;
- не копирует raw service logs или identities;
- выдаёт точные resource/owner/input/failed-link/re-entry поля;
- атомарный CPS consumer публикует эти поля в live current state.

## Tests, deploy и production consumption

- focused service-failure suite: `48/48 PASS`;
- full affected suite: `117/117 PASS`;
- safe-deploy manifest: `PASS`, blockers `0`, warnings `0`;
- runtime delta только:
  - `tools/v7-users-autoswitch`;
  - `tools/v7_sync_lib.py`;
- runtime commit: `422424a59776552bceb97619bc794249f90816fd`;
- deploy:
  `deploy-z8-14-Updatesystem-422424a-20260729T002345`;
- production non-test status caller: `PASS`;
- production CPS consumer:
  `tools/v7-truth-check --reconcile-active-standing-delegated-policy --json`;
- CPS atomic update: `ATOMIC_CPS_UPDATE_APPLIED`;
- root-cause projection schema:
  `v7.controlled-certification-source-health.v2`.

Forbidden effects:

- Candidate/Packet/lease: `0`;
- restore-barrier write: `0`;
- runtime apply/routing mutation/user movement: `0`;
- rollback apply: `0`;
- Authority expansion: `0`;
- Production Maturity change: `0`.

## Pool/campaign state и re-entry

- current pool: 48 dedicated identities on exact source `1`;
- campaign approval remains active and hash-bound;
- stages `5,10,25,48`: unexecuted;
- next consumer:
  `existing service-matrix baseline consumer -> existing T48-M8 controlled campaign owner`;
- automatic re-entry:
  external owner restores the matching peer/profile, then a fresh Matrix
  generation proves at least one reachable service and zero hard failures on
  the exact source.

После такого owner-backed state change существующая campaign должна продолжить
без нового Program и без повторной generic Tier-48 certification.

## Итог

Текущий prompt выполнен до доказанной независимой внешней границы. Финальный
успешный Program terminal
`SERVICE_FAILURE_CONTROLLED_PRODUCTION_OUTCOMES_CONSUMED_5_10_25_48`
не достигнут и не заявляется: для него сначала требуется указанный exact
external input.
