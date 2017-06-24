from fantasydota.lib.herolist import heroes as herolist
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.models import Friend, LeagueUser, LeagueUserDay, TeamHero, League, Match, Result, TeamHeroHistoric


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]
    users_playing = [x[0] for x in session.query(TeamHero.user_id).filter(TeamHero.league == league_id).group_by(TeamHero.user_id).all()]
    show_friend = True if request.params.get("showFriend") and user_id else False
    if show_friend:
        switch_to = "global"
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)
    else:
        switch_to = "friend"

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    # should prob move this func
    def rank_filter(rank_by):
        userOb = LeagueUser
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    rank_ = rank_filter(rank_by)

    player_heroes = []
    league = session.query(League).filter(League.id == league_id).first()
    leagueq = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.user_id.in_(users_playing))
    luser = leagueq.filter(LeagueUser.user_id == user_id).first()
    if show_friend:
        players = leagueq.filter(LeagueUser.user_id.in_(friends)).\
            order_by(desc(rank_)).limit(100).all()
    else:
        players = leagueq.order_by(desc(rank_)).order_by(desc(LeagueUser.points)).order_by(desc(LeagueUser.wins)).limit(100).all()

    for player in players:
        heroes = []
        if league.transfer_open:
            for hero in session.query(TeamHeroHistoric).filter(
                    and_(TeamHeroHistoric.user_id == player.user_id, TeamHeroHistoric.league == league_id)).\
                    filter(TeamHeroHistoric.day == league.current_day - 1).all():
                heroes.append(hero.hero_name)
        else:
            for hero in session.query(TeamHero).filter(and_(TeamHero.user_id == player.user_id,
                                                            TeamHero.league == league_id)).all():
                heroes.append(hero.hero_name)
        player_heroes.append(heroes)

    return {'user': luser, 'players': players, 'rank_by': rank_by, 'switch_to': switch_to, 'period': "tournament",
            'player_heroes': player_heroes, 'league': league}


@view_config(route_name='daily', renderer='../templates/daily.mako')
def daily(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]
    league = session.query(League).filter(League.id == league_id).first()
    show_friend = True if request.params.get("showFriend") and user_id else False
    if show_friend:
        switch_to = "global"
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)
    else:
        switch_to = "friend"
    period = int(request.params.get("period") or
                 (league.current_day if not league.transfer_open else league.current_day - 1))

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    # should prob move this func
    def rank_filter(rank_by):
        userOb = LeagueUserDay
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    rank_ = rank_filter(rank_by)

    player_heroes = []
    leagueq = session.query(LeagueUserDay).filter(LeagueUserDay.day == period).filter(LeagueUserDay.league == league_id)
    luser = leagueq.filter(LeagueUserDay.user_id == user_id).first()
    if show_friend:
        players = leagueq.filter(or_(LeagueUserDay.user_id.in_(friends), LeagueUserDay.user_id == user_id)). \
            order_by(desc(rank_)).limit(100).all()
    else:
        players = leagueq.order_by(desc(rank_)).limit(100).all()

    for player in players:
        heroes = []
        if period == league.current_day:
            for hero in session.query(TeamHero).filter(
                    and_(TeamHero.user_id == player.user_id, TeamHero.league == league_id)).all():
                heroes.append(hero.hero_name)
        else:
            for hero in session.query(TeamHeroHistoric).filter(
                    and_(TeamHeroHistoric.user_id == player.user_id, TeamHeroHistoric.league == league_id)).\
                    filter(TeamHeroHistoric.day == period).all():
                heroes.append(hero.hero_name)
        player_heroes.append(heroes)

    match_data = []
    matches = session.query(Match).filter(Match.day == period).all()
    for match in reversed(matches):  # we want to show most recent matches at the top
        match_dict = {
            "radiant": match.radiant_team, "dire": match.dire_team, "radiant_win": match.radiant_win,
            "match_id": match.match_id, "radiant_bans": [], "dire_bans": [], "radiant_picks": [],
            "dire_picks": []
        }
        for result in session.query(Result).filter(Result.match_id == match.match_id).all():
            result_entry = {"hero": [h["name"] for h in herolist if h["id"] == result.hero][0],
                            "points": Result.result_to_value(result.result_str)
                            }
            if result.is_radiant:
                if result.result_str[0] == "p":
                    match_dict["radiant_picks"].append(result_entry)
                else:
                    match_dict["radiant_bans"].append(result_entry)
            else:
                if result.result_str[0] == "p":
                    match_dict["dire_picks"].append(result_entry)
                else:
                    match_dict["dire_bans"].append(result_entry)
        match_data.append(match_dict)
    return {'user': luser, 'players': players, 'rank_by': rank_by, 'switch_to': switch_to, 'period': period,
            'player_heroes': player_heroes, 'league': league, 'match_data': match_data}


@view_config(route_name='matches', renderer='json')
def matches(request):
    session = DBSession()
    day = request.POST.get("day")
    data = []
    matches = session.query(Match).filter(Match.day == day).all()
    for match in matches:
        match_dict = {
            "radiant": match.radiant_team, "dire": match.dire_team, "radiant_win": match.radiant_win,
            "match_id": match.match_id, "radiant_bans": [], "dire_bans": [], "radiant_picks": [],
            "dire_picks": []
        }
        for result in session.query(Result).filter(Result.match_id == match.match_id).all():
            result_entry = {"hero": [h["name"] for h in herolist if h["id"] == result.hero][0],
                            "points": Result.result_to_value(result.result_str)
                            }
            if result.is_radiant:
                if result.result_str[0] == "p":
                    match_dict["radiant_picks"].append(result_entry)
                else:
                    match_dict["radiant_bans"].append(result_entry)
            else:
                if result.result_str[0] == "p":
                    match_dict["dire_picks"].append(result_entry)
                else:
                    match_dict["dire_bans"].append(result_entry)
        data.append(match_dict)
    return data
