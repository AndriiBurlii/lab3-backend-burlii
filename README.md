
# Лабораторна робота 3 — Валідація, обробка помилок, ORM

**Дисципліна:** Технології серверного ПЗ  
**Проєкт:** Expenses API (Flask + SQLAlchemy)  
**Група:** 32 → `32 % 3 = 2` ⇒ **Варіант: Користувацькі категорії витрат**

## Визначення варіанту
Остача від ділення номера групи (**32**) на 3 дорівнює **2**, отже реалізовано варіант **"Користувацькі категорії витрат"**. Тут передбачено **загальні** категорії (видимі для всіх) та **користувацькі** (видимі лише власнику).

## Стек
- Flask, flask-smorest (OpenAPI, валідація)
- SQLAlchemy, Flask‑Migrate (ORM + міграції)
- PostgreSQL (docker-compose)
- Marshmallow (схеми, валідація)

## Швидкий старт (локально)
1. **Python 3.12**, створіть та активуйте віртуальне середовище.
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустіть Postgres через docker:
   ```bash
   docker-compose up -d db
   ```
4. Створіть/оновіть БД:
   ```bash
   export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/expenses
   flask --app manage.py db init || true
   flask --app manage.py db migrate -m "initial"
   flask --app manage.py db upgrade
   ```
5. Запустіть API:
   ```bash
   python wsgi.py
   # healthcheck: http://localhost:5000/health
   ```

## Швидкий старт (Docker, повністю)
```bash
docker-compose up --build
# API: http://localhost:5000
```

## Ендпоінти (урізано)
- `POST /api/users` — створення користувача: `{ "email": "u@example.com" }`  
- `GET /api/users` — список користувачів
- `POST /api/categories` — створення категорії  
  - Загальна (для всіх): тіло `{ "name": "Food", "is_global": true }`
  - Користувацька: заголовок `X-User-Id: <id>` і тіло `{ "name": "MyCat" }`
- `GET /api/categories` — список категорій (якщо задано `X-User-Id`, повертає глобальні + власні; інакше лише глобальні)
- `POST /api/expenses` — створення витрати:
  ```json
  { "user_id": 1, "category_id": 2, "amount": "123.45", "description": "Lunch" }
  ```
- `GET /api/expenses` — список витрат

## Валідація та обробка помилок
- Валідація Marshmallow (мінімальні довжини, діапазони, формати email).
- 400 — невірні дані; 404 — не знайдено; 409 — конфлікт (дублікати категорій/користувачів).

## Міграції
- `flask --app manage.py db init` (перший запуск)
- `flask --app manage.py db migrate -m "<msg>"`
- `flask --app manage.py db upgrade`

## Postman
Колекція та environment у каталозі `postman/`. Імпортуйте обидва файли:
- Set env var `baseUrl` = `http://localhost:5000`
- У запитах на категорії для користувацьких категорій додайте заголовок `X-User-Id`.

## Git теги (приклад)
```bash
git tag v2.0.0 -a -m "Lab 3"
git push --tags
```

---

**Примітка:** Конфігурація (URI БД, секрети) зчитується з `config.py`/змінних середовища. Деталі завдання, критерії і методичні рекомендації виконано згідно файлу з умовою.
