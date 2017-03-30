from sqlalchemy import and_

from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero


def start_of_day():
    session = make_session(transaction=False, autoflush=False)
    for league in session.query(League).all():  # .filter(League.status == 1)
        session.query(TeamHero).filter(and_(
                                            TeamHero.league == league.id,
                                            )).update({TeamHero.active: True})
        session.query(League).filter(League.id == league.id).update({
            League.transfer_open: 0
        })
        league.transfer_open = False  # close league window if not already closed
    session.commit()


def main():
    start_of_day()

if __name__ == "__main__":
    main()
