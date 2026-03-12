from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Float, nullable=False)
    body_fat = Column(Float, nullable=True)
    date = Column(Date, default=lambda: datetime.now(timezone.utc).date())

    user = relationship("User", back_populates="progress_logs")
