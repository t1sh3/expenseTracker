# Expense Tracker API

REST API для учёта личных расходов с JWT-авторизацией, категориями и фильтрацией трат.

## Стек
- **Backend:** FastAPI, Pydantic v2
- **Database:** PostgreSQL, SQLAlchemy 2.0, Alembic
- **Auth:** JWT (`PyJWT`), хеширование паролей (`pwdlib[argon2]`)

## Функционал
- Регистрация, вход и получение профиля (`/auth/register`, `/auth/login`, `/auth/me`)
- CRUD для категорий расходов (`/categories/`)
- CRUD для трат с фильтрацией по категории и диапазону дат (`/expenses/`)
- Изоляция данных: каждый пользователь имеет доступ только к своим записям

## Локальный запуск

1. Клонировать репозиторий и установить зависимости:
   ```bash
   git clone [https://github.com/t1sh3/expenseTracker.git](https://github.com/t1sh3/expenseTracker.git)
   cd expenseTracker
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Создать базу данных `expense_tracker` в PostgreSQL (через pgAdmin или в терминале через `psql`):
   ```sql
   CREATE DATABASE expense_tracker;
   ```

3. Скопировать файл с примером переменных окружения:
   - **Windows:**
     ```powershell
     copy .env.example .env
     ```
   - **Linux / macOS:**
     ```bash
     cp .env.example .env
     ```

4. Открыть созданный `.env` и заполнить свои значения:
   - `DATABASE_URL` — строка подключения к PostgreSQL (логин, пароль, хост и порт).
   - `SECRET_KEY` — любая длинная случайная строка для подписи JWT-токенов (можно сгенерировать командой `python -c "import secrets; print(secrets.token_hex(32))"`).

5. Применить миграции базы данных:
   ```bash
   alembic upgrade head
   ```

6. Запустить сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

Документация Swagger UI будет доступна по адресу: `http://127.0.0.1:8000/docs`