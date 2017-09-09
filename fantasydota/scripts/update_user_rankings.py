import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, LeagueUser, LeagueUserDay
from sqlalchemy import desc


def set_user_rankings(session, league_id, day=None):
    # But is there a better way??
    user_l = LeagueUser if day is None else LeagueUserDay
    l_query = session.query(user_l.username).filter(user_l.league == league_id)
    l_query = l_query.filter(user_l.day == day) if day is not None else l_query
    wins_ranking = l_query.order_by(desc(user_l.wins)).all()
    for i, user in enumerate(wins_ranking):
        # try user.wins_rank += 1?
        l_query.filter(user_l.username == user.username).\
            update({user_l.wins_rank: i+1})

    points_ranking = l_query.order_by(desc(user_l.points)).all()
    for i, user in enumerate(points_ranking):
        l_query.filter(user_l.username == user.username). \
            update({user_l.points_rank: i + 1})

    picks_ranking = l_query.order_by(desc(user_l.picks)).all()
    for i, user in enumerate(picks_ranking):
        l_query.filter(user_l.username == user.username). \
            update({user_l.picks_rank: i + 1})

    bans_ranking = l_query.order_by(desc(user_l.bans)).all()
    for i, user in enumerate(bans_ranking):
        l_query.filter(user_l.username == user.username)  . \
            update({user_l.bans_rank: i + 1})
    return


def update_user_rankings(session, league):
    with transaction.manager:
        set_user_rankings(session, league.id)
        set_user_rankings(session, league.id, day=league.current_day)
        transaction.commit()


def main():
    session = make_session()
    for league in session.query(League).filter(League.status == 1).all():
        update_user_rankings(session, league)

if __name__ == "__main__":
    main()
