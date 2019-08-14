import json
import transaction
import urllib2
from fantasydota.lib.constants import API_URL
from fantasydota.lib.session_utils import make_session
from fantasydota.local_settings import FANTASY_API_KEY
from fantasydota.models import Team



def main():
    with transaction.manager:
        session = make_session()
        team_names = session.query(Team).all()
        for custom_team in team_names:
            print(custom_team.name, custom_team.user_id)
            url = API_URL + "users/" + str(custom_team.user_id) + "/leagues/" + str(custom_team.league_id)
            req = urllib2.Request(
                url, data=json.dumps({'username': custom_team.name}), headers={
                    'apiKey': FANTASY_API_KEY,
                    'User-Agent': 'fantasy-dota-frontend',
                    "Content-Type": "application/json"
                }
            )
            response = urllib2.urlopen(req)
            print(response.read())


if __name__ == "__main__":
    main()
