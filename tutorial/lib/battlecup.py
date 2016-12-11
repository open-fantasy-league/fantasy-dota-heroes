import random
from tutorial.models import User


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