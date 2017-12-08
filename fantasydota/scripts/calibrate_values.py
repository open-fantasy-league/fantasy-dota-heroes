import json
import os

from fantasydota.lib.hero import calibrate_all_hero_values, write_calibration, calibrate_all_hero_values_datdota, \
    squeeze_values_together, manual_overrides
from fantasydota.lib.session_utils import make_session


def calibrate_values(game_id):
    session = make_session()
    write_calibration(squeeze_values_together(calibrate_all_hero_values(session, game_id)))

if __name__ == "__main__":
    game_id = 1
    calibrate_values(game_id)
