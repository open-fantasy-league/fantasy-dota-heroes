import json

from fantasydota.scripts.common import all_pickees, update_pickees
from fantasydota.scripts.create_league import get_players


def main():
    filename = raw_input("filename:")
    with open(filename) as f:
        players = get_players(json.load(f))

    current_players = all_pickees()
    diffs = []
    for p in players:
        diff = {'limitTypes': {}}
        is_diff = False
        current_p = next((x for x in current_players if x.name == p["name"]), None)
        if current_p:
            if current_p['limitTypes']['club'] != p['limits'][1]:
                diff['limitTypes']['club'] = p['limits'][1]
                is_diff = True
            if current_p['limitTypes']['position'] != p['limits'][0]:
                diff['limitTypes']['position'] = p['limits'][0]
                is_diff = True

        if not current_p:
            diff['active'] = False
            is_diff = True

        if is_diff:
            diff['id'] = current_p['id']
            diffs.append(diff)
    update_pickees(diffs)


if __name__ == "__main__":
    main()
