from fantasydota.lib.constants import DEFAULT_LEAGUE
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper
from fantasydota.models import Friend


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))
    user_id = authenticated_userid(request)
    mode = request.params.get("mode", "global")
    period = int(request.params.get("period", 0))
    if mode == "friend" and not user_id:
        mode = "global"
    other_modes = ['global'] #, 'friend', 'hero']
    other_modes.remove(mode)
    if mode == "friend":
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    return_dict = {'rank_by': rank_by, 'mode': mode, 'other_modes': other_modes, 'period': period,
            'league_id': league_id}
    return all_view_wrapper(return_dict, session, user_id)
