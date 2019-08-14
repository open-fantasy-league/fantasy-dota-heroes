import re
import urllib2

import json
from fantasydota.lib.constants import API_URL
from fantasydota.local_settings import FANTASY_API_KEY
from fantasydota.models import User, Team
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper, get_league_id


@view_config(route_name='view_team', renderer='../templates/team.mako')
def view_team(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
    team_name_q = session.query(Team.name).filter(Team.league_id == league_id).filter(Team.user_id == user_id).first()
    if team_name_q:
        team_name = team_name_q[0]
    else:
        usernameq = session.query(User.username).filter(User.id == user_id).first()
        if usernameq:
            team_name = usernameq[0]
        else:
            team_name = ""
    return_dict = {'league_id': league_id, 'team_name': team_name}

    return_dict = all_view_wrapper(request, return_dict, session, user_id)
    return return_dict


@view_config(route_name='transfer_proxy', renderer='json')
def transfer_proxy(request):
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
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


@view_config(route_name='update_team_name', renderer='json')
def update_team_name(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
    new_name = request.json_body.get('name')
    if len(new_name) < 3:
        data = {"success": False, "msg": "Team name must be > 3 characters"}
        return Response(json_body=data, status=400)
    if len(new_name) > 20:
        data = {"success": False, "msg": "Team name must be <= 20 characters"}
        return Response(json_body=data, status=400)
    if not re.match("(?i)^[0-9a-zA-Z ]+$", new_name):
        data = {"success": False, "msg": "Team name can only contain letters, numbers and spaces"}
        return Response(json_body=data, status=400)
    else:
        teamq = session.query(Team).filter(Team.league_id == league_id).filter(Team.user_id == user_id)
        existing_name = session.query(Team).filter(Team.league_id == league_id).filter(Team.name == new_name)
        if existing_name.first():
            data = {"success": False, "msg": "Team name already taken. please choose unique one"}
            return Response(json_body=data, status=400, content_type="application/json")
        else:
            if teamq.first():
                teamq.update({Team.name: new_name})
            else:
                team = Team(user_id, league_id, new_name)
                session.add(team)
            data = {"success": True, "team_name": new_name}
            url = API_URL + "users/" + str(user_id) + "/leagues/" + str(league_id)
            req = urllib2.Request(
                url,  data=json.dumps({'username': new_name}), headers={
                    'apiKey': FANTASY_API_KEY,
                    'User-Agent': 'fantasy-dota-frontend',
                    "Content-Type": "application/json"
                }
            )

            response = urllib2.urlopen(req).read()
            print(response)
            return Response(json_body=data, status=200, content_type="application/json")


@view_config(route_name='new_card_pack', renderer='json')
def new_card_pack(request):
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
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
        return Response(json_body={'success': True, 'msg': json.loads(response.read())})
    except urllib2.HTTPError as e:
        return Response(json_body={'success': False, 'msg': e.read()}, status=e.code, content_type="application/json")
    except Exception as e:
        return Response(json_body={'success': False, 'msg': e.message}, status=500)


@view_config(route_name='recycle_card', renderer='json')
def recycle_card(request):
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
    url = API_URL + "transfers/leagues/" + str(league_id) + "/users/" + str(user_id) + "/recycleCard/" + str(request.POST.get('cardId'))
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
        return Response(text, status=e.code, content_type="application/json")
    except Exception as e:
        return Response(e.message, status=500)


@view_config(route_name='recycle_cards', renderer='json')
def recycle_cards(request):
    user_id = authenticated_userid(request)
    league_id = get_league_id(request)
    url = API_URL + "transfers/leagues/" + str(league_id) + "/users/" + str(user_id) + "/recycleCards"
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
        return Response(text, status=e.code, content_type="application/json")
    except Exception as e:
        return Response(e.message, status=500)
