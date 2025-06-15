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

DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres

SECRET_KEY=<ваш секретный ключ>
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

### Разработка

Запуск только бэкенда (для разработки)

```bash
cd app
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload
```

Сборка фронтенда

Фронтенд уже собран и находится в frontend/dist/. Для разработки:

Откройте frontend/index.html в браузере
Используйте Live Server в VS Code

### ⚠️ Примечания
FastAPI ожидает .env, иначе не поднимется подключение к БД.
Создай через /api/docs, пользователя с api_key = 'test'
Либо http://localhost/api/users/me?name=YOURNAME&api_key=test

Убедись, что Docker Desktop работает

### Авторизация

<img width="1680" alt="Снимок экрана 2025-06-15 в 18 00 44" src="https://github.com/user-attachments/assets/c35c8ceb-c28b-4fd4-a217-9c0f6c2828a9" />
через это окошко идет авторизация через api_key
