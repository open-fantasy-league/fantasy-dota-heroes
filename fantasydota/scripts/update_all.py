import transaction
from fantasydota.scripts.update_user_rankings import update_user_rankings

from fantasydota.scripts.update_leaderboard_points import update_league_points

from fantasydota.scripts.update_hero_points import update_hero_points

from fantasydota.models import League

from fantasydota.lib.session_utils import make_session


def main():
    session = make_session()
    with transaction.manager:
        print "Updating hero points"
        for league in session.query(League).all():
            update_hero_points(session, league)
        transaction.commit()
    with transaction.manager:
        print "Updating league points"
        for league in session.query(League).all():
            update_league_points(session, league)
        transaction.commit()
    with transaction.manager:
        print "Updating user rankings"
        for league in session.query(League).all():
            update_user_rankings(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
