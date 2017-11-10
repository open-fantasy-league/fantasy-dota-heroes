import argparse

import time
import transaction

from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, Hero


def add_result():
    session = make_session()

    parser = argparse.ArgumentParser()
    parser.add_argument("league", type=int, help="league id")
    parser.add_argument("match", type=int, help="match")
    parser.add_argument("player", type=str, help="player name")
    parser.add_argument("position", type=int, help="team position")
    parser.add_argument("kills", type=int, help="player kills")

    args = parser.parse_args()
    with transaction.manager:
        result_string = "%s,%s" % (args.position, args.kills)
        hero_id = session.query(Hero).filter(Hero.league == args.league).filter(Hero.name == args.player).first()
        if not hero_id:
            print "Name wrong"
            return
        session.add(Result(args.league, hero_id.id, args.match, result_string,
                           time.time(), 1, 1))
        transaction.commit()
    return

if __name__ == "__main__":
    add_result()
