import random

from fantasydota.models import User, League, Battlecup, BattlecupUser, BattlecupRound, BattlecupUserRound, TeamHero, \
    Hero, BattlecupTeamHeroHistory
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_


class FakePlayer(object):
    def __init__(self):
        self.user_id = -4
        self.username = "FAKE_USER_FOR_BATTLECUP_BYES"
        self.points = -9000


def fight(players, round):
    players_left, players_out = [], []
    for i in range(0, len(players), 2):
        if players[i][round].points > players[i + 1][round].points:
            players_left.append(players[i])
            players_out.append(players[i + 1])
        else:
            players_left.append(players[i + 1])
            players_out.append(players[i])
    return players_left, players_out


def check_winner_exists(session, p1, p2):
    if p1.points != p2.points:
        return p1.points, p2.points
    else:
        p1_tournament_points = session.query(User.points).filter(User.id == p1.user_id).first()[0]
        p2_tournament_points = session.query(User.points).filter(User.id == p2.user_id).first()[0]
        if p1_tournament_points > p2_tournament_points:
            return p1.points + 0.1, p2.points
        elif p1_tournament_points < p2_tournament_points:
            return p1.points, p2.points + 0.1
        else:  # rofl!
            return p1.points + random.choice([-0.1, 0.1]), p2.points


def make_battlecups(session, league_id, rounds, players, series_per_round):
    player_num = len(players)
    per_cup = 2 ** rounds
    cups = (player_num / per_cup)
    if player_num % per_cup != 0:
        cups += 1

    cup_counter = 1
    random.shuffle(players)
    new_bcups = 0
    league = session.query(League).filter(League.id == league_id).first()

    # This is kind of susceptible to breaking if I have to remove bcups from database as id not reset
    highest_id = session.query(func.max(Battlecup.id)).scalar() or 0
    # cups = (users_num / 8)
    # if users_num % 8 != 0:
    #     cups += 1
    # for i in range(cups):
    #     with transaction.manager:
    #         session.add(Battlecup(3, 0))
    #         transaction.commit()
    # cup_counter = 1
    # with transaction.manager:
    #     for user in users:
    #         if cup_counter > cups:
    #             cup_counter = 1
    #         session.add(BattlecupUser(cup_counter, user.username, user.user_id))
    #         cup_counter += 1
    #     transaction.commit()
    print "cups", cups
    for i in range(cups):
        new_bc = Battlecup(league.id, league.current_day, rounds, series_per_round)
        session.add(new_bc)
        session.commit()

    cup_counter = 0
    queues = [[] for _ in xrange(cups)]
    print len(players)
    for i, player in enumerate(players):
        if cup_counter >= cups:
            cup_counter = 0
        session.add(BattlecupUser(player.user_id, league_id, highest_id + cup_counter + 1))
        print "cup_counter: ", cup_counter
        queues[cup_counter].append(player.user_id)
        print len(queues[cup_counter])
        cup_counter += 1
    print queues

    for i, cup in enumerate(queues):
        print len(cup)
        byes = per_cup - len(cup)
        b_id = highest_id + i + 1
        for _ in range(byes):
            try:
                mr_lucky = cup.pop()
            except:
                session.add(BattlecupRound(b_id, 1, -1, None,
                                           None))
                continue
            session.add(BattlecupRound(b_id, 1, -1, mr_lucky,
                                       None))
            session.commit()
            new_bcup_id = session.query(BattlecupRound.id). \
                filter(and_(BattlecupRound.battlecup == b_id,
                            or_(BattlecupRound.player_one == mr_lucky))).first()[0]
            session.add(BattlecupUserRound(new_bcup_id, mr_lucky, 0, 0, 0, 0))
            session.commit()
        for j, player in enumerate(cup):
            if j % 2 != 0:
                print "highest_id + i + 1", highest_id + i + 1
                print "bid: ", b_id
                session.add(BattlecupRound(b_id, 1, -1, last_player, player))
                session.commit()
                new_bcup_id = session.query(BattlecupRound.id). \
                    filter(and_(BattlecupRound.battlecup == b_id,
                                or_(BattlecupRound.player_one == last_player))).first()[0]
                session.add(BattlecupUserRound(new_bcup_id, last_player, 0, 0, 0, 0))
                session.add(BattlecupUserRound(new_bcup_id, player, 0, 0, 0, 0))
                session.commit()
            else:
                last_player = player
                if j == len(cup) - 1:
                    session.add(BattlecupRound(b_id, 1, -1, last_player,
                                               None))
                    session.commit()
                    new_bcup_id = session.query(BattlecupRound.id). \
                        filter(and_(BattlecupRound.battlecup == b_id,
                                    or_(BattlecupRound.player_one == last_player))).first()[0]
                    session.add(BattlecupUserRound(new_bcup_id, last_player, 0, 0, 0, 0))
                    session.commit()


def auto_fill_teams(session, league):
    autofill_users = session.query(User).filter(User.autofill_team.is_(True)).all()
    for user in autofill_users:
        if not session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                               TeamHero.is_battlecup.is_(True),
                                               TeamHero.user_id == user.id)).first():
            generate_team(session, league.id, user.id)
    session.commit()


def generate_team(session, league, username):
    heroes = session.query(Hero).filter(Hero.is_battlecup.is_(True)).filter(Hero.league == league).all()
    value_counter = 0
    for i in range(5):
        if i == 0:
            filtered_heroes = heroes
        elif value_counter > (i+1) * 9.5:
            filtered_heroes = [hero for hero in heroes if hero.value < 9.5 and hero.value + value_counter < 50.]
        else:
            filtered_heroes = [hero for hero in heroes if hero.value > 9.5 and hero.value + value_counter < 50.]
        session.add(TeamHero(username, random.choice(filtered_heroes).id, league, True))


def player_hero_imgs(session, battlecup, round_, league_id, old_hero):

    if old_hero:
        hero_q = session.query(BattlecupTeamHeroHistory.hero_name). \
            filter(and_(BattlecupTeamHeroHistory.league == league_id,
                        BattlecupTeamHeroHistory.day == battlecup.day))
        hero_q_1 = hero_q.filter(BattlecupTeamHeroHistory.user_id == round_.player_one)

        hero_q_2 = hero_q.filter(BattlecupTeamHeroHistory.user_id == round_.player_two)
    else:
        hero_q = session.query(TeamHero.hero_name). \
            filter(and_(TeamHero.league == league_id,
                        TeamHero.is_battlecup.is_(True)
                        ))
        hero_q_1 = hero_q.filter(TeamHero.user_id == round_.player_one)

        hero_q_2 = hero_q.filter(TeamHero.user_id == round_.player_two)

    p1_heroes = {"pname": session.query(User.username).filter(User.id == round_.player_one).first(),
                 "heroes": [
                     x[0] for x in hero_q_1.all()
                     ]}

    p2_heroes = {"pname": session.query(User.username).filter(User.id == round_.player_two).first(),
                 "heroes": [
                     x[0] for x in hero_q_2.all()
                     ]}

    return p1_heroes, p2_heroes
