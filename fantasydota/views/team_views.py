from fantasydota.lib.constants import DEFAULT_LEAGUE
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper


@view_config(route_name='view_team', renderer='../templates/team.mako')
def view_team(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))

    return_dict = {'user_id': user_id, 'league_id': league_id}

    return_dict = all_view_wrapper(return_dict, session, request)
    print(return_dict)
    return return_dict

