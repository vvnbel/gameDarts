from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from typing import Optional


from database import SessionLocal
import crud, schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return templates.TemplateResponse("index.html", {"request": request, "players": players})

@router.post("/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.create_player(db, player)
    return db_player

@router.get("/players/", response_model=list[schemas.Player])
def read_players(db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return players

@router.post("/players/{player_id}/points", response_model=schemas.UpdatePointsResponse)
def add_points(player_id: int, points: int, db: Session = Depends(get_db)):
    player = crud.update_player_points(db, player_id, points)
    if player:
        if player.points <= 0:
            return {"message": f"Победитель: {player.name}", "player": player}
        return {"message": "Очки обновлены", "player": player}
    raise HTTPException(status_code=404, detail="Player not found")

@router.post("/reset/")
def reset_game(db: Session = Depends(get_db)):
    crud.reset_players(db)
    return {"message": "Результаты сброшены"}

@router.delete("/players/{player_id}/", response_model=schemas.Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    crud.delete_player(db, player_id)
    return player

