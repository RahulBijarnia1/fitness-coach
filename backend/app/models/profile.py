from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)  # male / female
    height = Column(Float, nullable=False)     # in cm
    weight = Column(Float, nullable=False)     # in kg
    body_fat = Column(Float, nullable=True)    # percentage, optional

    user = relationship("User", back_populates="profile")
