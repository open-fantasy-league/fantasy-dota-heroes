import argparse

import transaction
from fantasydota.lib.herolist_vals import heroes_init

from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, LeagueUserDay, User, LeagueUser, HeroDay, Hero


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int, help="league id")
    parser.add_argument("name", type=str, help="league name")
    parser.add_argument("days", type=int, help="no. days for league")
    parser.add_argument("stage1", type=int, help="when group stage starts")
    parser.add_argument("stage2", type=int, help="when main event starts")
    args = parser.parse_args()
    url = "http://wiki.teamliquid.net/dota2/The_International/2017"

    session = make_session()
    with transaction.manager:
        session.add(League(args.id, args.name, args.days, args.stage1, args.stage2, url))
        session.flush()
        for add_hero in heroes_init:
            hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], args.id)
            session.add(hero)
        for add_hero in heroes_init:
            for i in range(args.days):
                if i >= args.stage2:
                    stage = 2
                elif i >= args.stage1:
                    stage = 1
                else:
                    stage = 0
                hero = HeroDay(add_hero["id"], add_hero["name"], args.id, i, stage, add_hero["value"])
                session.add(hero)
        for user in session.query(User).all():
            session.add(LeagueUser(user.id, user.username, args.id))
            for i in range(args.days):
                if i >= args.stage2:
                    stage = 2
                elif i >= args.stage1:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(user.id, user.username, args.id, i, stage))
        transaction.commit()

if __name__ == "__main__":
    main()
