import time

import json
from datetime import datetime

import re
from selenium_utils import scroll_to_bottom
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver import DesiredCapabilities

from fantasydota.scripts.add_game_manually import add_game

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'


def process_match(driver):
    home, away = [x.text for x in
                  driver.find_elements_by_xpath("//*[starts-with(@class, 'match-headerstyles__MatchHeaderTeamTitle')]")]
    match_data = {
        "tournamentId": 1,
        "teamOne": home,
        "teamTwo": away,
        "teamOneGoals": [
        ],
        "teamTwoGoals": [
        ],
        "teamOnePlayers": [],
        "teamTwoPlayers": [],
        "yellowCards": [],
        "redCards": [],
        "penaltyMiss": {"teamOne": [], "teamTwo": []}
    }

    home_goals = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event--home')][div/div/div[contains(@class,'fm-svg--goal')]]"
    )
    away_goals = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event--away')][div/div/div[contains(@class,'fm-svg--goal')]]"
    )
    for goal in home_goals:
        scorer = goal.find_element_by_xpath("div[2]/span/a").text.split("(")[0]
        assist = goal.find_element_by_xpath(".//*[@class='fm-match-event__assist']")
        assist = re.search("assist by (.*)", assist.text).groups()[0] if assist and assist.text else None
        gtime = int(re.search("^\d+",
                          goal.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        match_data['teamOneGoals'].append({"min": gtime, "scorer": scorer, "assist": assist})

    for goal in away_goals:
        scorer = goal.find_element_by_xpath("div[2]/span/a").text.split("(")[0]
        assist = goal.find_element_by_xpath(".//*[@class='fm-match-event__assist']")
        assist = re.search("assist by (.*)", assist.text).groups()[0] if assist and assist.text else None
        gtime = int(re.search("^\d+",
                          goal.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        match_data['teamTwoGoals'].append({"min": gtime, "scorer": scorer, "assist": assist})
    yellows = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event')][div/div/div[contains(@class,'fm-svg--yellowcard')]]"
    )
    for yellow in yellows:
        ytime = int(re.search("^\d+",
                          yellow.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        name = yellow.find_element_by_xpath("div[2]/span/a").text.strip(" ")
        match_data['yellowCards'].append(name)

    reds = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event')][div/div/div[contains(@class,'fm-svg--redcard')]]"
    )
    for event in reds:
        time_ = int(re.search("^\d+",
                          event.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        name = event.find_element_by_xpath("div[2]/span/a").text.strip(" ")
        match_data['redCards'].append([name, time_])

    team_one_penalty_miss = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event--home')][div/div/div[contains(@class,'fm-svg--penaltymiss')]]"
    )
    for event in team_one_penalty_miss:
        time_ = int(re.search("^\d+",
                          event.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        name = event.find_element_by_xpath("div[2]/span/a").text.strip(" ")
        match_data['penaltyMiss']['teamOne'].append([name, time_])

    team_two_penalty_miss = driver.find_elements_by_xpath(
        "//*[contains(@class, 'MatchFactsContainer')]//*[contains(@class, 'fm-match-event--away')][div/div/div[contains(@class,'fm-svg--penaltymiss')]]"
    )
    for event in team_two_penalty_miss:
        time_ = int(re.search("^\d+",
                          event.find_element_by_xpath(".//*[contains(@class, 'fm-match-event__time')]").text).group(0))
        name = event.find_element_by_xpath("div[2]/span/a").text.strip(" ")
        match_data['penaltyMiss']['teamTwo'].append([name, time_])

    added_time = int(re.search(
        "\+(\d+) minutes? added",
        driver.find_element_by_xpath("//*[starts-with(@class, 'match-factsstyles__AddedTimeContainer')]").text).groups()[0])
    raw_input("now switch to lineup")
    for i, starting_player in enumerate(driver.find_elements_by_xpath("//*[@class='fm-lineup__player']")):
        name = starting_player.find_element_by_xpath(".//*[starts-with(@class, 'lineupstyles__LineupPlayerName')]").text
        rating = float(
            starting_player.find_element_by_xpath(".//*[starts-with(@class, 'fm-lineup__player__rating')]").text)
        sub_off = starting_player.find_elements_by_xpath(".//*[starts-with(@class, 'lineupstyles__LineupSubTime')]")
        sub_off = int(re.search("^\d+", sub_off[0].text).group(0)) if len(sub_off) and sub_off[0].text else 90 + added_time
        if i <= 10:
            match_data["teamOnePlayers"].append([name, 0, sub_off, rating])
        else:
            match_data["teamTwoPlayers"].append([name, 0, sub_off, rating])

    # Away
    for sub in driver.find_elements_by_xpath(
            "//*[starts-with(@class, 'lineupstyles__LineupSubsAway')]//div[@class='fm-substitutes__player']"
    ):
        try:
            sub_on = sub.find_element_by_xpath(".//*[starts-with(@class, 'lineupstyles__LineupSubTime')]")
        except NoSuchElementException:
            continue
        if sub_on:
            name = sub.find_element_by_xpath(".//*[starts-with(@class, 'lineupstyles__LineupPlayerName')]").text
            try:
                rating = float(sub.find_element_by_xpath(".//*[starts-with(@class, 'fm-lineup__player__rating')]").text)
            except (NoSuchElementException, ValueError):
                rating = 0.0  # they came on too late to be rated
            match_data["teamTwoPlayers"].append([name, int(re.search("^\d+", sub_on.text).group(0)), 90+added_time, rating])

    # Home
    for sub in driver.find_elements_by_xpath(
            ".//*[starts-with(@class, 'lineupstyles__LineupSubsHome')]//div[@class='fm-substitutes__player']"
    ):
        try:
            sub_on = sub.find_element_by_xpath(".//*[starts-with(@class, 'lineupstyles__LineupSubTime')]")
        except NoSuchElementException:
            continue
        if sub_on:
            name = sub.find_element_by_xpath(
                ".//*[starts-with(@class, 'lineupstyles__LineupPlayerName')]").text
            try:
                rating = float(
                    sub.find_element_by_xpath(".//*[starts-with(@class, 'fm-lineup__player__rating')]").text)
            except (NoSuchElementException, ValueError):
                rating = 0.0  # they came on too late to be rated
            match_data["teamOnePlayers"].append([name, int(re.search("^\d+", sub_on.text).group(0)), 90+added_time, rating])
    return match_data


def data_listener():
    driver = webdriver.Firefox(capabilities=firefox_capabilities)
    driver.set_page_load_timeout(10)
    league_link = "https://www.fotmob.com/leagues/47/"
    try:
        driver.get(league_link)
    except TimeoutException:
        pass
    while True:
        raw_input("Wait to load match")
        scroll_to_bottom(driver)
        match_data = process_match(driver)
        print(match_data)
        raw_input("this look fine?: ")
        add_game(match_data)


if __name__ == "__main__":
    data_listener()
