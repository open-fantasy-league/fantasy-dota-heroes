import transaction
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import Hero, Result, League
from sqlalchemy import and_


def update_hero_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied == 0).\
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        # More than one because we have battlecup and league
        heroq_all = session.query(Hero).filter(and_(Hero.id == result.hero,
                                                    Hero.league == league_id)).all()
        for heroq in heroq_all:
            heroq.picks += 1
            if result.win:
                heroq.wins += 1
                if result.set_ == 3:
                    heroq.points += 1
                elif result.set_ == 5:
                    heroq.points += 3
                else:
                    heroq.points += 2
        result.applied = 1


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            update_hero_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
