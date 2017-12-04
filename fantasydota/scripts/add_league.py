import argparse

import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.lib.pubg_players import pubg_init

from fantasydota.models import League, LeagueUserDay, User, LeagueUser, HeroDay, Hero, Game


def add_league(game_id, league_id, name, days, stage1, stage2, url, session=None):
    if not session:
        # probably a more sensible way to avoid circular import
        from fantasydota.lib.session_utils import make_session
        session = make_session()
    game = session.query(Game).filter(Game.id == game_id).first()
    session.add(League(game.id, league_id, name, days, stage1, stage2, url))
    session.flush()
    hero_list = heroes_init if game_id == 1 else pubg_init
    for add_hero in hero_list:
        hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], league_id, team=add_hero.get('team', None))
        session.add(hero)
        session.flush()
    for add_hero in hero_list:
        for i in range(days):
            if i >= stage2:
                stage = 2
            elif i >= stage1:
                stage = 1
            else:
                stage = 0
            hero = HeroDay(add_hero["id"], add_hero["name"], league_id, i, stage, add_hero["value"])
            session.add(hero)
    for user in session.query(User).all():
        money = game.team_size * 10.
        reserve_money = game.reserve_size * 10.
        session.add(LeagueUser(user.id, user.username, league_id, money=money, reserve_money=reserve_money))
        for i in range(days):
            if i >= stage2:
                stage = 2
            elif i >= stage1:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(user.id, user.username, league_id, i, stage))

if __name__ == "__main__":
    #add_league(1, new_id, new_name, 7, 5, 9, "", session=session)
    parser = argparse.ArgumentParser()
    parser.add_argument("game", type=int, help="Game id")
    parser.add_argument("id", type=int, help="league id")
    parser.add_argument("name", type=str, help="league name")
    parser.add_argument("days", type=int, help="no. days for league")
    parser.add_argument("stage1", type=int, help="when group stage starts")
    parser.add_argument("stage2", type=int, help="when main event starts")
    parser.add_argument("url", type=str, help="tournament URL")
    args = parser.parse_args()
    with transaction.manager:
        add_league(args.game, args.id, args.name, args.days, args.stage1, args.stage2, args.url)
        transaction.commit()
