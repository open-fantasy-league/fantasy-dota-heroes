from fantasydota import DBSession
from fantasydota.models import Friend, LeagueUser, LeagueUserDay, TeamHero, League
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    user = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]

    show_friend = True if request.params.get("showFriend") and user else False
    if show_friend:
        switch_to = "global"
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user == user).all()]
    else:
        switch_to = "friend"
    period = request.params.get("period") or "tournament"

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks", "bans") else "points"

    # should prob move this func
    def rank_filter(rank_by, period):
        userOb = LeagueUser if period == "tournament" else LeagueUserDay
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
        elif rank_by == "bans":
            return userOb.bans
        else:
            return userOb.points

    def period_filter(period):
        try:
            return int(period)
        except:
            return "tournament"

    rank_ = rank_filter(rank_by, period)
    period_ = period_filter(period)

    player_heroes = []
    league = session.query(League).filter(League.id == league_id).first()
    leagueq = session.query(LeagueUser).filter(LeagueUser.league == league_id)
    if period == "tournament":
        user = leagueq.filter(LeagueUser.username == user).first()
        if show_friend:
            players = leagueq.filter(or_(LeagueUser.username.in_(friends), LeagueUser.username == user)).\
                order_by(desc(rank_)).limit(100).all()
        else:
            players = leagueq.order_by(desc(rank_)).limit(100).all()

    else:
        leagueq = session.query(LeagueUserDay).filter(LeagueUserDay.day == period_).filter(LeagueUserDay.league == league_id)
        user = leagueq.filter(LeagueUserDay.username == user).first()
        if show_friend:
            players = leagueq.filter(or_(LeagueUserDay.username.in_(friends), LeagueUserDay.username == user)). \
                order_by(desc(rank_)).limit(100).all()
        else:
            players = leagueq.order_by(desc(rank_)).limit(100).all()

    for player in players:
        heroes = []
        for hero in session.query(TeamHero).filter(and_(TeamHero.user == player.username,
                                                        TeamHero.is_battlecup == False,
                                                        TeamHero.league == league_id)).all():
            heroes.append(hero.hero_name)
        player_heroes.append(heroes)

    return {'user': user, 'players': players, 'rank_by': rank_by, 'switch_to': switch_to, 'period': period,
            'player_heroes': player_heroes, 'league': league}