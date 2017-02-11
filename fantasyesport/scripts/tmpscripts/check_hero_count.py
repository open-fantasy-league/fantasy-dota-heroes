# import transaction
# from fantasyesport.lib.session_utils import make_session
# from fantasyesport.models import TeamHero, User, Hero
# from fantasyesport.util.random_function import bprint
#
#
# def main():
#     '''
#     Fix user money to what it should be based on heroes in their team
#     remove hero if team over max value
#     :return:
#     '''
#     session = make_session()
#     with transaction.manager:
#         users = session.query(User).all()
#         for user in users:
#             current_money = user.money
#             user_money = 50.0
#             heroes_removed = 0
#             heroes = session.query(TeamHero).filter(TeamHero.user == user.username).all()
#             start_hero = len(heroes)
#             heroes_seen = []
#             # CARE!!! indentation was fucked when last checked this.
#         active_counter = 0
#             for hero in heroes:
#         if hero.active:
#             active_counter += 1
#                 heroq = session.query(Hero).filter(Hero.hero_id == hero.hero).first()
#                 if hero.hero in heroes_seen:
#                     print "would remove", user.username
#                     #session.delete(hero)
#                     heroes_removed += 1
#                     continue
#                 heroes_seen.append(hero.hero)
#                 if user_money - heroq.value < -0.001:
#                         bprint("deleting")
#                         #session.delete(hero)
#                         heroes_removed += 1
#                 else:
#                     user_money -= heroq.value
#         if active_counter > 5:
#                 print "uh oh. user has more than 5 active" % user.username
#             if heroes_removed != 0:
#                 print "would update hero count user: %s, -%s" % (user.username, heroes_removed)
#             #user.hero_count = start_hero - heroes_removed
#             #user.money = user_money
#             if abs(current_money - user_money) > 0.5:
#                 print "Would update money from %s to %s, user:%s" % (current_money, user_money, user.username)
#         #transaction.commit()
#
# if __name__ == "__main__":
#     main()
