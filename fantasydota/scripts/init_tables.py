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
                ('Daily Win', 'Finish the day as points leader', 110),
                ('Fantasy King', 'Finish the week as points leader', 300),
                ('Weekly Top Five', 'Finish the week 5th or higher for points', 40),
                ('Win King', 'Finish the week with the most wins', 90),
                ('Ban King', 'Finish the week with the most bans', 50),
                ('Pick King', 'Finish the week with the most picks', 75),
                ('Top Picker', 'Own the highest points scoring hero this week', 100),
                ('Shrewd Investor', 'Own the highest points per cost ratio hero this week', 140),
                ('Full House', 'Your whole main team is either picked or banned', 280),
                ('Three of a Kind', '3 of your main team is picked', 200),
                ('HAHAHA....AHAHAHAHAHAHAHA', 'Finish week with negative points', 50)
            ]
            for achievement in achievements:
                new_achievement = Achievement(1, achievement[0], achievement[1], achievement[2])
                session.add(new_achievement)
            add_league(1, 1, "Week 1", 7, 5, 9, "", session=session)
            for tournament in PRO_CIRCUIT_LEAGUES:
                session.add(ProCircuitTournament(tournament['id'], 1, tournament['name'], tournament['major']))
            transaction.commit()
