from fantasydota.models import League, Game


def game_from_league_id(session, league_id):
    game_id = session.query(League.game).filter(League.id == league_id).first()
    return session.query(Game).filter(Game.id == game_id).first()
