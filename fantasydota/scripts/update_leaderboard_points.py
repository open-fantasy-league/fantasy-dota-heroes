import random

import transaction
from fantasydota.lib.battlecup import FakePlayer
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, Battlecup, LeagueUser, League, LeagueUserDay, \
    BattlecupUserRound, BattlecupRound, TeamHero
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func


def add_result_to_user(userq, res, hero_count):
    username = userq.username
    if "p" in res:
        userq.picks += 1
    if "w" in res:
        userq.wins += 1
    if "b" in res:
        userq.bans += 1
    to_add = (0.5 ** (5 - hero_count)) * Result.result_to_value(res)
    print "addin %s points to %s" % (to_add, username)
    userq.points += to_add


def update_league_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied.is_(1)). \
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        res = result.result_str
        winners = session.query(TeamHero.user). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id,
                        TeamHero.is_battlecup.is_(False))).all()
        for winner in winners:
            userq = session.query(LeagueUser).filter(and_(LeagueUser.username == winner[0],
                                                          LeagueUser.league == league_id)).first()
            userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.username == userq.username,
                                                            LeagueUserDay.league == userq.league,
                                                            LeagueUserDay.day == league.current_day
                                                                 )).first()
            username = userq.username
            hero_count = session.query(func.count(TeamHero)).filter(and_(TeamHero.league == league_id,
                                                                         TeamHero.user == username,
                                                                         TeamHero.is_battlecup.is_(False))).scalar()
            add_result_to_user(userq, res, hero_count)
            add_result_to_user(userq_day, res, hero_count)

        result.applied = 2


def main():
    session = make_session()
    for league in session.query(League).all():
        with transaction.manager:
            update_league_points(session, league)
            transaction.commit()

if __name__ == "__main__":
    main()
