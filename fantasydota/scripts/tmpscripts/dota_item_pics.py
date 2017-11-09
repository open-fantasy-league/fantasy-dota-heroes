# import time
#
# import json
#
# import urllib.request
# from selenium import webdriver
#
# chrome_opts = webdriver.ChromeOptions()
# # needed because of insane ad-js on dotabuff pretty much just breaking selenium
# chrome_opts.add_extension('ublock_1_11_4.crx')
# driver = webdriver.Chrome(chrome_options=chrome_opts)
#
#
# def main():
#     driver.get("https://www.dota2.com/items/")
#     items = driver.find_elements_by_xpath("//div[@itemname]")
#     for item in items:
#         name = item.get_attribute("itemname")
#         src = item.find_element_by_xpath("./img").get_attribute("src")
#         print(src)
#         urllib.request.urlretrieve(str(src), "/home/jdog/projects/fantasy-dota-heroes/fantasydota/static/images/dota/items/%s.png" % name)
#
# if __name__ == '__main__':
#     try:
#         main()
#     except:
#         import pdb;
#         pdb.set_trace()
