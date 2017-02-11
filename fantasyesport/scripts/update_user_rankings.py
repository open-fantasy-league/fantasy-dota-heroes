import transaction
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import League, LeagueUser, LeagueUserDay
from sqlalchemy import and_
from sqlalchemy import desc


def set_user_rankings(session, user_leagues, day):
    # But is there a better way??
    user_leagues.sort(key=lambda x: x.wins, reverse=True)
    for i, user in enumerate(user_leagues):
        user.wins_rank = i + 1

    user_leagues.sort(key=lambda x: x.points, reverse=True)
    for i, user in enumerate(user_leagues):
        user.points_rank = i + 1
        session.query(LeagueUserDay).filter(and_(LeagueUserDay.league_user == user.id,
                                                         LeagueUserDay.day == day)).update({
            LeagueUserDay.cumulative_points_rank: i+1
        })

    user_leagues.sort(key=lambda x: x.picks, reverse=True)
    for i, user in enumerate(user_leagues):
        user.picks_rank = i + 1

    return


def set_user_day_rankings(session, user_league, day):
    user_league_days = session.query(LeagueUserDay).\
        filter(and_(LeagueUserDay.league_user.in_([x.id for x in user_league]),
                    LeagueUserDay.day == day)).all()
    # But is there a better way??
    user_league_days.sort(key=lambda x: x.wins, reverse=True)
    for i, user in enumerate(user_league_days):
        user.wins_rank = i + 1

    user_league_days.sort(key=lambda x: x.points, reverse=True)
    for i, user in enumerate(user_league_days):
        user.points_rank = i + 1

    user_league_days.sort(key=lambda x: x.picks, reverse=True)
    for i, user in enumerate(user_league_days):
        user.picks_rank = i + 1

    return


def update_user_rankings(session, league):
    with transaction.manager:
        league_users = session.query(LeagueUser).filter(LeagueUser.league == league.id).all()
        set_user_day_rankings(session, league_users, league.current_day)
        set_user_rankings(session, league_users, league.current_day)
        transaction.commit()


def main():
    session = make_session()
    for league in session.query(League).all():
        update_user_rankings(session, league)

if __name__ == "__main__":
    main()
