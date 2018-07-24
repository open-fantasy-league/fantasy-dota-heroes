from fantasydota.models import TeamHero, LeagueUser


def main_team_to_active(session, luser):
    session.query(TeamHero).filter(TeamHero.user_id == luser.user_id)\
        .filter(TeamHero.league == luser.league).filter(TeamHero.reserve.is_(False)).update({
            TeamHero.active: True
        })


def void_in_progress_transfers(session, league_id):
    # TODO make this a join
    for luser in session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.swap_tstamp == None).all():
        for th in session.query(TeamHero).filter(TeamHero.user_id == luser.user_id):
            if not th.active:
                luser.money += th.cost
                session.delete(th)
                luser.voided_transfers = True
            else:
                th.reserve = False
                luser.money -= th.cost
                luser.voided_transfers = True
