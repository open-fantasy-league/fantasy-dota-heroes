import json
import os
import traceback

from selenium import webdriver

chrome_opts = webdriver.ChromeOptions()
# needed because of insane ad-js on dotabuff pretty much just breaking selenium
chrome_opts.add_extension('ublock_1_11_4.crx')
driver = webdriver.Chrome(chrome_options=chrome_opts)


def main():
    driver.get("https://www.dotabuff.com/heroes/winning?date=patch_7.04")
    rows = driver.find_elements_by_xpath("//table/tbody/tr")
    old_winrates = {}
    for row in rows:
        cells = row.find_elements_by_xpath("td")
        hero = cells[1].text
        winrate = float(cells[2].get_attribute("data-value"))
        old_winrates[hero] = winrate

    driver.get("https://www.dotabuff.com/heroes/winning?date=patch_7.05")
    rows = driver.find_elements_by_xpath("//table/tbody/tr")
    win_rate_diff = {}
    for row in rows:
        cells = row.find_elements_by_xpath("td")
        hero = cells[1].text
        winrate = float(cells[2].get_attribute("data-value"))
        win_rate_diff[hero] = winrate - old_winrates[hero]
    with open(os.environ.get('FDOTA') + '/fantasydota/junk/windiff_705', 'w') as f:
        json.dump(win_rate_diff, f)

if __name__ == '__main__':
    main()
