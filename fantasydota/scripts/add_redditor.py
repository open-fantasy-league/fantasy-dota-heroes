import random
import re
import string

import transaction
from fantasydota.lib.herodict import herodict
from fantasydota.lib.session_utils import make_session
from fantasydota.lib.trade import buy
from fantasydota.models import User, UserXp, LeagueUser, League, LeagueUserDay
from fantasydota.scripts.get_tournament_data import dont_piss_off_valve_but_account_for_sporadic_failures

THREAD_URL = "https://www.reddit.com/r/DotA2/comments/96tu37/understanding_openai_five_a_simplified_dissection.json"


def main():
    regex = re.compile('[^a-zA-Z]')
    data = dont_piss_off_valve_but_account_for_sporadic_failures(THREAD_URL)
    posts = data[1]["data"]["children"]
    heroes_simple = {k: regex.sub('', v.lower()) for k, v in herodict.items()}
    with transaction.manager:
        session = make_session()
        users = session.query(User).all()
        league = session.query(League).filter(League.id == 9870).first()
        for post in posts:
            p_data = post["data"]
            body = p_data.get("body", "")
            name = p_data.get("name", "")
            if not body or not name or any(user.username == name for user in users):
                continue

            if re.match("(?i)^[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+(,)?$", body):

                pword = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
                new_user = User(name, pword, "fantasydotaeu@gmail.com")
                session.add(new_user)
                session.flush()
                session.add(UserXp(new_user.id))
                user_league = LeagueUser(new_user.id, name, 9870, False, money=50, reserve_money=50)
                session.add(user_league)
                for i in range(league.days):
                    if i >= league.stage2_start:
                        stage = 2
                    elif i >= league.stage1_start:
                        stage = 1
                    else:
                        stage = 0
                    session.add(LeagueUserDay(new_user.id, name, league.id, i, stage))
                session.flush()
                choices = [regex.sub('', c.lower()) for c in
                           re.findall('(.*?)[,$]', body)]
                for k, v in heroes_simple.items():
                    if v in choices:
                        buy(session, user_league, k, 9870, started=False)

        transaction.commit()

if __name__ == "__main__":
    main()
