import transaction
# from sqlalchemy import and_
# from sqlalchemy import desc
from sqlalchemy import and_

from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, TeamHero, LeagueUser, Sale


#
#
#
def add_hero_player(session, user_id, hero_id, league_id, reserve):
    with transaction.manager:

        hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                           Hero.league == league_id)).first()[0]

        teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id).filter(TeamHero.reserve.is_(reserve))
        teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

        l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(
            LeagueUser.league == league_id).first()

        user_money = l_user.money if not reserve else l_user.reserve_money

        if user_money < hero_value:
            print("ERROR: Insufficient credits")
            return {"success": False, "message": "ERROR: Insufficient credits"}

        new_credits = round(user_money - hero_value, 1)

        if teamq.count() >= 5:
            return {"success": False, "message": "ERROR: Team is currently full"}
        if teamq_hero.first():
            print "ERROR: Hero already in team"
            return {"success": False, "message": "ERROR: Hero already in team"}
        else:
            l_user.money = new_credits
            session.add(TeamHero(user_id, hero_id, league_id, hero_value, reserve))
            session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, True))

        transaction.commit()


def main():
    session = make_session()
    # add_hero_player(session, 480, 107, 5609, False)
    # add_hero_player(session, 480, 71, 5609, False)
    # add_hero_player(session, 480, 112, 5609, False)
    # add_hero_player(session, 480, 66, 5609, False)
    # add_hero_player(session, 480, 32, 5609, False)

    add_hero_player(session, 337, 10, 5627, False)
    add_hero_player(session, 337, 107, 5627, False)
    add_hero_player(session, 337, 72, 5627, False)
    add_hero_player(session, 337, 100, 5627, False)
    add_hero_player(session, 337, 91, 5627, False)
    add_hero_player(session, 337, 50, 5627, True)
    add_hero_player(session, 337, 52, 5627, True)
    add_hero_player(session, 337, 58, 5627, True)
    add_hero_player(session, 337, 57, 5627, True)

if __name__ == "__main__":
    main()
