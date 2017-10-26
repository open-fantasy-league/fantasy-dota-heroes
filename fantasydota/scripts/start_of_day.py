from fantasydota.lib.session_utils import make_session
from fantasydota.lib.trade import reset_incomplete_teams
from fantasydota.models import League


def start_of_day():
    session = make_session(transaction=False, autoflush=False)
    for league in session.query(League).all():  # .filter(League.status == 1)
        league.transfer_open = False  # close league window if not already closed
        league.swap_open = False
        if league.current_day > 0:
            reset_incomplete_teams(session, league)
    session.commit()


def main():
    start_of_day()

if __name__ == "__main__":
    main()
