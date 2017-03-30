import transaction

from fantasydota.lib.hero import recalibrate_hero_values
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).filter(League.status == 1).all():

            recalibrate_hero_values(session, league.id)
            league.current_day += 1
            league.transfer_open = True
        transaction.commit()

if __name__ == "__main__":
    main()
