import os
import socket

DIR = os.environ.get('FDOTA')
SECONDS_IN_WEEK = 604800
SECONDS_IN_DAY = 86400
SECONDS_IN_12_HOURS = 43200
SECONDS_IN_HOUR = 3600

DEFAULT_LEAGUE = 3
API_URL = 'https://football.openfantasyleague.com/api/v1/' if socket.gethostname() == 'fantasyesport' else 'http://localhost/api/v1/'

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
