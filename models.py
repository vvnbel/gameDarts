from sqlalchemy import Column, Integer, String, PickleType, CLOB, Float, ForeignKey, Boolean
from database import Base
import json
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship


class JSONEncodedList(TypeDecorator):
    impl = CLOB  # CLOB для хранения JSON

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'  # Пустой список в виде JSON
        return json.dumps(value)  # Сериализация списка в JSON

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)  # Десериализация JSON в список


class Player(Base):
    __tablename__ = "darts_players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    points = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    points_per_attempt = Column(JSONEncodedList, default=[])
    # points_per_attempt = Column(String)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    is_active = Column(Integer, default=1)

    # statistics = relationship("PlayerStatistics", back_populates="player")
    statistics = relationship("PlayerStatistics", back_populates="player", uselist=False)

class PlayerStatistics(Base):
    __tablename__ = "player_statistics"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('darts_players.id'), nullable=False)
    total_games = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    max_points_in_game = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_games_updated = Column(Boolean, default=False)

    player = relationship("Player", back_populates="statistics")