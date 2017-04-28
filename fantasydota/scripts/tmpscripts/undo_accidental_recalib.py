import json

from fantasydota.models import Hero

from fantasydota.lib.session_utils import make_session


def hmmm():
    session = make_session(False)
    with open("/home/johnny/oldvals.json", "r") as f:
        heroes = json.load(f)
    for hero in session.query(Hero).all():
	old_val = [h["value"] for h in heroes if h["id"] == hero.id][0]
	hero.value = old_val
	print "would set %s: %f to %f" % (hero.name, hero.value, old_val)
    session.commit()
	

def main():
    hmmm()

if __name__ == "__main__":
    main()
