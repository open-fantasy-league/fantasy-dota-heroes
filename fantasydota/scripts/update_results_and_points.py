from fantasydota.lib.session_utils import make_session
from fantasydota.scripts.get_tournament_data import add_matches
from fantasydota.scripts.update_hero_values import update_hero_values


def main():
    session = make_session()
    add_matches(session)
    update_hero_values(session)
    with open("/home/jdog/testfile", "w+") as f:
        f.write("it worked?")

if __name__ == "__main__":
    main()
