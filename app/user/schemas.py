from pydantic import BaseModel
from typing import List


class UserShort(BaseModel):
    id: int
    name: str

    model_config = {"arbitrary_types_allowed": True}


class UserMe(BaseModel):
    id: int
    name: str
    followers: List[UserShort]
    following: List[UserShort]

    model_config = {"arbitrary_types_allowed": True}


class UserMeResponse(BaseModel):
    result: str
    user: UserMe


class UserCreate(BaseModel):
    name: str
    api_key: str
