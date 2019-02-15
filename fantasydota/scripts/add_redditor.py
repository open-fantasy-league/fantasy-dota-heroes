import random
import re
import string

import os
from functools import partial

import transaction
from fantasydota.lib.constants import API_URL
from fantasydota.lib.constants import DEFAULT_LEAGUE
from fantasydota.lib.general import post_api_json
from fantasydota.lib.herodict import herodict
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User

THREAD_URL = "https://www.reddit.com/r/DotA2/comments/96yrmt/need_players_for_ti8_hero_fantasy_dota_league.json"

API_ADD_USER_URL = "{}users/".format(API_URL, DEFAULT_LEAGUE)

FAKE = {"data": {"body": "Weaver, Keeper of the light, Doom, Techies, and Bloodseeker", "author": "Daveoo"}}

def main():
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
    post_api_json_wkey = partial(post_api_json, fe_api_key=FE_APIKEY)

    regex = re.compile('[^a-zA-Z]')
    #data = dont_piss_off_valve_but_account_for_sporadic_failures(THREAD_URL)
    #posts = data[1]["data"]["children"]
    heroes_simple = {k: regex.sub('', v.lower()) for k, v in herodict.items()}
    posts = [FAKE]
    for post in posts:
        p_data = post["data"]
        body = p_data.get("body", "")
        body = body.replace(", and ", ",")
        name = p_data.get("author", "")
        if not body:
            continue

        print(body)
        print(re.match("(?i)^[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+,[a-z\-'\s]+(,)?$", body))
        matches = re.match("(?i)^([a-z\-'\s]+),([a-z\-'\s]+),([a-z\-'\s]+),([a-z\-'\s]+),([a-z\-'\s]+)(?:,)?$", body)
        if matches:
            with transaction.manager:
                session = make_session()
                users = session.query(User).all()
                if not name or any(user.username == name for user in users):
                    continue

                pword = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
                new_user = User(name, pword, "fantasydotaeu@gmail.com", account_type=2)
                session.add(new_user)
                session.flush()
                new_user_id = new_user.id
                print(body.lower())
                #import pdb; pdb.set_trace()
                choices = [m.strip().lower() for m in matches.groups()]
                post_api_json_wkey(API_ADD_USER_URL, {'userId': new_user_id, 'username': name})
                API_JOIN_LEAGUE_URL = "{}users/{}/join/{}".format(API_URL, new_user_id, DEFAULT_LEAGUE)
                API_BUY_URL = "{}transfers/leagues/{}/users/{}".format(API_URL, DEFAULT_LEAGUE, new_user_id)
                post_api_json_wkey(API_JOIN_LEAGUE_URL, {})
                buy_dict = {'buy': [], "isCheck": False}
                print(choices)
                for k, v in heroes_simple.items():
                    if v in choices:
                        print(v)
                        buy_dict['buy'].append(k)

                post_api_json_wkey(API_BUY_URL, buy_dict)
                transaction.commit()

if __name__ == "__main__":
    main()
