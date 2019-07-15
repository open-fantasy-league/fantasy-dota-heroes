import time

import json
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

#$x("//*[@id='First-team_squad']/../../table[3]//tr")
from selenium.webdriver import DesiredCapabilities

from fantasydota.scripts.common import simplify_team_names

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

def get_fixtures():
    fixtures = []
    driver = webdriver.Firefox(capabilities=firefox_capabilities)
    driver.set_page_load_timeout(10)
    link = "https://www.flashscore.com/football/england/premier-league/fixtures/"
    try:
        driver.get(link)
    except TimeoutException:
        pass
    time.sleep(60)
    rows = driver.find_elements_by_xpath("//table[@class='soccer']/tbody/tr")
    round = 0
    period_starts = []
    first_match_of_round = True
    for row in rows:
        if row.get_attribute('class') == 'event_round':
            round += 1
            first_match_of_round = True
        else:
            columns = row.find_elements_by_tag_name('td')
            kickoff_dt = datetime.strptime('2020.' + columns[1].text, '%Y.%d.%m. %H:%M')
            kickoff_dt = kickoff_dt.replace(year=2020) if kickoff_dt.month <= 7 else kickoff_dt.replace(year=2019)
            kickoff_str = kickoff_dt.strftime('%Y:%m:%d %H:%M')
            if first_match_of_round:
                period_starts.append(kickoff_str)
            team_one = columns[2].text
            team_two = columns[3].text
            fixtures.append((simplify_team_names(team_one), simplify_team_names(team_two), kickoff_str))
            first_match_of_round = False
    return {'fixtures': fixtures, 'period_starts': period_starts}


if __name__ == "__main__":
    data = get_fixtures()
    with open('fixtures.json', 'w+') as f:
        f.write(json.dumps(data))
