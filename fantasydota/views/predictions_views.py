import json
import urllib2
from pyramid.response import Response

from fantasydota.lib.constants import API_URL
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper, get_league_id
from fantasydota.local_settings import FANTASY_API_KEY


@view_config(route_name='predictions', renderer='../templates/predictions.mako')
def predictions(request):
    session = DBSession()
    league_id = get_league_id(request)
    user_id = authenticated_userid(request)
    try:
        period = int(request.params.get("period", 1))
    except ValueError:
        print("Got invalid period param: %s" % request.params.get("period"))
        period = 0
    return_dict = {'period': period, 'league_id': league_id}
    return all_view_wrapper(request, return_dict, session, user_id)


@view_config(route_name='prediction_proxy', renderer='json')
def prediction_proxy(request):
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
    # out = {'buy': in_.getall('buy[]'), 'sell': in_.getall('sell[]'),
    #        'isCheck': in_.get('isCheck'), 'wildcard': in_.get('wildcard', False)}
    url = API_URL + "results/leagues/" + str(league_id) + "/predictions/" + str(user_id)
    try:
        req = urllib2.Request(
            url, data=json.dumps(request.json_body), headers={
                'apiKey': FANTASY_API_KEY,
                'User-Agent': 'fantasy-dota-frontend',
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        text = e.read()
        return Response(text, status=e.code)
