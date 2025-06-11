from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)

    tweet = relationship("Tweet", back_populates="media")

    def __repr__(self):
        return f"<Media {self.id} for Tweet {self.tweet_id}>"