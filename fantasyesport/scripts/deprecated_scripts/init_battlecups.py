from fantasyesport.lib.battlecup import make_battlecups
from fantasyesport.lib.session_utils import make_session


def main():
    session = make_session()
    league_id = 4979
    make_battlecups(session, league_id, 3)

if __name__ == "__main__":
    main()
