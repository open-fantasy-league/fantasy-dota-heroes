from fantasyesport.lib.hero import calibrate_all_hero_values
from fantasyesport.lib.session_utils import make_session


def main():
    session = make_session()

    calibrate_all_hero_values(session)

if __name__ == "__main__":
    main()
