from fantasyesport.lib.session_utils import make_session
from fantasyesport.scripts.get_tournament_data import add_matches
from fantasyesport.scripts.update_hero_points import update_hero_points


def main():
    session = make_session()
    add_matches(session)
    update_hero_values(session)
    with open("/home/jdog/testfile", "w+") as f:
        f.write("it worked?")

if __name__ == "__main__":
    main()
