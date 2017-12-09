from fantasydota.models import Game, Notification, League
from sqlalchemy import desc


def add_other_games(return_dict, session, game_code):
    other_games = session.query(Game).filter(Game.code != game_code).all()
    return_dict['other_games'] = other_games
    return return_dict


def add_leagues_to_view(return_dict, session, game_code):
    leagues = session.query(League).filter(Game.code == game_code).order_by(desc(League.id)).all()
    return_dict['leagues'] = leagues
    return return_dict


def add_notifications(return_dict, session, user_id):
    notifications = session.query(Notification).filter(Notification.user == user_id).filter(Notification.seen.is_(False)).all()
    return_dict['notifications'] = notifications
    return return_dict


def all_view_wrapper(return_dict, session, game_code, user_id):
    if user_id:
        return_dict = add_notifications(return_dict, session, user_id)
    else:
        return_dict['notifications'] = []
    return_dict = add_leagues_to_view(return_dict, session, game_code)
    return add_other_games(return_dict, session, game_code)


def get_game(request):
    return request.cookies.get('game', 'DOTA')


def get_league(request):
    return request.cookies.get('league', 1)


def match_link(match_id):
    return 'https://stratz.com/match/%s' % match_id