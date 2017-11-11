import time
import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import LeagueUser, TeamHero


def make_swaps():
    with transaction.manager:
        session = make_session()
        for luser in session.query(LeagueUser).filter(LeagueUser.swap_tstamp < time.time()).all():
            for thero in session.query(TeamHero).filter(TeamHero.user_id == luser.user_id)\
             .filter(TeamHero.league == luser.league).filter(TeamHero.active != TeamHero.reserve).all():
                thero.active = thero.reserve

        transaction.commit()

if __name__ == "__main__":
    make_swaps()
