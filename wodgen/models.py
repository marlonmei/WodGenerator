from sqlalchemy import Column, Integer, String, Numeric, Enum

from database import Base
from type import WorkoutType

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    time = Column(Numeric(100, 2))
    type = Column(Enum(WorkoutType))
    description = Column(String)
