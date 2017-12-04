import json
import os

from fantasydota.lib.hero import calibrate_all_hero_values, write_calibration, calibrate_all_hero_values_datdota, \
    squeeze_values_together, manual_overrides
from fantasydota.lib.session_utils import make_session


def calibrate_values():
    session = make_session()
    write_calibration(squeeze_values_together(calibrate_all_hero_values(session, patch=False)))

if __name__ == "__main__":
    calibrate_values()
