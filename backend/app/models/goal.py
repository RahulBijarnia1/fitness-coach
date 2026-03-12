from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    goal_type = Column(String(50), nullable=False)        # cut / bulk / maintain
    activity_level = Column(String(50), nullable=False)    # sedentary / light / moderate / active / very_active
    calorie_target = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)                 # grams
    carbs = Column(Float, nullable=True)                   # grams
    fat = Column(Float, nullable=True)                     # grams

    user = relationship("User", back_populates="goal")
