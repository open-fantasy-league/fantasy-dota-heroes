import argparse

from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import League, LeagueUserDay, User, LeagueUser
from sqlalchemy import and_


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=int, help="league id")
    parser.add_argument("name", type=str, help="league name")
    parser.add_argument("days", type=int, help="no. days for league")
    parser.add_argument("stage1", type=int, help="when group stage starts")
    parser.add_argument("stage2", type=int, help="when main event starts")
    args = parser.parse_args()

    session = make_session(False, True, True)
    session.add(League(args.id, args.name, args.days, args.stage1, args.stage2))
    for user in session.query(User).all():
        session.add(LeagueUser(user.id, user.username, args.id))
        session.commit()
        league_user = session.query(LeagueUser.id).filter(and_(LeagueUser.user_id == user.id,
                                                               LeagueUser.league == args.id)).first()[0]
        for i in range(args.days):
            if i >= args.stage2:
                stage = 2
            elif i >= args.stage1:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(league_user, i, stage))

if __name__ == "__main__":
    main()
