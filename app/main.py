from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import pathlib

# Импортируем роутеры (замените на ваши реальные роутеры)
from app.tweet.routers import router as router_tweet
from app.likes.routers import router as router_likes
from app.follower.routers import router as router_follow
from app.media.routers import router as router_media
from app.user.routers import router as router_user

# Инициализация приложения с явным указанием путей к документации
app = FastAPI(
    title="Twitter Clone API",
    description="API для Twitter Clone",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Подключаем роутеры
app.include_router(router_likes)
app.include_router(router_tweet)
app.include_router(router_follow)
app.include_router(router_user)
app.include_router(router_media)

# Создаем директорию для медиафайлов если её нет
MEDIA_DIR = "uploaded_media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Монтируем директорию с медиафайлами
app.mount(
    "/media",
    StaticFiles(directory=MEDIA_DIR),
    name="media"
)

# Путь к собранному фронтенду
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend" / "dist"

# Монтируем статический фронтенд последним
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
