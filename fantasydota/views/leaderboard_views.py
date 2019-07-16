from fantasydota.lib.constants import DEFAULT_LEAGUE
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper
from fantasydota.models import Friend


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    mode = request.params.get("mode", "global")
    try:
        period = int(request.params.get("period", 0))
    except ValueError:
        print("Got invalid period param: %s" % request.params.get("period"))
        period = 0
    if mode == "friend" and not user_id:
        mode = "global"
    other_modes = ['global', 'friend'] # , 'hero']
    other_modes.remove(mode)
    friends = []
    if mode == "friend" and user_id:
        friends = [int(kek[0]) for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        friends.append(int(user_id))

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    return_dict = {'rank_by': rank_by, 'mode': mode, 'other_modes': other_modes, 'period': period, 'friends': friends}
    return all_view_wrapper(request, return_dict, session, user_id)
