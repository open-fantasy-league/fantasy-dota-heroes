from fantasydota.models import Game


def add_other_games(session, game_code, return_dict):
    other_games = session.query(Game).filter(Game.code != game_code).all()
    return_dict['other_games'] = other_games
    return return_dict


def get_game(request):
    return request.cookies.get('game', 'DOTA')
