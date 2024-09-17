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
    points_per_attempt: List[int]

    class Config:
        orm_mode = True


class UpdatePointsResponse(BaseModel):
    message: str
    player: Player


class MaxPoints(BaseModel):
    max_points: int