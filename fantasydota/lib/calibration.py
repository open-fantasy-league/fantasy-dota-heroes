import random
import urllib2

import json
from fantasydota.lib.herodict import herodict
from fantasydota.lib.constants import API_URL
from fantasydota.lib.match import update_hero_calibration_dict
from fantasydota.scripts.get_dota_results import iterate_matches


def manual_overrides(hero_list):
    # treant = [hero for hero in hero_list if hero["name"] == "Treant Protector"][0]
    # treant["value"] = 20.0
    # underlord = [hero for hero in hero_list if hero["name"] == "Underlord"][0]
    # underlord["value"] = 14.0
    return hero_list


def squeeze_values_together(hero_values):
    # this is for if unsure and would rather have things have averagish values rather than exremes
    average_value = sum(hero_values.values()) / len(hero_values)
    for key, value in hero_values.items():
        tmp = value - ((value - average_value) / 5.)
        new_value = round(min(
            max(
                2.7 + random.randint(0, 5) / 10,
                tmp
            ),
            23.5 + random.randint(0, 6) / 10
        ), 1)
        hero_values[key] = new_value
        print "New squeezed %s: %s" % (key, new_value)
    return hero_values


def calibrate_all_hero_values(tournament_ids, tstamp_from):
    """
    :param session:
    :param game_id:
    :return:
    """
    hero_points = {_id: 0 for _id in herodict.keys()}
    hero_values = {}
    for tournament_id in tournament_ids:
        iterate_matches(
            tournament_id, update_hero_calibration_dict, tstamp_from=tstamp_from, hero_calibration_dict=hero_points
        )
    average_points = sum(hero_points.values()) / len(hero_points)
    for key, points in hero_points.items():
        # if points < 0:
        #     hero_points[key] = 1
        #     points = 1
        new_value = round(calibrate_value(average_points, points), 1)
        hero_values[key] = new_value
        print("New %s: %s" % (key, new_value))
    return hero_values


def calibrate_value(average_points, our_points):
    output = ((float(our_points) / float(average_points)) * 9.8 * 3 + 9.8) / 4.
    return output


def combine_calibrations(older_value, newer_value):
    return (newer_value + older_value * 5) / 6.


def recalibrate_hero_values(league_id):
    url = "{}pickees/leagues/{}".format(API_URL, league_id)
    update_url = "{}pickees/leagues/{}/updateCosts".format(API_URL, league_id)
    req = urllib2.Request(
        url, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'}
    )
    response = urllib2.urlopen(req)
    heroes = json.loads(response)
    print(response)
    heroes = None
    for hero in heroes:
        new_calibration = calibrate_value(average_points, hero.points)
        print "new calbration: %s, from %s" % (round(combine_calibrations(hero.value, new_calibration), 1), hero.value)
        hero.value = round(combine_calibrations(hero.value, new_calibration), 1)

