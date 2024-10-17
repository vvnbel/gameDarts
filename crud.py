from sqlalchemy.orm import Session, joinedload
from models import Player, PlayerStatistics
from schemas import PlayerCreate

def get_player(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

def get_players(db: Session):
    return db.query(Player).all()




def create_player(db: Session, player: PlayerCreate, max_points: int):

    existing_player = db.query(Player).filter_by(name=player.name).first()

    if existing_player:
        existing_player.is_active = 1
        existing_player.points = max_points
        existing_player.attempts = 0
        existing_player.points_per_attempt = []
        # existing_player.games_played = 0
        existing_player.games_won = 0
        db.add(existing_player)
        db.commit()
        db.refresh(existing_player)
        return existing_player
    new_player = Player(
        name=player.name,
        points=max_points,
        attempts=0,
        points_per_attempt=[],
        games_played=0,
        games_won=0,
        is_active=1
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

def update_player_points(db: Session, player_id: int, points: int):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        if player.points - points < 0:
            return None
        elif player.points - points == 0:
            player.points = 0
            all_players = db.query(Player).filter_by(is_active=True).all()
            for p in all_players:

                if p.id == player.id:  # Не дублируем обновление для победителя
                    update_player_statistics(db, p, points, game_finished=True, update_wins=True)
                    update_player_statistics_after_win(db, p)
                    p.games_played += 1
                    for other_player in all_players:
                        if other_player.id != player.id:
                            other_player.games_played += 1
                            db.commit()
                    break
                else:
                    update_player_statistics(db, p, points, game_finished=True, update_wins=False)
                    print('блок елс для обновления статистики всем')

            db.commit()
            db.refresh(player)
            return player

        player.points -= points
        player.attempts += 1
        player.points_per_attempt.append(points)
        update_player_statistics(db, player, points, game_finished=False, update_wins=False)
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
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        player.is_active = 0
        db.commit()


def get_active_players(db: Session):
    return db.query(Player).filter(Player.is_active == 1).all()


def reset_game_statistics(db: Session):
    players = db.query(Player).all()
    for player in players:
        player.games_played += 1  # Увеличиваем количество игр для каждого игрока
        player.points = player.max_points  # Сбрасываем очки
    db.commit()


def update_player_statistics(db: Session, player: Player, points: int, game_finished: bool, update_wins: bool = False):
    statistics = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player.id).first()

    if statistics:
        # Увеличиваем количество игр только один раз
        if game_finished: #and not statistics.total_games_updated:
            statistics.total_games += 1
            # statistics.total_games_updated = True  # Флаг, чтобы не обновлять игры дважды
        print('total_attempts')
        # Увеличиваем количество попыток только для активного игрока
        statistics.total_attempts += 1

        # Обновляем максимальные очки для каждого игрока индивидуально
        if statistics.max_points_in_game is None or points > statistics.max_points_in_game:
            statistics.max_points_in_game = points
            print('here')

        if update_wins:
            statistics.total_wins += 1  # Увеличиваем количество побед для победителя

        db.commit()

    else:
        # Если записи о статистике игрока еще нет, создаем её

        new_statistics = PlayerStatistics(
            player_id=player.id,
            total_games=1 if game_finished else 0,
            total_attempts=1 if not game_finished else 0,  # Увеличиваем попытки только если игра не завершена
            max_points_in_game=points,
            total_wins=1 if update_wins else 0,
            total_games_updated=game_finished
        )
        print('max_points_in_game', PlayerStatistics.max_points_in_game)
        db.add(new_statistics)
        db.commit()

def update_player_statistics_win(db: Session, player: Player, points: int):
    # Извлекаем статистику игрока
    statistics = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player.id).first()

    if statistics:
        # Увеличиваем количество побед
        statistics.total_wins += 1

        # Обновляем максимальные очки за один раунд ТОЛЬКО для победителя
        if statistics.max_points_in_game is None or points > statistics.max_points_in_game:
            statistics.max_points_in_game = points

        # Обновляем количество игр для победителя
        statistics.total_games += 1

        db.commit()
        db.refresh(statistics)
def update_player_statistics_after_win(db: Session, player: Player):
    statistics = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player.id).first()

    statistics.total_games_updated = False
    print('1', statistics.total_games)
    statistics.total_games -= 1
    statistics.total_attempts -= 1
    print('2', statistics.total_games)

    db.commit()


def get_all_players(db: Session):
    return db.query(Player).options(joinedload(Player.statistics)).all()


'''
def update_player_statistics(db: Session, player: Player):
    stats = db.query(GameStatistics).filter(GameStatistics.player_id == player.id).first()
    if not stats:
        stats = GameStatistics(player_id=player.id, games_played=0, games_won=0)
        db.add(stats)

    stats.games_played += 1
    if player.points == 0:
        stats.games_won += 1

    stats.win_percentage = (stats.games_won / stats.games_played) * 100
    db.commit()
    db.refresh(stats)
    return stats
'''