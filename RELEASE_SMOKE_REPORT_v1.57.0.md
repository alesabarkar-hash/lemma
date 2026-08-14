# Release smoke report — LEMMA v1.57.0

Дата проверки: 14 августа 2026.

## База и интеграция

- актуальная production-база перед сборкой: `47c779e`;
- принятые этапы перенесены поверх production без пересборки контента;
- release branch: `release/lemma-v1.57.0`;
- Pages-compatible URL локальной проверки: `/lemma/`;
- app version: `1.57.0`.

## Автоматический прогон

Результат: **126/126 проверок пройдено**.

Проверены viewport `390×844` и `1366×768`, маршруты Main → Path → Topic,
Hello L1/L2 и Family L2 до Result с возвратом на Path, вход в учебник Hello
и Family с контекстным возвратом, точный SAVED/resume, последовательные locks
внутри Hello и для всех десяти тем, первая награда и повтор без повторного
начисления.

Representative rendering выполнен для всех десяти тем:
Hello, Alphabet 1, Alphabet 2, Alphabet 3, Review 1, Family, Colours, Home,
Birthday и Review 2.

## Технические критерии

| Критерий | Результат |
|---|---:|
| JavaScript errors | 0 |
| horizontal overflow | 0 |
| broken/missing images | 0 |
| legacy illustrations visible | 0 |
| legacy flash | 0 |
| внешние запросы | 0 |
| HTTP errors / failed requests | 0 |
| GitHub Pages subpath assets | загружаются |
| Manrope | локальные WOFF2, загружаются |

SAVED/resume восстановил точное состояние `family_l2 / practice / step 3`
вместе со score и mistakes. После первого завершения Hello L1 награда была
начислена; повторное завершение сохранило прежний баланс. После L1 открылся
L2, после L2 — Check. Все десять тем показали реальную последовательность
`done → current → locked`.

## Дополнительная правка по результату smoke

На mobile Главной декоративный псевдоэлемент hero расширял документ до
`460 px` при viewport `390 px`. Область свечения ограничена свойством
`overflow-x: clip`; композиция, содержимое и функциональная логика не менялись.
После исправления весь прогон повторён с нуля: document width `390/390`.

После публикации выполняется отдельный live smoke реального GitHub Pages,
включая прямое открытие, reload, версию, ассеты, навигацию и production-
скриншоты.
