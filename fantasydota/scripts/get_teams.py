import os
import time

import json
from datetime import datetime

from fantasydota.lib.constants import TEAM_IDS_TO_NAMES
from fantasydota.lib.valve_requests import dont_piss_off_valve_but_account_for_sporadic_failures


def get_data():
    teams = []
    for team_id, team_name in TEAM_IDS_TO_NAMES.items():
        team_info = dont_piss_off_valve_but_account_for_sporadic_failures("https://api.opendota.com/api/teams/{}/players".format(team_id))
        team_info = [p for p in team_info if p['is_current_team_member']]
        teams.append({'name': team_name, 'players': team_info})
    return teams


if __name__ == "__main__":
    data = get_data()
    #import pdb; pdb.set_trace()
    try:
        with open(os.getcwd() + '/../miscdata/dotaplayers_{}.json'.format(datetime.now().date()), 'w+') as f:
            f.write(json.dumps(data))
    except:
        import pdb;
        pdb.set_trace()
