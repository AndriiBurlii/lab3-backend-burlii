# Лабораторна робота №3
## Тема: Розробка REST API з Flask та Docker

**Виконав:** Бурлій Андрій  
**Група:** ІО-32  
**Варіант:** 2 — Користувацькі категорії витрат

---

## Визначення варіанту
Номер групи: **32**  
Розрахунок: **32 mod 3 = 2**  
Висновок: **Варіант №2 — Користувацькі категорії витрат**

### Що реалізовано в межах варіанту
- Підтримка **глобальних** і **користувацьких** категорій.
- Створення користувацьких категорій із заголовком `X-User-Id`.
- Перегляд категорій:
  - без `X-User-Id` → лише глобальні;
  - з `X-User-Id` → глобальні **+** персональні користувача.
- Захист від дублікатів (409 Conflict) і валідація вхідних даних (422).

---

## Мета роботи
Розробити REST API для обліку витрат із використанням **Flask**, **SQLAlchemy**, **PostgreSQL** та **Docker Compose**.  
Реалізувати CRUD для користувачів, категорій і витрат; забезпечити контейнеризований запуск і перевірку через **Postman/curl**.

---

## Використані технології
- Python 3.11 • Flask 3.x • Flask-Smorest  
- SQLAlchemy • Alembic / Flask-Migrate  
- PostgreSQL 16 • Docker Compose  
- Marshmallow (валідація) • Postman / curl

---

## Запуск проєкту

### 1) Середовище (Docker)
```bash
docker-compose up --build
```

Після запуску обидва контейнери працюють коректно.

**Рис. 1. Запущені контейнери у Docker Desktop**  
![Docker Desktop containers](screens/01_docker_desktop_containers.png)

### 2) Міграції БД
```bash
flask --app manage.py db init
flask --app manage.py db migrate -m "initial"
flask --app manage.py db upgrade
```

Створено таблиці: `users`, `categories`, `expenses`.

---

## Перевірка ендпоінтів (мінімальний сценарій)

### Користувачі та категорії
- `GET /health` — 200 OK  
- `POST /api/users` — 201 Created (або 409 Conflict при дублікаті)  
- `POST /api/categories` — 201 Created (або 409 Conflict)  
- `GET /api/categories`  
  - без заголовка — лише глобальні
  - з `X-User-Id` — глобальні + персональні

**Рис. 2. Тестування ендпоінтів користувачів та категорій**  
![Users & Categories API tests](screens/02_api_users_categories_tests.png)

### Витрати
- `POST /api/expenses` — 201 Created  
- `POST /api/expenses` з `amount=0` → 422 Unprocessable Entity (валідація)  
- `GET /api/expenses` — 200 OK

**Рис. 3. Створення витрати та помилка валідації**  
![Expense creation & validation error](screens/03_api_expenses_tests.png)

**Рис. 4. Відповідь `GET /api/expenses`**  
![Expenses list response](screens/04_api_expenses_list.png)

---

## Postman колекція

У репозиторії додано готову колекцію для перевірки:  
**`Lab3_Burlii_IO32_V3.postman_collection.json`**

Запити в колекції:
1. `GET /health`  
2. `POST /api/users`  
3. `POST /api/categories`  
4. `POST /api/expenses`  
5. `GET /api/expenses`

> Для запитів, що залежать від користувача, використовуй заголовок  
> `X-User-Id: {{user_id}}` (можна оголосити змінну середовища в Postman).

---

## Структура проєкту
```
Lab3/
 ├─ app/
 │  ├─ __init__.py
 │  ├─ models.py
 │  ├─ schemas.py
 │  └─ routes/
 │     ├─ users.py
 │     ├─ categories.py
 │     └─ expenses.py
 ├─ migrations/
 ├─ postman/
 ├─ screens/
 │  ├─ 01_docker_desktop_containers.png
 │  ├─ 02_api_users_categories_tests.png
 │  ├─ 03_api_expenses_tests.png
 │  └─ 04_api_expenses_list.png
 ├─ Dockerfile
 ├─ docker-compose.yml
 ├─ manage.py
 ├─ config.py
 ├─ requirements.txt
 ├─ wsgi.py
 └─ README.md
```

---

## Висновок
Зроблено REST API для обліку витрат, реалізовано ORM-моделі, валідацію і обробку помилок, налаштовано Docker-інфраструктуру та міграції. Продемонстровано логіку **варіанту №2 — користувацькі категорії витрат**, підготовлено Postman-колекцію та скріншоти з перевірками. Проєкт відповідає вимогам ЛР-3.
