from sqlalchemy import Column, Integer, String, PickleType
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    points = Column(Integer, default=301)
    attempts = Column(Integer, default=0)
    points_per_attempt = Column(PickleType, default=[])