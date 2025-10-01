# Wordstat Top Requests CLI

Небольшой CLI-скрипт, который запрашивает эндпоинт `topRequests` API Яндекс.Wordstat и возвращает результаты в формате JSON.

Документация по подключению и получению токена: https://yandex.ru/support2/wordstat/ru/content/api-wordstat

## Быстрый старт

```bash
cd python/wordstat
cp .env.example .env        # добавьте токен в WORDSTAT_API_KEY
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wordstat_top_requests.py "продвижение сайта" "контекстная реклама"
```

## Аргументы

- позиционные аргументы — фразы для проверки;
- `--env` — путь к `.env` (по умолчанию `.env`). Передайте `--env ""`, если токен уже есть в переменных окружения.

Результат — единый JSON-объект с ключами-фразами. Ошибки сетевых запросов и ответа сервера сохраняются рядом в объекте `error`.

## Формат ответа Wordstat

Сырые данные возвращаются без постобработки. В разных тарифах структура может меняться, поэтому удобно хранить весь JSON и разбирать его в своих пайплайнах отдельно.
