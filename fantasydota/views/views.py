import datetime

from fantasydota.models import (
    DBSession,
    Friend)
from fantasydota.util.random_function import add_months, bprint
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden)
from pyramid.security import (
    authenticated_userid)
from pyramid.view import (
    view_config,
)
from sqlalchemy import and_


@view_config(route_name='view_faq', renderer='../templates/faq.mako')
def view_faq(request):
    return {}


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    return {}


@view_config(route_name='view_index')
def view_index(request):
    return HTTPFound("/viewLeague")


# @view_config(route_name='battlecup_json', renderer='json')
# def battlecup_json(request):
#     session = DBSession()
#     battlecup_round = session.query(Battlecup.last_completed_round).first()[0]
#     battlecup_id = request.params.get("battlecup_id")
#     battlecup = session.query(BattlecupUserPoints).filter(and_(BattlecupUserPoints.battlecup_id == battlecup_id,
#                                                                BattlecupUserPoints.date > 100)).\
#         order_by(BattlecupUserPoints.username).order_by(BattlecupUserPoints.series_id).all()
#
#     player_q = session.query(BattlecupUser).filter(BattlecupUser.battlecup_id == battlecup_id).\
#         group_by(BattlecupUser.username).order_by(BattlecupUser.username)
#
#     player_names, hero_imgs = [], []
#
#     class FakePlayer(object):
#         def __init__(self):
#             self.username = None
#             self.points = -9000
#
#     fake_player = FakePlayer()
#     # Hack to have a bye for the missing 8th player
#
#     num_players = player_q.count()
#
#     if battlecup_round <= 1:
#         results = []
#         players = player_q.all()
#         if num_players == 7:
#             players.append(fake_player)
#         for i in range(0, len(players), 2):
#             pname1, pname2 = players[i].username.title(), players[i+1].username.title()
#             player_names.append([pname1, pname2])
#
#             hero_ids = [res[0] for res in
#                         session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i].username,
#                                                                  TeamHero.active == True)).all()]
#             player1_heronames = {"pname": pname1,
#                                  "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in hero_ids
#                                             ]}
#             hero_ids = [res[0] for res in
#                         session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i+1].username,
#                                                                  TeamHero.active == True)).all()]
#             player2_heronames = {"pname": pname2,
#                                  "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in
#                                             hero_ids
#                                             ]}
#             hero_imgs.extend([player1_heronames, player2_heronames])
#
#     else:
#         players = [[],[],[],[],[],[],[],[]]
#         for i, pres in enumerate(battlecup):
#             print i, pres
#             players[i/(len(battlecup) / num_players)].append(pres)
#
#         if num_players == 7:
#             players[7] = [fake_player]
#
#         round_zero_points, round_one_points, round_two_points = [], [], []
#
#         if battlecup_round > 1:
#             for i in range(0, len(players), 2):
#                 player1, player2 = players[i][0], players[i+1][0]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 round_zero_points.append([p1_points, p2_points])
#
#                 pname1, pname2 = players[i][0].username.title(), players[i+1][0].username.title()
#                 player_names.append([pname1, pname2])
#
#                 hero_ids = [res[0] for res in session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i][0].username),
#                                                                                        TeamHero.active == True).all()]
#                 player1_heronames = {"pname": pname1,
#                                      "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in hero_ids
#                                      ]}
#                 hero_ids = [res[0] for res in
#                             session.query(TeamHero.hero).filter(and_(TeamHero.user == players[i+1][0].username),
#                                                                 TeamHero.active == True).all()]
#                 player2_heronames = {"pname": pname2,
#                                      "heroes": [hDict["name"].replace(" ", "_") for hDict in heroes_init if hDict["id"] in
#                                                 hero_ids
#                                      ]}
#                 hero_imgs.extend([player1_heronames, player2_heronames])
#
#         if battlecup_round > 2:
#             next_round_players = fight(players, 0)[0]
#             for i in range(0, len(next_round_players), 2):
#                 player1, player2 = next_round_players[i][1], next_round_players[i + 1][1]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 round_one_points.append([p1_points, p2_points])
#
#         if battlecup_round > 3:
#             next_round_players, third_place_playoffs = fight(next_round_players, 1)
#             for i in range(0, len(next_round_players), 2):
#                 player1, player2 = next_round_players[i][2], next_round_players[i + 1][2]
#                 player3, player4 = third_place_playoffs[i][2], third_place_playoffs[i + 1][2]
#                 p1_points, p2_points = check_winner_exists(session, player1, player2)
#                 p3_points, p4_points = check_winner_exists(session, player3, player4)
#                 round_two_points.append([p1_points, p2_points])
#                 round_two_points.append([p3_points, p4_points])
#
#         results = []
#         if battlecup_round > 0:
#             results.append(round_zero_points)
#         if battlecup_round > 1:
#             results.append(round_one_points)
#         if battlecup_round > 2:
#             results.append(round_two_points)
#
#     bracket_dict = {
#         "teams": player_names,
#         "results": results
#     }
#
#     return {"bracket_dict": bracket_dict, "hero_imgs": hero_imgs}


@view_config(route_name="add_friend", renderer="json")
def add_friend(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    new_friend = request.POST["newFriend"].lower()
    if session.query(Friend).filter(and_(Friend.user == user, Friend.friend == new_friend)).first():
        return {"success": False, "message": "You have already added that friend"}
    else:
        session.add(Friend(user, new_friend))
        return {"success": True, "message": "Friend successfully added"}


@view_config(route_name="switch_transfers", renderer="string")
def switch_transfers(request):
    change = request.params.get("state")
    if request.remote_addr not in ('127.0.0.1', '149.210.217.128'):
        raise HTTPForbidden()
    bprint(request.remote_addr)
    if change == 'open':
        request.registry.settings.update({"transfers": True})
        return "transfer window opened"
    elif change == 'closed':
        request.registry.settings.update({"transfers": False})
        return "transfer window closed"
    else:
        return "incorrect state param"


@view_config(route_name="news", renderer="../templates/news.mako")
def news(request):
    return {}


@view_config(route_name="hall_of_fame", renderer="../templates/hall_of_fame.mako")
def hall_of_fame(request):
    return {}

def get_time_range(time_range):
    if time_range == 'week':
        date_start = datetime.datetime.now() - datetime.timedelta(days=7)
        date_end = datetime.datetime.now()
    elif time_range == 'month':
        date_start = add_months(datetime.datetime.now(), -1)
        date_end = datetime.datetime.now()
    else:
        date_start = datetime.datetime(2015, 11, 1)
        date_end = datetime.datetime.now()
    return date_start, date_end
