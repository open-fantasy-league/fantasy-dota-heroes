import json

from fantasydota.models import Hero

from fantasydota.lib.session_utils import make_session


def hmmm():
    session = make_session()
    heroes = []
    for hero in session.query(Hero).all():
        heroes.append({"id": hero.id,
                       "value": hero.value})
    with open("/home/jdog/projects/fantasy-dota-heroes/fantasydota/junk/oldvals", "w") as f:
        json.dump(heroes, f)


def main():
    hmmm()

if __name__ == "__main__":
    main()