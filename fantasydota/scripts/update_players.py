import os

import json

from fantasydota.scripts.common import all_pickees, update_pickees
from fantasydota.scripts.create_league import get_players


def main():
    filename = raw_input("filename:")
    with open(os.getcwd() + "/../data/" + filename) as f:
        players = get_players(json.load(f))

    current_players = all_pickees()
    diffs = []
    inserts = []
    seen_players = set({})
    max_id = max(p['id'] for p in current_players)
    for p in players:
        diff = {'limitTypes': []}
        is_diff = False
        current_p = next((x for x in current_players if x["name"] == p["name"]), None)
        if current_p:
            seen_players.add(p["name"])
            if current_p['limitTypes']['club'] != p['limits'][1]:
                diff['limitTypes'].append({'name': 'club', 'value': p['limits'][1]})
                is_diff = True
            if current_p['limitTypes']['position'] != p['limits'][0]:
                diff['limitTypes'].append({'name': 'position', 'value': p['limits'][0]})
                is_diff = True
            if not current_p['active']:
                is_diff = True
                diff['active'] = True

        if not current_p:
            max_id += 1
            p['id'] = max_id
            inserts.append(p)

        if is_diff:
            diff['id'] = current_p['id']
            diffs.append(diff)

    unseen_players = [x for x in current_players if x["name"] not in seen_players]
    for p in unseen_players:
        diffs.append({'id': p['id'], 'active': False})
    update_pickees(diffs, inserts)


if __name__ == "__main__":
    main()
