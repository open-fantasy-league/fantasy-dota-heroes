import json

from fantasydota.models import LeagueUserDay

from fantasydota.lib.session_utils import make_session


def hmmm():
    session = make_session(False)
    for luser in session.query(LeagueUserDay).filter(LeagueUserDay.day==5).all():
	yesterday = session.query(LeagueUserDay).filter(LeagueUserDay.day==4).filter(LeagueUserDay.user_id == luser.user_id).first()
	yesterday.points += luser.points
	yesterday.picks += luser.picks
	yesterday.bans += luser.bans
	yesterday.wins += luser.wins
	luser.points = 0
	luser.picks = 0
	luser.wins = 0
	luser.bans = 0
	
    session.commit()
	

def main():
    hmmm()

if __name__ == "__main__":
    main()
