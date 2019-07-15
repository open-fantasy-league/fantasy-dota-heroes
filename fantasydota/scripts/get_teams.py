import os
import time

import json
from datetime import datetime

from fantasydota.scripts.common import simplify_team_names
from selenium_utils import scroll_to_bottom
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

def get_data():
    driver = webdriver.Firefox(capabilities=firefox_capabilities)
    driver.set_page_load_timeout(10)
    league_link = "https://www.fotmob.com/leagues/47/"
    teams = []
    try:
        driver.get(league_link)
    except TimeoutException:
        pass
    team_urls = []
    for team_row in driver.find_elements_by_xpath('//div[starts-with(@class, "tablestyled__TableLeagueTeamlogo")]/following-sibling::a'):
        team_urls.append((simplify_team_names(team_row.text), team_row.get_attribute("href")))
    for (team_name, team_url) in team_urls:
        time.sleep(5)
        team = []
        driver.get(team_url)

        time.sleep(15)
        len_player_rows = 0
        while len_player_rows == 0:
            len_player_rows = len(driver.find_elements_by_xpath(
                '//ul[@class="fm-team__list"][{}]//div[@class="fm-team__list__description"]'.format(1)
            ))
            driver.find_element_by_xpath("//a[text()='SQUAD']").click()
            time.sleep(4)
            scroll_to_bottom(driver, "fm-content")
        for i, pos in enumerate(['Goalkeeper', 'Defender', 'Midfielder', 'Forward']):
            while True:
                scroll_to_bottom(driver, "fm-content")
                player_rows = driver.find_elements_by_xpath(
                    '//ul[@class="fm-team__list"][{}]//div[@class="fm-team__list__description"]'.format(i+1)
                )
                try:
                    assert len(player_rows) > 0
                    assert all(p.text for p in player_rows)
                except:
                    print("len(player_rows) > 0", len(player_rows) > 0)
                    print([p.text for p in player_rows])
                    #import pdb; pdb.set_trace()
                    continue
                else:
                    break
            for player in player_rows:
                    name = player.text
                    team.append((name, pos))
        teams.append((team_name, team))
    return teams


if __name__ == "__main__":
    data = get_data()
    #import pdb; pdb.set_trace()
    try:
        with open(os.getcwd() + '/../data/players_{}.json'.format(datetime.now().date()), 'w+') as f:
            f.write(json.dumps(data))
    except:
        import pdb;
        pdb.set_trace()
