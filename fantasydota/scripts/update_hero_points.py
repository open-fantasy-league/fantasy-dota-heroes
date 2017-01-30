import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, League
from sqlalchemy import and_


def update_hero_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied.is_(False)).\
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        res = result.result_str
        # More than one because we have battlecup and league
        heroq_all = session.query(Hero).filter(and_(Hero.id == result.hero,
                                                Hero.league == league_id)).all()
        # if not heroq_all:  # temp for no underlord
        #     continue  # TODO remove!!!
        for heroq in heroq_all:
            print result.match_id
            print "Hero id: ", result.hero
            if "p" in res:
                heroq.picks += 1
            if "w" in res:
                heroq.wins += 1
            if "b" in res:
                heroq.bans += 1
            print "Would add %s to hero points", Result.result_to_value(res)
            heroq.points += Result.result_to_value(res)
        result.applied = 1


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            update_hero_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
