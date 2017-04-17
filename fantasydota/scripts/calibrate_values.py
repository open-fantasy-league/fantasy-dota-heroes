import json
import os

from fantasydota.lib.hero import calibrate_all_hero_values, write_calibration, calibrate_all_hero_values_datdota, \
    squeeze_values_together, manual_overrides
from fantasydota.lib.session_utils import make_session


def main():
    kiev_major = True  # have to do some funky calibrating due to patch coming right before tournament
    session = make_session()
    if kiev_major:
        patch7_04 = calibrate_all_hero_values_datdota(session, "7_04")
        with open(os.environ.get('FDOTA') + "/fantasydota/junk/windiff_705", "r") as f:
            pub_win_diffs = json.load(f)
        for hero in patch7_04:
            for key, val, in pub_win_diffs.iteritems():
                if ''.join([i for i in hero["name"].lower() if i.isalpha()]) == ''.join([i for i in key.lower() if i.isalpha()]):
                    win_diff = val
                #win_diff = pub_win_diffs[''.join([i for i in hero["name"].lower() if i.isalpha()])]
            hero["value"] *= (1 + (win_diff / 2.))
        patch7_05 = calibrate_all_hero_values_datdota(session, "7_05")
        for hero in patch7_05:
            hero["value"] = (hero["value"] * 3 + [h for h in patch7_04 if h["id"] == hero["id"]][0]["value"]) /4.
        write_calibration(squeeze_values_together(manual_overrides(patch7_05)))
    else:
        write_calibration(calibrate_all_hero_values(session))

if __name__ == "__main__":
    main()
