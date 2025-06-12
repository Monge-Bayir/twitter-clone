from fastapi import APIRouter, Header

from typing import Annotated, Optional

from app.user.dao import UserDAO

router = APIRouter(prefix="/api/users", tags=["Users"])

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
            'followers': [{'id': x.follower.id, 'name': x.follower.name} for x in user.followers],
            'following': [{'id': x.followed.id, 'name': x.followed.name} for x in user.following],
        }
    }
    return data


@router.get('/{user_id}')
async def get_user_by_id(user_id: int):
    user = await UserDAO.get_user_by_user_id(user_id)
    data = {
        'result': 'true',
        'user': {
            'id': user.id,
            'name': user.name,
            'followers': [{'id': x.follower.id, 'name': x.follower.name} for x in user.followers],
            'following': [{'id': x.followed.id, 'name': x.followed.name} for x in user.following],
        }
    }
    return data
