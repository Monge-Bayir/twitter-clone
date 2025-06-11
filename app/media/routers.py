import shutil

from fastapi import APIRouter, UploadFile, File, Depends

from app.database import async_session_maker
from app.media.models import Media
from app.user.auth import get_current_user

router = APIRouter(prefix="/api/medias", tags=["Media"])

@router.post("")
async def upload_media(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    file_location = f"uploaded_media/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    async with async_session_maker() as session:
        media = Media(filename=file.filename)
        session.add(media)
        await session.commit()
        await session.refresh(media)

    return {
        "result": True,
        "media_id": media.id
    }