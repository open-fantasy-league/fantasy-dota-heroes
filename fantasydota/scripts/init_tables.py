import transaction
from fantasydota.lib.constants import PRO_CIRCUIT_LEAGUES
from fantasydota.models import Game, Achievement, ProCircuitTournament
from fantasydota.scripts.add_league import add_league


def create_tables(DBSession, overwrite_empty_game_check=False):
    session = DBSession()
    with transaction.manager:
        if not session.query(Game).first() or overwrite_empty_game_check:
            dota = Game('DotA', 'DOTA', 'Hero', 5, 4)
            pubg = Game('PUBG', 'PUBG', 'Player', 4, 2)
            session.add(dota)
            session.add(pubg)
            achievements = [
                ('Daily Win', 'Finish the day as points leader', 60),
                ('Fantasy King', 'Finish the week as points leader', 200),
                ('Weekly Top Five', 'Finish the week 5th or higher for points', 30),
                ('Ban King', 'Finish the week with the most bans', 50),
                ('Pick King', 'Finish the week with the most picks', 50),
                ('Top Picker', 'Own the highest points scoring hero this week', 40),
                ('Shrewd Investor', 'Own the highest points per cost ratio hero this week', 80),
                ('Full House', 'Your whole main team is either picked or banned', 150),
                ('Three of a Kind', '3 of your main team is picked', 40)
            ]
            for achievement in achievements:
                new_achievement = Achievement(1, achievement[0], achievement[1], achievement[2])
                session.add(new_achievement)
            add_league(1, 1, "Week 1", 7, 5, 9, "", session=session)
            for tournament in PRO_CIRCUIT_LEAGUES:
                session.add(ProCircuitTournament(tournament['id'], 1, tournament['name'], tournament['major']))
            transaction.commit()
