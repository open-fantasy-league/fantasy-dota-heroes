import transaction

from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import League
from fantasyesport.scripts.update_hero_points import update_hero_points
from fantasyesport.scripts.update_leaderboard_points import update_league_points
from fantasyesport.scripts.update_user_rankings import update_user_rankings


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
