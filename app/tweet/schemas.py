from typing import Optional, List

from pydantic import BaseModel



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


class LikeInfo(BaseModel):
    user_id: int
    name: str

class AuthorInfo(BaseModel):
    id: int
    name: str

class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: AuthorInfo
    likes: List[LikeInfo] = []

class TweetListResponse(BaseModel):
    result: bool
    tweets: Optional[List[TweetResponse]] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
