import time
import fcntl

import sys
from fantasydota.lib.constants import SECONDS_IN_WEEK, SECONDS_IN_DAY
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, ProCircuitTournament
from rollover_league import rollover_league
from fantasydota.scripts.end_of_day import end_of_day
from fantasydota.scripts.get_tournament_data import add_matches
from fantasydota.scripts.update_all import update_all


def check_not_already_running(fp_):
    # https://stackoverflow.com/a/1662504
    try:
        fcntl.lockf(fp_, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("locked pid")
    except IOError:
        print("another instance is running")
        sys.exit(0)


def super_duper_updaterooney():
    session = make_session()
    game_id = 1
    week = session.query(League).filter(League.game == game_id).filter(League.status == 1).first()
    week_id = week.id
    time_since_week_start = time.time() - week.start
    if time_since_week_start > SECONDS_IN_WEEK:
        print("rolling over league")
        rollover_league()
        week = session.query(League).filter(League.game == game_id).filter(League.status == 1).first()
        week_id = week.id
    # days are 0 indexed
    elif time_since_week_start > SECONDS_IN_DAY * (week.current_day + 1):
        print("it's a new day!")
        end_of_day(week_id)
    for tournament in [x[0] for x in session.query(ProCircuitTournament.id).all()]:
        add_matches(session, tournament, tstamp_from=1512057853, week_id=week_id)
    update_all(session)

if __name__ == "__main__":
    fp = open('/tmp/fdota.pid', 'w')
    check_not_already_running(fp)
    super_duper_updaterooney()
