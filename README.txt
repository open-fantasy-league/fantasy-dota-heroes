fantasyesport README
==================

Lives at https://www.fantasyesport.eu

Next tournament planned is Kie Major starting early April
Getting Started
---------------

- Make a new python 2 virtual environment for this project

- cd <directory containing this file>

- add environment variable for database string. e.g. add this to .bashrc
  export FANTASYESPORT_DB=mysql://root:password@localhost/yourdbname

- add environment for your steam API key e.g.
  export APIKEY=38ABCDERFHJKK99988222;

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_fantasyesport_db development.ini

- $VENV/bin/pserve development.ini

