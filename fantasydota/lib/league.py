from fantasydota.lib.account import assign_xp_and_weekly_achievements
from fantasydota.models import League, Game


def game_from_league_id(session, league_id):
    game_id = session.query(League.game).filter(League.id == league_id).first()[0]
    return session.query(Game).filter(Game.id == game_id).first()


def in_progress_league(session, game_id):
    return session.query(League).filter(League.status == 1).filter(League.game == game_id).first()


def next_league(session, game_id):
    return session.query(League).filter(League.status == 0).filter(League.game == game_id).first()


def close_league(session, game_id):
    old_league = session.query(League).filter(League.game == game_id).filter(League.status == 1).first()
    old_league.status = 2
    assign_xp_and_weekly_achievements(session, old_league)
