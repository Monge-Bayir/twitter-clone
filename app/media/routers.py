import shutil

from fastapi import APIRouter, UploadFile, File, Header, HTTPException

from app.database import async_session_maker
from app.media.models import Media
from app.user.dao import UserDAO

router = APIRouter(prefix="/api", tags=["Media"])


@router.post("/medias")
async def upload_media(file: UploadFile = File(...), api_key: str = Header(...)):
    user = await UserDAO.find_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    file_location = f"uploaded_media/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    async with async_session_maker() as session:
        media = Media(file_path=file_location)
        session.add(media)
        await session.commit()
        await session.refresh(media)

    return {"result": True, "media_id": media.id}
