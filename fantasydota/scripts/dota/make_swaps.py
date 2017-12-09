import time
import transaction
from fantasydota.lib.account import team_swap_all
from fantasydota.lib.session_utils import make_session
from fantasydota.models import LeagueUser, TeamHero


def make_swaps():
    with transaction.manager:
        session = make_session()
        team_swap_all(session, 1)
        transaction.commit()

if __name__ == "__main__":
    make_swaps()
