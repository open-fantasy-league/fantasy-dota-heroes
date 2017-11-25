import argparse

import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero, TeamHeroHistoric


def store_todays_teams(session, league):
    for th in session.query(TeamHero).filter(TeamHero.league == league.id).filter(TeamHero.reserve.is_(False)).all():
        day = league.current_day
        session.add(TeamHeroHistoric(th.user_id, th.hero_id, th.league, th.cost, day, hero_name=th.hero_name))


def end_of_day(league_id=None):
    with transaction.manager:
        session = make_session()
        if not league_id:
            parser = argparse.ArgumentParser()
            parser.add_argument("league", type=int, help="league id")
            args = parser.parse_args()
            league_id = args.league
        league = session.query(League).filter(League.id == league_id).first()
        store_todays_teams(session, league)

        league.current_day += 1
        league.swap_open = True
        transaction.commit()

if __name__ == "__main__":
    end_of_day()
