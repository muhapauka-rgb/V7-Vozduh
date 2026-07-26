# Отчёт: обязательное правило semantic discovery перед реализацией

Дата: `2026-07-26`

Перед продолжением M5–M7 в каноническую программу добавлено обязательное
правило: каждое изменение начинается не с кода, а с доказательства текущей
semantic topology.

```text
required outcome
-> producer
-> durable identity
-> consumer
-> verification
-> terminal or successor
```

Проверка выполняется по смыслу и data-flow, а не по совпадению названий
файлов. Сначала требуется найти существующие owners, их deployed/live status,
identities, freshness, one-use limits, Authority boundary и фактические
producer-to-consumer links.

Порядок исполнения закреплён как:

```text
discover
-> trace connections
-> reuse
-> minimally connect or extend
-> implement only the proven residual
-> verify real downstream consumption
```

Это защищает V7 от дублирования уже существующих capabilities и от
«реализации ради реализации». Новый код допустим только для минимального
доказанного отсутствующего или разорванного handoff. Completion означает, что
выход достиг существующего downstream owner и изменил exact successor,
terminal или capability projection.
