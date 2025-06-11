from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

from app.likes.models import Like
from app.user.models import User


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = []
    model_config = {
        "arbitrary_types_allowed": True
    }

class TweetCreatedResponse(BaseModel):
    result: bool
    tweet_id: int
    model_config = {
        "arbitrary_types_allowed": True
    }

class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: User
    likes: List[Like] = []
    model_config = {
        "arbitrary_types_allowed": True
    }


class TweetListResponse(BaseModel):
    result: bool
    tweets: List[TweetResponse]
    model_config = {
        "arbitrary_types_allowed": True
    }