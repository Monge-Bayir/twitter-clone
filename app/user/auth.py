from fastapi import Depends, Header, HTTPException, status
from app.user.dao import UserDAO
from app.user.models import User

async def get_current_user(x_api_key: str = Header(...)) -> User:
    user = await UserDAO.find_by_api_key(x_api_key)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key"
        )
    return user


from fastapi import Header, HTTPException, Depends

async def get_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing x-api-key header")
    return x_api_key