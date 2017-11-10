import argparse
import time

import transaction
from fantasydota.lib.pubg_results_auto import results_config
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, Hero


def add_result_config():
    session = make_session()
    parser = argparse.ArgumentParser()
    parser.add_argument("league", type=int, help="league id")
    parser.add_argument("match", type=int, help="match id")
    args = parser.parse_args()
    results = results_config

    with transaction.manager:
        for team in results:
            for player in team['players']:
                result_string = "%s,%s" % (team["position"], player["kills"])
                hero_id = session.query(Hero).filter(Hero.league == args.league).filter(Hero.name == player['name']).first()
                if not hero_id:
                    print "Name wrong"
                    return
                session.add(Result(args.league, hero_id.id, args.match, result_string,
                                   time.time(), 1, 1))
        transaction.commit()
    return

if __name__ == "__main__":
    add_result_config()
