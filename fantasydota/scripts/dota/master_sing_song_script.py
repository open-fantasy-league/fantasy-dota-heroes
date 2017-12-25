import datetime
import fcntl
import sys

from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, ProCircuitTournament
from fantasydota.scripts.end_of_day import end_of_day
from fantasydota.scripts.get_tournament_data import add_matches
from fantasydota.scripts.update_all import update_all
from rollover_league import rollover_league


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
    now = datetime.datetime.utcnow()
    if now.weekday() == 1 and now.hour >= 6 and week.current_day > 1:
    #if time_since_week_start > SECONDS_IN_WEEK:
        print("rolling over league")
        rollover_league()
        week = session.query(League).filter(League.game == game_id).filter(League.status == 1).first()
        week_id = week.id
    # days are 0 indexed
    elif now.weekday() > (week.current_day + 1) and now.hour >= 6:
        print("it's a new day!")
        end_of_day(week_id)
    for tournament in [x[0] for x in session.query(ProCircuitTournament.id).all()]:
        add_matches(session, tournament, tstamp_from=1514786400, week_id=week_id)
    update_all(session)

if __name__ == "__main__":
    fp = open('/tmp/fdota.pid', 'w')
    check_not_already_running(fp)
    super_duper_updaterooney()
