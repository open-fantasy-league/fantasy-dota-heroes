import os
import socket

DIR = os.environ.get('FDOTA')
SECONDS_IN_WEEK = 604800
SECONDS_IN_DAY = 86400
SECONDS_IN_12_HOURS = 43200
SECONDS_IN_HOUR = 3600

DEFAULT_LEAGUE = 1 if socket.gethostname() == 'fantasyesport' else 6
HERO_LEAGUE = 2 if socket.gethostname() == 'fantasyesport' else 10
OTHER_LEAGUES = [HERO_LEAGUE]
API_URL = 'https://dota.openfantasyleague.com/api/v1/' if socket.gethostname() == 'fantasyesport' else 'http://localhost/api/v1/'

FESPORT_ACCOUNT = 0
STEAM_ACCOUNT = 1
REDDIT_ACCOUNT = 2
FACEBOOK_ACCOUNT = 3
GOOGLE_ACCOUNT = 4
OTHER_ACCOUNT = 5
SOCIAL_CODES = {'FESPORT_ACCOUNT': FESPORT_ACCOUNT,
                'steam': STEAM_ACCOUNT,
                'facebook': FACEBOOK_ACCOUNT,
                'google-oauth2': GOOGLE_ACCOUNT,
                'reddit': REDDIT_ACCOUNT
                }

TEAM_IDS_TO_NAMES = {
    1838315: 'Team Secret',
1883502: 'Virtus.Pro',
726228: 'Vici Gaming',
    39: 'Evil Geniuses',
2626685: 'Keen Gaming',
2586976: 'OG',
36: 'Navi',
543897: 'Mineski',
350190: 'Fnatic',
15: 'PSG.LGD',
6214973: 'Ninjas in Pyjamas',
111474: 'Alliance',
2108395: 'TNC Predator',
2163: 'Team Liquid',
2672298: 'Infamous',
6214538: 'Forward Gaming',
7203342: 'Chaos',
6209804: 'RNG'



}

TI9 = 10749