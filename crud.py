from sqlalchemy.orm import Session
from models import Player
from schemas import PlayerCreate

def get_player(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

def get_players(db: Session):
    return db.query(Player).all()

def create_player(db: Session, player: PlayerCreate, max_points: int):
    db_player = Player(name=player.name, points=max_points, attempts=0, points_per_attempt=[])
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def update_player_points(db: Session, player_id: int, points: int):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        if player.points - points < 0:
            return None  # игнор
        player.points -= points
        player.attempts += 1
        player.points_per_attempt.append(points)
        db.commit()
        db.refresh(player)
        return player
    return None

def reset_players(db: Session, max_points: int):
    players = db.query(Player).all()
    for player in players:
        player.points = max_points
        print('TSRTT', max_points)
        player.attempts = 0
        player.points_per_attempt = []
    db.commit()

def delete_player(db: Session, player_id: int):
    db.query(Player).filter(Player.id == player_id).delete()
    db.commit()