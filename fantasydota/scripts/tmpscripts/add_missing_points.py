import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import LeagueUser, Result, Game, LeagueUserDay, League
from fantasydota.scripts.update_leaderboard_points import add_results_to_user
from sqlalchemy import and_


def add_missing_points():
    fix_ts = 1515536315
    session = make_session()
    with transaction.manager:
        league_id = 2
        league = session.query(League).filter(League.id == league_id).first()
        for userq in session.query(LeagueUser).filter(LeagueUser.league == 2).filter(LeagueUser.late_start == 2).all():
            print(userq.username)
            """new_results = session.query(Result).filter(Result.applied == 2). \
                filter(Result.tournament_id == league_id).filter(Result.timestamp < 1515536315).filter(Result.start_tstamp > userq.late_start_tstamp).all()

            team_size = session.query(Game.team_size).filter(Game.id == league.game).first()[0]
            game = 1
            userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.user_id == userq.user_id,
                                                                 LeagueUserDay.league == userq.league,
                                                                 LeagueUserDay.day == league.current_day
                                                                 )).first()
            add_results_to_user(session, userq, userq_day, new_results, league, team_size, game)

            for res in new_results:
                res.applied = 2
            """

        transaction.commit()
    return

if __name__ == "__main__":
    add_missing_points()
