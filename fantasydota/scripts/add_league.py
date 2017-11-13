import argparse

import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.lib.pubg_players import pubg_init

from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, LeagueUserDay, User, LeagueUser, HeroDay, Hero, Game


def main():
    # 4 2 4
    parser = argparse.ArgumentParser()
    parser.add_argument("game", type=int, help="Game id")
    parser.add_argument("id", type=int, help="league id")
    parser.add_argument("name", type=str, help="league name")
    parser.add_argument("days", type=int, help="no. days for league")
    parser.add_argument("stage1", type=int, help="when group stage starts")
    parser.add_argument("stage2", type=int, help="when main event starts")
    parser.add_argument("url", type=str, help="tournament URL")
    args = parser.parse_args()
    url = args.url

    session = make_session()
    with transaction.manager:
        game = session.query(Game).filter(Game.id == args.game).first()
        session.add(League(game.id, args.id, args.name, args.days, args.stage1, args.stage2, url))
        session.flush()
        hero_list = heroes_init if args.game == 1 else pubg_init
        for add_hero in hero_list:
            hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], args.id, team=add_hero.get('team', None))
            session.add(hero)
            session.flush()
        for add_hero in hero_list:
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
            money = game.team_size * 10.
            reserve_money = game.reserve_size * 10.
            session.add(LeagueUser(user.id, user.username, args.id, money=money, reserve_money=reserve_money))
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
