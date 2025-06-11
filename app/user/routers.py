from fastapi import APIRouter, Depends, Request

from typing import List

from app.user.auth import get_current_user
from app.user.dao import UserDAO
from app.user.models import User
from app.user.schemas import UserProfileResponseSchema

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


@router.api_route("/me", methods=["GET", "POST"], response_model=UserMeResponse)
async def get_or_post_my_profile(
    request: Request,
):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return {"result": "false", "user": None}

    user = await UserDAO.get_user_by_api_key(session, api_key)
    if not user:
        return {"result": "false", "user": None}

    return {
        "result": "true",
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": f.follower.id, "name": f.follower.name}
                for f in user.followers
            ],
            "following": [
                {"id": f.followed.id, "name": f.followed.name}
                for f in user.following
            ],
        },
    }

@router.get("/me/following")
async def get_following(user: User = Depends(get_current_user)):
    return [{"id": f.followed.id, "name": f.followed.name} for f in user.following]

@router.get("/me/followers")
async def get_followers(user: User = Depends(get_current_user)):
    return [{"id": f.follower.id, "name": f.follower.name} for f in user.followers]