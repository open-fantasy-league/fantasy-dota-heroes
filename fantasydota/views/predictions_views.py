from fantasydota.lib.constants import DEFAULT_LEAGUE
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper


@view_config(route_name='predictions', renderer='../templates/predictions.mako')
def predictions(request):
    session = DBSession()
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))
    user_id = authenticated_userid(request)
    try:
        period = int(request.params.get("period", 1))
    except ValueError:
        print("Got invalid period param: %s" % request.params.get("period"))
        period = 0
    return_dict = {'period': period, 'league_id': league_id}
    return all_view_wrapper(return_dict, session, user_id)
