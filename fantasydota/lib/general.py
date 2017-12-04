from fantasydota.models import Game, Notification


def add_other_games(session, game_code, return_dict):
    other_games = session.query(Game).filter(Game.code != game_code).all()
    return_dict['other_games'] = other_games
    return return_dict


def add_notifications(return_dict, session, user_id):
    notifications = session.query(Notification).filter(Notification.user == user_id).filter(Notification.seen.is_(False)).all()
    return_dict['notifications'] = notifications
    return return_dict


def all_view_wrapper(return_dict, session, game_code, user_id):
    if user_id:
        return_dict = add_notifications(session, return_dict, user_id)
    return add_other_games(return_dict, session, game_code)


def get_game(request):
    return request.cookies.get('game', 'DOTA')