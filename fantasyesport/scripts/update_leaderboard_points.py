import random

import transaction
from fantasyesport.lib.battlecup import FakePlayer
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import Hero, Result, Battlecup, LeagueUser, League, LeagueUserDay, \
    BattlecupUserRound, BattlecupRound, TeamHero
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func


def add_result_to_user(userq, res):
    userq.picks += 1
    if res.win:
        userq.wins += 1
        if res.set_ == 3:
            userq.points += 1
        elif res.set_ == 5:
            userq.points += 3
        else:
            userq.points += 2


def update_league_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied == 1). \
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        winners = session.query(TeamHero.user_id). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id,
                        TeamHero.is_battlecup.is_(False))).all()
        for winner in winners:
            userq = session.query(LeagueUser).filter(and_(LeagueUser.user_id == winner[0],
                                                          LeagueUser.league == league_id)).first()
            userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.league_user == userq.id,
                                                            LeagueUserDay.day == league.current_day
                                                                 )).first()
            add_result_to_user(userq, result)
            add_result_to_user(userq_day, result)

        result.applied = 2


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            update_league_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
