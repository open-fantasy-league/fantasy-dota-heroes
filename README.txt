# fantasydota README
==================

Lives at https://www.fantasyesport.eu

The fantasy sport ecosystem described in readme of https://github.com/open-fantasy-sports/fantasy-esport-scala

this project utilises fantasy-esport-scala as an api for storing/manipulating data.

It handles user auth (either their own site accounts or with steam), and provides frontend for displaying leaderboards and choosing teams.

frontend is hacky jquery

it also has scripts to:
- get results from dota api and add them to league
- calibrate hero values based on recent results and create league
- recalibrate values midway through league

Uses:
- python  2, pyramid web framework, mysql db

Getting Started
---------------

- Make a new python 2 virtual environment for this project

- cd <directory containing this file>

- add environment variable for database string. e.g. add this to .bashrc
  export FANTASYDOTA_DB=mysql://root:password@localhost/yourdbname

- add environment for your steam API key e.g.
  export APIKEY=38ABCDERFHJKK99988222;

- $VENV/bin/python setup.py develop (i think this makes it so that it can import fantasydota stuff. however recently i havent bothered with this and i just add the fantasy-dota-heroes folder to my pythonpath env variable)

- $VENV/bin/initialize_fantasydota_db development.ini (this script might be out of date)

- $VENV/bin/pserve development.ini --reload

