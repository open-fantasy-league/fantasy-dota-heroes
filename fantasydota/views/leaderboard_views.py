from collections import namedtuple

from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper
from fantasydota.lib.herolist import heroes as herolist
from fantasydota.models import Friend, LeagueUser, LeagueUserDay, TeamHero, League, Match, Result, TeamHeroHistoric, \
    HeroDay, Hero, Game


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    game_code = request.game
    game = session.query(Game).filter(Game.code == game_code).first()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings[game_code]["default_league"]
    users_playing = [x[0] for x in session.query(TeamHero.user_id).filter(TeamHero.league == league_id).group_by(TeamHero.user_id).all()]
    mode = request.params.get("mode", "global")
    if mode == "friend" and not user_id:
        mode = "global"
    other_modes = ['global', 'friend', 'hero']
    other_modes.remove(mode)
    if mode == "friend":
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    # should prob move this func
    def rank_filter(rank_by, hero=False):
        userOb = LeagueUser if not hero else Hero
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    rank_ = rank_filter(rank_by, (mode == "hero"))

    player_heroes = []
    league = session.query(League).filter(League.id == league_id).first()
    leagueq = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.user_id.in_(users_playing))
    luser = leagueq.filter(LeagueUser.user_id == user_id).first()
    if mode == "friend":
        players = leagueq.filter(or_(LeagueUser.user_id.in_(friends), LeagueUser.user_id == user_id)). \
            order_by(desc(rank_)).limit(100).all()
    elif mode == "hero":
        players = session.query(Hero).filter(Hero.league == league_id).order_by(desc(rank_)).all()
        for i, p in enumerate(players):
            setattr(p, "%s_rank" % rank_by, i + 1)
    else:
        players = leagueq.order_by(desc(rank_)).limit(100).all()

    for player in players:
        if mode == "hero":
            if game_code == "DOTA":
                player_heroes.append([player.username])
            else:
                x = namedtuple('hero', ['team', 'name'])
                player_heroes.append([x(player.team, player.name)])
        else:
            heroes = []
            if league.transfer_open:
                for hero in session.query(TeamHeroHistoric).filter(
                                and_(TeamHeroHistoric.user_id == player.user_id, TeamHeroHistoric.league == league_id)).\
                                filter(TeamHeroHistoric.day == league.current_day - 1).all():
                            heroes.append(hero.hero_name)
            else:
                for hero in session.query(TeamHero).filter(and_(TeamHero.user_id == player.user_id,
                                                                        TeamHero.league == league_id))\
                        .filter(TeamHero.reserve.is_(False)).all():
                            if game_code == 'DOTA':
                                heroes.append(hero.hero_name)
                            elif game_code == 'PUBG':
                                heroes.append(session.query(Hero).filter(Hero.id == hero.hero_id).filter(Hero.league == league.id).first())
            player_heroes.append(heroes)

    return_dict = {'user': luser, 'players': players, 'rank_by': rank_by, 'mode': mode, 'other_modes': other_modes, 'period': "tournament",
            'player_heroes': player_heroes, 'league': league, 'game': game}
    return all_view_wrapper(return_dict, session, game_code, user_id)


@view_config(route_name='daily', renderer='../templates/daily.mako')
def daily(request):
    session = DBSession()
    game_code = request.game
    game = session.query(Game).filter(Game.code == game_code).first()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings[game_code]["default_league"]
    league = session.query(League).filter(League.id == league_id).first()
    mode = request.params.get("mode", "global")
    if mode == "friend" and not user_id:
        mode = "global"
    other_modes = ['global', 'friend', 'hero']
    other_modes.remove(mode)
    if mode == "friend":
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)

    period = int(request.params.get("period") or
                 (league.current_day if not league.transfer_open else league.current_day - 1))

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    # should prob move this func
    def rank_filter(rank_by, hero=False):
        userOb = LeagueUserDay if not hero else HeroDay
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    rank_ = rank_filter(rank_by, (mode == "hero"))

    player_heroes = []
    leagueq = session.query(LeagueUserDay).filter(LeagueUserDay.day == period).filter(LeagueUserDay.league == league_id)
    luser = leagueq.filter(LeagueUserDay.user_id == user_id).first()
    if mode == "friend":
        players = leagueq.filter(or_(LeagueUserDay.user_id.in_(friends), LeagueUserDay.user_id == user_id)). \
            order_by(desc(rank_)).limit(100).all()
    elif mode == "hero":
        players = session.query(HeroDay).filter(HeroDay.day == period).filter(HeroDay.league == league_id).order_by(desc(rank_)).all()
    else:
        players = leagueq.order_by(desc(rank_)).limit(100).all()

    for player in players:
        if mode == "hero":
            if game_code == "DOTA":
                player_heroes.append([player.username])
            else:
                x = namedtuple('hero', ['team', 'name'])
                player_heroes.append([x(player.team, player.name)])
        else:
            heroes = []
            if period == league.current_day:
                for hero in session.query(TeamHero).filter(
                        and_(TeamHero.user_id == player.user_id, TeamHero.league == league_id)).\
                        filter(TeamHero.reserve.is_(False)).all():
                    if game_code == 'DOTA':
                        heroes.append(hero.hero_name)
                    elif game_code == 'PUBG':
                        heroes.append(session.query(Hero).filter(Hero.id == hero.hero_id).filter(
                            Hero.league == league.id).first())
            else:
                for hero in session.query(TeamHeroHistoric).filter(
                        and_(TeamHeroHistoric.user_id == player.user_id, TeamHeroHistoric.league == league_id)).\
                        filter(TeamHeroHistoric.day == period).all():
                    if game_code == 'DOTA':
                        heroes.append(hero.hero_name)
                    elif game_code == 'PUBG':
                        heroes.append(session.query(Hero).filter(Hero.id == hero.hero_id).filter(
                            Hero.league == league.id).first())
            player_heroes.append(heroes)

    match_data = []
    matches = session.query(Match).filter(Match.day == period).all() if game_code == 'DOTA' else []
    for match in reversed(matches):  # we want to show most recent matches at the top
        match_dict = {
            "radiant": match.radiant_team, "dire": match.dire_team, "radiant_win": match.radiant_win,
            "match_id": match.match_id, "radiant_bans": [], "dire_bans": [], "radiant_picks": [],
            "dire_picks": []
        }
        for result in session.query(Result).filter(Result.match_id == match.match_id).all():
            if period < league.stage1_start:
                multiplier = 1
            elif period < league.stage2_start:
                multiplier = 2
            else:
                multiplier = 4
            result_entry = {"hero": [h["name"] for h in herolist if h["id"] == result.hero][0],
                            "points": multiplier * Result.result_to_value(result.result_str)
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
    return_dict = {'user': luser, 'players': players, 'rank_by': rank_by, 'mode': mode, 'period': period, 'game': game,
            'player_heroes': player_heroes, 'league': league, 'match_data': match_data, 'other_modes': other_modes}
    return all_view_wrapper(return_dict, session, game_code, user_id)
