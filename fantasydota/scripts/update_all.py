import argparse
import transaction
from fantasydota.lib.account import team_swap_all
from fantasydota.scripts.update_user_rankings import update_user_rankings

from fantasydota.scripts.update_leaderboard_points import update_league_points

from fantasydota.scripts.update_hero_points import update_hero_points

from fantasydota.models import League

from fantasydota.lib.session_utils import make_session


def update_all(session=None):
    session = session or make_session()
    #parser = argparse.ArgumentParser()
    #parser.add_argument("league", type=int, help="league id")
    #args = parser.parse_args()
    league = session.query(League).filter(League.status == 1).first()
    with transaction.manager:
        print "Updating hero points"
        update_hero_points(session, league)
        transaction.commit()
    with transaction.manager:
        print "Updating league points"
        team_swap_all(session, league.id)
        session.flush()
        update_league_points(session, league)
        transaction.commit()
    with transaction.manager:
        print "Updating user rankings"
        update_user_rankings(session, league)
        transaction.commit()

if __name__ == "__main__":
    update_all()
