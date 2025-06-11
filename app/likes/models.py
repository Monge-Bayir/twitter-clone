from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    tweet = relationship("Tweet", back_populates="likes")
    user = relationship("User", back_populates="likes")

    __table_args__ = (UniqueConstraint('tweet_id', 'user_id', name='_tweet_user_like_uc'),)