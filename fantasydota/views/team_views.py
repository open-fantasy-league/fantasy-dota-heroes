import traceback
import urllib2

import json
from fantasydota.lib.constants import DEFAULT_LEAGUE, API_URL
from fantasydota.local_settings import FANTASY_API_KEY
from fantasydota.models import User
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPInternalServerError
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper


@view_config(route_name='view_team', renderer='../templates/team.mako')
def view_team(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return_dict = {'league_id': int(request.params.get('league', DEFAULT_LEAGUE))}

    return_dict = all_view_wrapper(return_dict, session, user_id)
    return return_dict


@view_config(route_name='transfer_proxy', renderer='json')
def transfer_proxy(request):
    user_id = authenticated_userid(request)
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))
    in_ = request.POST
    print(in_.getall('buy[]'))
    print(in_)
    out = {'buy': in_.getall('buy[]'), 'sell': in_.getall('sell[]'),
           'isCheck': in_.get('isCheck'), 'wildcard': in_.get('wildcard', False)}
    url = API_URL + "transfers/leagues/" + str(league_id) + "/users/" + str(user_id)
    try:
        req = urllib2.Request(
            url, data=json.dumps(out), headers={
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


@view_config(route_name='new_card_pack', renderer='json')
def new_card_pack(request):
    user_id = authenticated_userid(request)
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))
    url = API_URL + "transfers/leagues/" + str(league_id) + "/users/" + str(user_id) + "/newPack"
    try:
        req = urllib2.Request(
            url, data="", headers={
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
    except Exception as e:
        text = traceback.print_exc()
        return Response(e.message, status=500)