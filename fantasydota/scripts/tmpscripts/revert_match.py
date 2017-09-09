import transaction
from fantasydota.scripts.update_user_rankings import update_user_rankings
from sqlalchemy import func

from fantasydota.lib.session_utils import make_session
from sqlalchemy import and_

from fantasydota.lib.constants import MULTIPLIER
from fantasydota.models import Result, Hero, League, TeamHero, LeagueUser, LeagueUserDay


def revert_hero_points(session, league_id, results):

    for i, result in enumerate(results):
        res = result.result_str

        heroq_all = session.query(Hero).filter(and_(Hero.id == result.hero,
                                                Hero.league == league_id)).all()

        for heroq in heroq_all:
            print result.match_id
            print "Hero id: ", result.hero
            if "p" in res:
                heroq.picks -= 1
            if "w" in res:
                heroq.wins -= 1
            if "b" in res:
                heroq.bans -= 1
            print "Would remove %s to hero points", Result.result_to_value(res)
            heroq.points -= MULTIPLIER * Result.result_to_value(res)


def remove_result_to_user(userq, res, hero_count):
    user_id = userq.user_id
    if "p" in res:
        userq.picks -= 1
    if "w" in res:
        userq.wins -= 1
    if "b" in res:
        userq.bans -= 1
    to_add = MULTIPLIER * ((0.5 ** (5 - hero_count)) * Result.result_to_value(res))
    print "removing %s points to %s" % (to_add, user_id)
    userq.points -= to_add


def revert_league_points(session, league_id, results):
    league = session.query(League).filter(League.id == league_id).first()

    for i, result in enumerate(results):
        res = result.result_str
        winners = session.query(TeamHero.user_id). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id)).all()
        for winner in winners:
            userq = session.query(LeagueUser).filter(and_(LeagueUser.user_id == winner[0],
                                                          LeagueUser.league == league_id)).first()
            user_id = userq.user_id
            userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.user_id == user_id,
                                                            LeagueUserDay.league == userq.league,
                                                            LeagueUserDay.day == league.current_day
                                                                 )).first()
            hero_count = session.query(func.count(TeamHero)).filter(and_(TeamHero.league == league_id,
                                                                         TeamHero.user_id == user_id)).scalar()

            remove_result_to_user(userq, res, hero_count)
            remove_result_to_user(userq_day, res, hero_count)


def main():
    league_id = 5401
    match_id = 3368387319
    with transaction.manager:
        session = make_session()
        league = session.query(League).filter(League.id == league_id).first()
        results = session.query(Result).filter(Result.match_id == match_id).all()
        #revert_hero_points(session, league_id, results)
        #revert_league_points(session, league_id, results)
        update_user_rankings(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
