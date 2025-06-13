# 🐦 Twitter Clone

Полноценный клон Twitter на FastAPI с авторизацией, лайками, подписками, медиа и PostgreSQL.

## 📦 Стек

- ⚙️ FastAPI + SQLAlchemy
- 🐘 PostgreSQL
- 🐳 Docker + Docker Compose
- 🖼 Nginx (frontend + media)
- 💡 Alembic (миграции)
- 🌐 HTML/CSS/JS (без фреймворков)

---

## 🚀 Запуск проекта

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Monge-Bayir/twitter-clone.git
cd twitter-clone
```
### 2. Заполни .env
```env

DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres

SECRET_KEY=sjKZ2cvr4cPVh7ooGcqgJEpLEvxIsSEHgPcRWMXn/Hs=
ALGORITHM=HS256
```

## 3. Собери и запусти
```bash
docker-compose up --build
```
🔗 Frontend: http://localhost

🔗 API: http://localhost/api/...

🔗 Медиа: http://localhost/media/...

## 🗃 Миграции (alembic)
```bash
docker exec -it backend alembic revision --autogenerate -m "message"
docker exec -it backend alembic upgrade head
```

### 📁 Структура
app/ — бэкенд-логика

frontend/dist/ — собранный HTML/CSS/JS

uploaded_media/ — директория с медиафайлами

nginx.conf — конфигурация прокси

docker-compose.yaml — все сервисы

### ⚠️ Примечания
FastAPI ожидает .env, иначе не поднимется подключение к БД.

Убедись, что Docker Desktop работает
