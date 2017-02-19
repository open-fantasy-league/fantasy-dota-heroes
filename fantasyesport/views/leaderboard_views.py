from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import desc

from fantasyesport import DBSession
from fantasyesport.models import Friend, LeagueUser, LeagueUserDay, League, User, TeamHero


@view_config(route_name='leaderboard', renderer='../templates/leaderboard.mako')
def leaderboard(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]
    show_friend = True if request.params.get("showFriend") and user_id else False
    users_playing = [x[0] for x in session.query(User.id).all()]
    if show_friend:
        switch_to = "global"
        friends = [kek[0] for kek in session.query(Friend.friend).filter(Friend.user_id == user_id).all()]
        if user_id:
            friends.append(user_id)
    else:
        switch_to = "friend"
    period = request.params.get("period") or "tournament"

    rank_by = request.params.get("rank_by")
    rank_by = rank_by if rank_by in ("points", "wins", "picks") else "points"

    # should prob move this func
    def rank_filter(rank_by, period):
        userOb = LeagueUser if period == "tournament" else LeagueUserDay
        if rank_by == "wins":
            return userOb.wins
        elif rank_by == "picks":
            return userOb.picks
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
    if show_friend:
        user_filter = friends
    else:
        user_filter = users_playing
    leagueq = session.query(LeagueUser, LeagueUserDay, LeagueUser.user_id).filter(LeagueUser.league == league_id). \
        filter(LeagueUser.user_id.in_(user_filter))

    luser = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.user_id == user_id).first()
    if period == "tournament":
        last_day = league.current_day - 1 if league.current_day != 0 else league.current_day
        players = leagueq.filter(LeagueUserDay.day == last_day).order_by(desc(rank_)).join(LeagueUserDay).\
            limit(100).all()
        # If we dont only take one league user day we have too many entries.
        # this is only day needed for up/down arrow of progress
    else:
        leagueq = session.query(LeagueUser.username, LeagueUserDay, LeagueUser.user_id).filter(LeagueUserDay.day == period_).\
            filter(LeagueUserDay.league_user.in_([x[0].id for x in leagueq.all()]))
        players = leagueq.order_by(desc(rank_)).join(LeagueUserDay).limit(100).all()
        # If we dont only take one league user day we have too many entries.
        # this is only day needed for up/down arrow of progress

        luser = session.query(LeagueUser.username, LeagueUserDay, LeagueUser.user_id).filter(LeagueUserDay.day == period_).\
            filter(LeagueUserDay.league_user == luser.id).join(LeagueUserDay).first()

    for player in players:
        heroes = []
        print player[0], player[1], player[2]
        for hero in session.query(TeamHero).filter(and_(TeamHero.user_id == player[2],
                                                        TeamHero.is_battlecup.is_(False),
                                                        TeamHero.league == league_id)).all():
            heroes.append(hero.hero_name)
        player_heroes.append(heroes)

    return {'user': luser, 'players': players, 'rank_by': rank_by, 'switch_to': switch_to, 'period': period,
            'player_heroes': player_heroes, 'league': league}
