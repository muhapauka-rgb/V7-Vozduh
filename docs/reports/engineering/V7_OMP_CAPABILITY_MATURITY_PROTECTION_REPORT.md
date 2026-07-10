# V7 OMP Capability Maturity Protection Engineering Report

Дата: 2026-07-10
Статус: `PASS`
Область: `OPERATIONAL_MATURITY_PROGRAM`

## Summary

В OMP добавлен минимальный protection pre-check перед Necessity, Merge, Remove, Value Conservation и архитектурной минимизацией.

Теперь элемент, принадлежащий незавершенной Capability, получает статус:

```text
PROTECTED_BY_CAPABILITY_MATURITY
```

и не может быть объединен, удален, collapsed, eliminated или минимизирован до завершения Capability Lifecycle.

Новая программа, owner, архитектура, Runtime, Planner, Protection Engine, Capability Engine, Lifecycle Engine, Optimization Engine, graph, queue или Candidate type не создавались.

## Существовал Ли Такой Механизм

Полностью готового запрета найдено не было.

Найдены существующие частичные механизмы:

| Механизм | Статус | Как переиспользован |
| --- | --- | --- |
| Capability Management | `EXISTS` | Уже определяет Capability как maturity unit, status values, DoD, completion, lock и re-open triggers. |
| Capability Production Contract | `EXISTS` | Уже определяет путь Engineering Complete -> Production Candidate -> Capability Certified -> Production Maturity -> Next Capability. |
| Necessity Framework | `EXISTS` | Уже определяет Creation, Removal, Merge, Chain Completion и Necessity Certification. |
| Architecture Closed by Default | `EXISTS` | Запрещает новую архитектуру до доказательства невозможности reuse. |
| Need New Owner Gate | `EXISTS` | Запрещает новых owners без proof. |
| Semantic Reuse Audit | `EXISTS` | Проверяет reuse/extend/merge до создания нового. |
| Automation Gap Closure | `EXISTS` | Маршрутизирует автоматизируемые gaps через BDP -> OMP. |
| Intent Responsibility Resolution | `EXISTS` | Определяет owner-mapped failed chain link. |

Пробел: эти механизмы не запрещали явно применять Merge/Remove/минимизацию к элементу, который пока не имеет downstream value только потому, что его Capability еще не завершена.

## Что Добавлено

В `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` добавлено:

- версия `4.12`;
- `Law 17: Capability Maturity Protection Law`;
- раздел `Capability Maturity Protection` внутри `Necessity Framework Consumption`;
- обязательный pre-check capability membership;
- status `PROTECTED_BY_CAPABILITY_MATURITY`;
- запрет `MERGE`, `REMOVE`, Collapse, Value Conservation, Necessity Removal, Owner Elimination, Function Elimination для незавершенных Capability;
- правило обработки unknown capability mapping через обычный `Implementation Candidate Instance`;
- Engineering Report Lifecycle fields;
- Current Program State storage contract fields.

В `docs/reference/V7_CANONICAL_REFERENCE.md` добавлено короткое durable rule:

```text
Capability Maturity Protection Law
```

SYSTEM_MAP не обновлялся, потому что новый owner не создан.

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` не обновлялся, потому что в этой работе не возник конкретный volatile protected element.

## Как OMP Защищает Незавершенные Capability

Перед любой минимизацией OMP обязан определить:

```text
Element
  -> Capability membership
  -> Capability name
  -> Capability status
  -> Completion / Certification / Lock / Terminal Consumer
  -> Minimizability decision
```

Если элемент принадлежит Capability со статусом `Idea`, `Need Identified`, `Creation Justified`, `Implemented`, `Integrated`, `Necessity Verified`, `IN_PROGRESS`, `OPEN`, `PARTIAL`, `BLOCKED`, `BROKEN` или любым незавершенным эквивалентом, OMP возвращает:

```text
PROTECTED_BY_CAPABILITY_MATURITY
```

После этого Necessity minimization для элемента должна остановиться.

## Почему Незавершенная Функция Больше Не Может Быть Удалена

Отсутствие downstream value у элемента теперь не является достаточным основанием для `MERGE` или `REMOVE`, если элемент принадлежит незавершенной Capability.

OMP обязан сначала доказать, что Capability достигла одного из существующих terminal states:

- `COMPLETE`;
- `Capability Certified`;
- `LOCKED`;
- `Capability Locked`;
- `Capability Retired`;
- другой legal terminal consumer из Capability Management.

До этого момента отсутствие downstream value может означать не ненужность элемента, а незавершенность Capability.

## Unknown Capability Mapping

Если OMP не может определить, принадлежит ли элемент Capability, минимизация запрещена.

Тогда OMP использует существующий путь:

```text
Capability mapping unknown
  -> BDP candidate production when discovery is required
  -> OMP candidate consumption
  -> Mission Admission
  -> mapping correction / hold / rejection / not applicable
  -> verification
  -> Engineering Report
```

Новый Candidate type не создается.

## Почему Новая Программа Не Понадобилась

Защита выражается существующими owners:

- Capability Management owns capability state;
- Necessity Framework owns existence / merge / removal tests;
- OMP owns execution decision and Mission admission;
- BDP owns candidate production when discovery/mapping correction is required;
- SYSTEM_MAP owns owner mapping;
- CPS owns volatile current state;
- Engineering Reports own evidence.

Новый Protection Engine или Capability Engine создал бы дублирующий lifecycle owner и нарушил бы No Duplication / Architecture Closed by Default.

## Certification

| Review | Verdict | Evidence |
| --- | --- | --- |
| Reuse Review | `PASS` | Переиспользованы Capability Management, Necessity Framework, OMP, BDP, SYSTEM_MAP, CPS. |
| Capability Protection Review | `PASS` | Незавершенные Capability получают `PROTECTED_BY_CAPABILITY_MATURITY`. |
| Necessity Review | `PASS` | Necessity не отменена; она заблокирована только до maturity-ready состояния Capability. |
| Lifecycle Review | `PASS` | Новый lifecycle не создан; используются existing Capability statuses и legal terminal consumers. |
| Architecture Review | `PASS` | Новая архитектура, owner, Planner, Runtime, Engine, graph, queue или программа не созданы. |
| No Duplication Review | `PASS` | Protection является OMP pre-check, а не отдельной системой. |
| OMP Review | `PASS` | Правило встроено в Necessity Framework Consumption и Engineering Report Lifecycle. |
| Quality Review | `PASS` | Указаны triggers, protected status, forbidden actions, unknown mapping path и terminal conditions. |
| Self Review | `PASS` | Scope соблюден; обновлены только OMP, короткое canonical rule и engineering report. |

## Final Verdict

`PASS`

После этой правки ни один механизм Necessity, Merge, Remove, Value Conservation или архитектурной минимизации не может изменить или удалить элемент, если Capability, к которой он относится, еще не завершена.
