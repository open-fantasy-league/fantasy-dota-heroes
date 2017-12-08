from fantasydota.models import UserAchievement, Achievement, UserXp, LeagueUser, Hero, TeamHero, HeroDay
from sqlalchemy import func


def check_invalid_password(password, confirm_password):
    if len(password) < 6:
        return {"message": "Password too short. 6 characters minimum please"}
    elif len(password) > 20:
        return {"message": "Password too long. 20 characters maximum please"}
    elif confirm_password != password:
        return{"message": "Passwords did not match"}
    else:
        return False


def add_achievement(session, achievement_name, user_id):
    # TODO maybe need a game check
    achievement = session.query(Achievement).filter(Achievement.name == achievement_name).first()
    new_achievement = UserAchievement(achievement.id, user_id)
    session.add(new_achievement)
    session.query(UserXp).filter(UserXp.user_id == user_id).update({
        UserXp.xp: UserXp.xp + achievement.xp
    })


def check_top(session, league_id, valid_users, max_col, achievement_name):
    subq = session.query(func.max(max_col).label('m')).subquery()
    tops = session.query(Hero).join(subq, subq.c.ml == max_col).all()
    for t in tops:
        users_to_add = []
        for th in session.query(TeamHero).filter(TeamHero.league == league_id)\
            .filter(TeamHero.active.is_(True))\
            .filter(TeamHero.hero_id == t.hero_id).all():
                users_to_add.append(th.user_id)
        for user_id in set(users_to_add) & valid_users:
            add_achievement(session, achievement_name, user_id)


def check_top_value_picker(session, league_id, valid_users):
    subq = session.query(func.max(Hero.points / Hero.value).label('mp')).subquery()
    top = session.query(Hero).join(subq, subq.c.ml == Hero.points / Hero.value).all()
    for th in session.query(TeamHero).filter(TeamHero.league == league_id)\
        .filter(TeamHero.active.is_(True))\
        .filter(TeamHero.hero_id == top.hero_id).all():
        if th.user_id in valid_users:
            add_achievement(session, 'Shrewd Investor', th.user_id)


def check_top_day(session, league_id, max_col, achievement_name):
    subq = session.query(func.max(max_col).label('m')).subquery()
    tops = session.query(HeroDay).join(subq, subq.c.ml == max_col).all()
    for t in tops:
        users_to_add = []
        for th in session.query(TeamHero).filter(TeamHero.league == league_id)\
            .filter(TeamHero.active.is_(True))\
            .filter(TeamHero.hero_id == t.hero_id).all():
                users_to_add.append(th.user_id)
        for user_id in set(users_to_add):
            add_achievement(session, achievement_name, user_id)


def assign_xp_and_weekly_achievements(session, league):
    # TODO need a master order by func
    # order by late_start so that i == 0 check doesnt pick invalid winner
    lusers = session.query(LeagueUser).filter(LeagueUser.league == league.id).order_by(LeagueUser.late_start).order_by(LeagueUser.points_rank).all()
    valid_users = set(l.user_id for l in lusers if not l.late_start)
    check_top(session, league.id, valid_users, Hero.points, 'Top Picker')
    check_top(session, league.id, valid_users, Hero.bans, 'Ban King')
    check_top(session, league.id, valid_users, Hero.picks, 'Pick King')
    check_top_value_picker(session, league.id, valid_users)
    for i, luser in enumerate(lusers):
        if i == 0:
            add_achievement(session, "Fantasy King", luser)
        if i < 5:
            add_achievement(session, "Weekly Top Five", luser)
        user_xp = session.query(UserXp).filter(UserXp.user_id == luser.user_id).first()
        if not luser.late_start:
            user_xp.highest_weekly_pos = max(user_xp.highest_weekly_pos, luser.points_rank)
        user_xp.xp += UserXp.position_xp(i, len(lusers))
        user_xp.all_time_points += luser.points


def assign_daily_achievements(session, league):
    luser = session.query(LeagueUser).filter(LeagueUser.league == league.id).order_by(LeagueUser.points_rank).first()
    add_achievement(session, "Daily Winner", luser)
