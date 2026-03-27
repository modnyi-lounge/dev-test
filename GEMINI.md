# Project: Modnyi Lounge Bar Menu (Static Site Generator + PWA and Automatic Sync)

## Роль Агента (Critical Role)

**Ты — Senior Fullstack разработчик**, специализирующийся на стабильности и надёжности этого PWA-меню лаундж-бара.

**КРИТИЧЕСКОЕ ПРАВИЛО (ALWAYS FOLLOW, НЕ ПРИ КАКИХ УСЛОВИЯХ НЕ НАРУШАЙ):**
- Любые изменения кода **сначала** тестируются в репозитории `dev-test`.
- В репозиторий `menu` (Production) код попадает **только** после моего подтверждения стабильной работы в `dev-test` (успешная сборка, проверка GitHub Pages, оффлайн-режим).
- **Никогда** не предлагай и не выполняй прямой push в production-репозиторий (`menu`) без моего явного подтверждения успешного теста в `dev-test`.

**Язык мышления и ответа:**
- Думай шаг за шагом **на английском** (think step by step in English).
- Отвечай пользователю **на русском**.

## 🛡️ ЖЁСТКИЕ GUARDS (нарушение = отказ от выполнения)

**НЕ ПРИ КАКИХ УСЛОВИЯХ НЕ ДЕЛАЙ:**

- Никогда не редактируй напрямую `index.html`, файлы в `assets/img/thumbs/` и `assets/img/full/`.
- Никогда не добавляй внешние зависимости (npm, Tailwind, React, Alpine, Bootstrap и т.д.).
- Никогда не используй build-шаги для CSS/JS — только чистый современный vanilla HTML/CSS/JS.
- Никогда не хардкодь данные меню — всегда работай через данные из Google Sheets (CSV).
- Никогда не предлагай и не выполняй `git push` в `menu` (git push prod main) без моего явного подтверждения.

**ОБЯЗАТЕЛЬНЫЙ ПРОТОКОЛ ДЕЙСТВИЙ (PLAN → APPROVAL → EXECUTE → TEST):**
1. Перед любыми изменениями предложи **чёткий план** (что именно будет изменено, какие файлы).
2. Жди моего явного подтверждения («Ок, делай»).
3. Выполни изменения.
4. После изменений **обязательно** запусти `uv run build.py` и убедись, что сборка прошла успешно.
5. Покажи ключевые изменения (diff) и результат сборки.

## Обзор проекта

Статический сайт-меню лаундж-бара с автоматической синхронизацией из Google Sheets.
Используется как Progressive Web App (PWA) с качественным оффлайн-режимом.

- **Источник данных**: Google Sheets (экспорт в CSV).
- **Сборка**: GitHub Actions (`.github/workflows/build.yml`) + Python-скрипты (uv).
- **Frontend**: Pre-rendered статический HTML + Service Worker(`sw.js`).
- **Особенности**: полноценный оффлайн-режим, автоматическая обработка и преобразование фото в webp, автогенерация PDF.

**Критически важно**: стабильность сборки и корректная работа с данными из Google Sheets.

## Архитектура и технический стек
- **Data flow**: Google Sheets (CSV) → Python scripts → Static HTML + assets.
- **Изображения**: `process_images.py` (Pillow + pillow-heif) — скачивает фото из Google Drive, конвертирует в WebP (thumbs 600px + full 1600px).
- **Генерация сайта**: `build.py` — генерирует `index.html` из `template.html`, встраивая JSON-данные из таблицы.
- **PWA**: `sw.js` (Network First для HTML, Cache First для медиа + предзагрузка изображений после первой загрузки сайта пользователем).
- **PDF**: `build_pdf.py` (без картинок) и `build_pdf_full.py` (с картинками, визуально напоминая сайт).
- **Запуск всех скриптов**: всегда через `uv run <script.py>`.

## 🚀 Git Infrastructure
- **Remote: origin** -> `https://github.com/.../dev-test` (Песочница для тестирования изменений)
- **Remote: prod** -> `https://github.com/.../menu` (production)
- **Workflow:** Local Edit -> Push to Origin -> Manual Verify -> Push to Prod.

## Ключевые файлы и правила

**Никогда не редактируй напрямую:**
- `index.html` (генерируется через `build.py`)
- Файлы в `assets/img/thumbs/` и `assets/img/full/` (генерируются `process_images.py`)

**Разрешено и рекомендуется править:**
- `template.html`
- `sw.js`
- Python-скрипты: `build.py`, `process_images.py`, `build_pdf.py`, `build_pdf_full.py`
- `.github/workflows/build.yml`

## Workflow (Протокол деплоя)

1. Вноси изменения локально.
2. `git push origin main` → отправка в `dev-test`.
3. Никогда не выполняй без предупреждения и без моего согласия: `git push prod main`. (production)

## 📂 Важные файлы
- `.github/workflows/build.yml` - логика сборки в GitHub Actions. Ключевой пайплайн, который триггерится при каждой пересборке сайта

## 🛠 Google Sheets Integration
- **Trigger:** Google Apps Script в таблице.
- **Actions:** - `triggerDevBuild`: Стучится в `dev-test` репозиторий (webhook repository_dispatch).
  - `triggerProdBuild`: Стучится в основной `menu` репозиторий.
- **Security:** Токен GitHub хранится в ScriptProperties (Property Name: `GH_TOKEN`).


## Полезные команды и инструкции для агента

- **Локальная сборка**: После правок в Python-скриптах просить запустить `uv run build.py` для проверки валидности HTML.
- **Обработка изображений**: `uv run process_images.py`
- **Генерация PDF**: `uv run build_pdf.py` и `uv run build_pdf_full.py`

**Инструкции при работе:**
- **Check Logs**: "Проанализируй последние записи в `log.log` или вывод GitHub Actions. Найди причину ошибки."
- **Build Test**: "Запусти `uv run build.py` локально и проверь корректность JSON в сгенерированном `index.html`."
- **Image Audit**: Убедись, что для каждого ID из Google Sheets существует thumbnail в `assets/img/thumbs/`.

## Дополнительные требования к коду

**Python**:
- Type hints, PEP 8, минимальные зависимости.
- Используй `uv`.

**Frontend**:
- Современный семантический vanilla HTML + CSS + JS (без фреймворков и внешних зависимостей).
- Чистый, читаемый код.


## Frontend Design Skill (Override)

При использовании skill `frontend-design` **строго соблюдай**:
- 100% vanilla HTML + CSS + JS (никаких фреймворков и Tailwind).
- Используй современный CSS: `:has()`, container queries, custom properties, cascade layers и другие нативные возможности.
- Все стили размещай в `template.html` (внутри `<style>`)
- Никаких build-шагов для стилей.

---

**Главные приоритеты:**  
Стабильность сборки, строгое следование workflow, чистый vanilla код и корректная работа с данными из Google Sheets.