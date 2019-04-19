import os
import socket

DIR = os.environ.get('FDOTA')
SECONDS_IN_WEEK = 604800
SECONDS_IN_DAY = 86400
SECONDS_IN_12_HOURS = 43200
SECONDS_IN_HOUR = 3600

DEFAULT_LEAGUE = 28
API_URL = 'https://fantasyesport.eu/api/v1/' if socket.gethostname() == 'fantasyesport' else 'http://localhost/api/v1/'

FESPORT_ACCOUNT = 0
STEAM_ACCOUNT = 1
REDDIT_ACCOUNT = 2
