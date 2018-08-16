import transaction

from fantasydota.lib.hero import recalibrate_hero_values
from fantasydota.lib.session_utils import make_session
from fantasydota.lib.team import void_in_progress_transfers

if __name__ == "__main__":
    session = make_session()
    league_id = 9870
    with transaction.manager:
        void_in_progress_transfers(session, league_id)
        recalibrate_hero_values(session, league_id)
        transaction.commit()
