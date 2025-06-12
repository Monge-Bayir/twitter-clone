import uvicorn
from fastapi import FastAPI
from app.tweet.routers import router as router_tweet
from app.likes.routers import router as router_likes
from app.follower.routers import router as router_follow
from app.media.routers import router as router_media
from app.user.routers import router as router_user
from fastapi.staticfiles import StaticFiles
import pathlib
import os


app = FastAPI()

os.makedirs("uploaded_media", exist_ok=True)

# Добавляем статическую раздачу файлов
app.mount("/uploaded_media", StaticFiles(directory="uploaded_media"), name="uploaded_media")


app.include_router(router_likes)
app.include_router(router_tweet)
app.include_router(router_follow)
app.include_router(router_user)
app.include_router(router_media)

# Абсолютный путь к dist
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"


app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000)