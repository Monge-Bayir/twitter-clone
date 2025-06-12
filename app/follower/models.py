from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    followed = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers"
    )

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="_follower_followed_uc"),
    )
