import transaction
from fantasydota.models import Game, Achievement
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
                ('Daily Win', 'Finish the day as points leader'),
                ('Fantasy King', 'Finish the week as points leader'),
                ('Weekly Top Five', 'Finish the week 5th or higher for points'),
                ('Ban King', 'Finish the week with the most bans'),
                ('Pick King', 'Finish the week with the most picks'),
                ('Top Picker', 'Own the highest points scoring hero this week'),
                ('Shrewd Investor', 'Own the highest points per cost ratio hero this week'),
                ('Daily Win', 'Finish the day as points leader'),
                ('Full House', 'Your whole main team is either picked or banned'),
                ('Three of a Kind', '3 of your main team is picked')
            ]
            for achievement in achievements:
                new_achievement = Achievement(1, achievement[0], achievement[1])
                session.add(new_achievement)
            add_league(1, 1, "Week 1", 7, 5, 9, "", session=session)
            transaction.commit()
