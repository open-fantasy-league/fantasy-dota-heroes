import os
import time

import json

import urllib2


def main():
    filename = raw_input("players filename:")
    with open(os.getcwd() + "/../miscdata/" + filename) as f:
        teams = json.load(f)
    for team in teams:
        for player in team["players"]:
            with open("../static/images/dota/players/{}.png".format(player["account_id"]), "wb") as f:
                time.sleep(2)
                f.write(urllib2.urlopen(
                    "https://steamcdn-a.akamaihd.net/apps/dota2/images/players/{}.png".format(player["account_id"])
                ).read())


if __name__ == "__main__":
    main()
