from fastapi import APIRouter, Depends, Request, Header

from typing import List, Annotated, Optional

from app.user.auth import get_current_user
from app.user.dao import UserDAO
from app.user.models import User
from app.user.schemas import UserCreate

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
            'followers': [{'id': x.id, 'name': x.name} for x in user.followers],
            'following': [{'id': x.id, 'name': x.name} for x in user.following]
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
            'followers': [{'id': x.id, 'name': x.name} for x in user.followers],
            'following': [{'id': x.id, 'name': x.name} for x in user.following]
        }
    }
    return data
