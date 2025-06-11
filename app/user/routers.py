

from fastapi import APIRouter, Depends, Request, Header

from typing import List, Annotated, Optional

from app.user.auth import get_current_user
from app.user.dao import UserDAO
from app.user.models import User
from app.user.schemas import UserCreate

router = APIRouter(prefix="/api/users", tags=["Users"])


# @router.get("/users/me", response_model=UserProfileResponseSchema)
# async def get_my_profile(current_user=Depends(get_current_user)):
#     user = await UserDAO.get_user_profile(current_user.id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     return {
#         "result": "true",
#         "user": user
#     }


@router.post('/me')
async def create_user(name: str, api_key: str):
    user = await UserDAO.create(name, api_key)
    return {
        'user': user.name,
        'api_key': user.api_key
    }

@router.get('/me')
async def get_user_me(api_key: Annotated[Optional[str], Header()] = None):
    user = await UserDAO.get_user_by_api_key(api_key)
    data = {
        'result': 'true',
        'user': {
            'id': user.id,
            'name': user.name,
            'followers': [{'id': x.id, 'name': x.name} for x in user.followers],
            'following': [{'id': x.id, 'name': x.name} for x in user.following]
        }
    }
    return data

@router.get("/me/following")
async def get_following(user: User = Depends(get_current_user)):
    return [{"id": f.followed.id, "name": f.followed.name} for f in user.following]

@router.get("/me/followers")
async def get_followers(user: User = Depends(get_current_user)):
    return [{"id": f.follower.id, "name": f.follower.name} for f in user.followers]