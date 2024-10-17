from pydantic import BaseModel
from typing import List, Optional


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    points: int
    attempts: int
    games_played: int
    games_won: int
    points_per_attempt: List[int]
    def __init__(self, **data):
        super().__init__(**data)
        print('FLAG01')
        print(self.max_points)
    class Config:
        orm_mode = True


class UpdatePointsResponse(BaseModel):
    message: str
    player: Player


class MaxPoints(BaseModel):
    max_points: int


class PlayerStatistics(BaseModel):
    total_games: int
    total_attempts: int
    max_points_in_game: Optional[int] = None
    total_wins: int
    win_percentage: float

    class Config:
        orm_mode = True
