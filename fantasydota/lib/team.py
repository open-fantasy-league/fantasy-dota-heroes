from fantasydota.models import TeamHero


def main_team_to_active(session, luser):
    session.query(TeamHero).filter(TeamHero.user_id == luser.user_id)\
        .filter(TeamHero.league == luser.league).filter(TeamHero.reserve.is_(False)).update({
            TeamHero.active: True
        })
