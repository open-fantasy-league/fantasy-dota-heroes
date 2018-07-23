import argparse

from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, LeagueUser, LeagueUserDay


def set_old_rankings(session, league):
    old_list = []
    for league_user in session.query(LeagueUser).filter(LeagueUser.league == league.id):
        recent_points_q = session.query(LeagueUserDay.points) \
            .filter(LeagueUserDay.user_id == league_user.user_id).filter(LeagueUserDay.league == league.id) \
            .filter(LeagueUserDay.day > league.current_day).all()
        recent_points = sum(t[0] for t in recent_points_q)

        recent_wins_q = session.query(LeagueUserDay.wins) \
            .filter(LeagueUserDay.user_id == league_user.user_id).filter(LeagueUserDay.league == league.id) \
            .filter(LeagueUserDay.day > league.current_day).all()
        recent_wins = sum(t[0] for t in recent_wins_q)

        recent_bans_q = session.query(LeagueUserDay.bans) \
            .filter(LeagueUserDay.user_id == league_user.user_id).filter(LeagueUserDay.league == league.id) \
            .filter(LeagueUserDay.day > league.current_day).all()
        recent_bans = sum(t[0] for t in recent_bans_q)

        recent_picks_q = session.query(LeagueUserDay.picks) \
            .filter(LeagueUserDay.user_id == league_user.user_id).filter(LeagueUserDay.league == league.id) \
            .filter(LeagueUserDay.day > league.current_day).all()
        recent_picks = sum(t[0] for t in recent_picks_q)

        old_list.append({
            "id": league_user.id,
            "points": league_user.points - recent_points,
            "wins": league_user.wins - recent_wins,
            "picks": league_user.picks - recent_picks,
            "bans": league_user.bans - recent_bans,
        })

    sorted_points = sorted(old_list, key=lambda x: x["points"], reverse=True)
    sorted_wins = sorted(old_list, key=lambda x: x["wins"], reverse=True)
    sorted_picks = sorted(old_list, key=lambda x: x["picks"], reverse=True)
    sorted_bans = sorted(old_list, key=lambda x: x["bans"], reverse=True)
    for i, old_user in enumerate(sorted_points):
        session.query(LeagueUser).filter(LeagueUser.id == old_user["id"]).update({
            LeagueUser.old_points_rank: i + 1
        })
    for i, old_user in enumerate(sorted_picks):
        session.query(LeagueUser).filter(LeagueUser.id == old_user["id"]).update({
            LeagueUser.old_picks_rank: i + 1
        })
    for i, old_user in enumerate(sorted_wins):
        session.query(LeagueUser).filter(LeagueUser.id == old_user["id"]).update({
            LeagueUser.old_wins_rank: i + 1
        })
    for i, old_user in enumerate(sorted_bans):
        session.query(LeagueUser).filter(LeagueUser.id == old_user["id"]).update({
            LeagueUser.old_bans_rank: i + 1
        })


def start_of_day(league_id=None):
    session = make_session(transaction=False, autoflush=False)
    if not league_id:
        parser = argparse.ArgumentParser()
        parser.add_argument("league", type=int, help="league id")
        args = parser.parse_args()
        league_id = args.league
    league = session.query(League).filter(League.id == league_id).first()
    set_old_rankings(session, league)
    league.transfer_open = False  # close league window if not already closed
    league.swap_open = False
    session.commit()


def main():
    start_of_day()

if __name__ == "__main__":
    main()
