from app.dao.base import BaseDao
from app.database import async_session_maker
from app.follower.models import Follower
from app.tweet.models import Tweet
from sqlalchemy import select
from app.media.models import Media


class TweetDAO(BaseDao):
    model = Tweet

    @classmethod
    async def create(cls, content: str, author_id: int, media_ids: list[int] = None):
        async with async_session_maker() as session:
            tweet = Tweet(content=content, author_id=author_id)
            session.add(tweet)
            await session.flush()

            if media_ids:
                result = await session.execute(select(Media).where(Media.id.in_(media_ids)))
                medias = result.scalars().all()
                for media in medias:
                    media.tweet_id = tweet.id

            await session.commit()
            await session.refresh(tweet)
            return tweet

    @classmethod
    async def delete(cls, tweet_id: int, author_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(cls.model.id == tweet_id, cls.model.author_id == author_id)
            )
            tweet = result.scalar_one_or_none()
            if tweet:
                await session.delete(tweet)
                await session.commit()
                return True
            return False

    @classmethod
    async def get_feed_for_user(cls, user_id: int):
        async with async_session_maker() as session:
            # Получаем ID пользователей, на которых подписан user_id
            result = await session.execute(
                select(Follower.following_id).where(Follower.follower_id == user_id)
            )
            following_ids = [r[0] for r in result.all()]
            following_ids.append(user_id)  # Включаем свои твиты

            # Получаем твиты этих пользователей
            result = await session.execute(
                select(Tweet)
                .where(Tweet.author_id.in_(following_ids))
                .order_by(Tweet.created_at.desc())
                .limit(50)
            )
            tweets = result.scalars().all()

            # Преобразуем твиты в dict с вложенными авторами и лайками
            feed = []
            for tweet in tweets:
                attachments = [media.file_path for media in tweet.medias]  # предполагаем связь tweet.medias
                likes = [{"user_id": like.user.id, "name": like.user.name} for like in tweet.likes]
                feed.append({
                    "id": tweet.id,
                    "content": tweet.content,
                    "attachments": attachments,
                    "author": {"id": tweet.author.id, "name": tweet.author.name},
                    "likes": likes
                })
            return feed