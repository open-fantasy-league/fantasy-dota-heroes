import random

import transaction
from fantasydota.models import User, League, Battlecup, BattlecupUser, BattlecupRound
from sqlalchemy import func


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
        p1_tournament_points = session.query(User.points).filter(User.username == p1.username).first()[0]
        p2_tournament_points = session.query(User.points).filter(User.username == p2.username).first()[0]
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

    # This is kind of susceptible to breaking if I have to remove bcups from database as id not reset
    highest_id = session.query(func.max(Battlecup.id)).scalar() or 0
    for i, player in enumerate(players):
        if cup_counter == 1:
            league = session.query(League).filter(League.id == league_id).first()
            new_bc = Battlecup(league.id, league.current_day, rounds, series_per_round)
            with transaction.manager:
                session.add(new_bc)
                transaction.commit()
            new_bcups += 1
        with transaction.manager:
            session.add(BattlecupUser(player.user, league_id, highest_id + new_bcups))
            transaction.commit()

        if i % 2 != 0:
            # -1 is temporary. gets overwritten when we parse 1st game of the day
            # when made at start day always going to be 0 for round right?
            with transaction.manager:
                session.add(BattlecupRound(highest_id + new_bcups, 0, -1, last_player.user, player.user))
                transaction.commit()
        else:
            last_player = player

        cup_counter += 1
        if cup_counter > per_cup:
            cup_counter = 1
