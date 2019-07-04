def scroll_to_bottom(driver, class_name):
    print("scrolling to bottom")
    driver.execute_script('var a = document.querySelectorAll("[class^={}]")[0]; a.scrollTop = a.scrollHeight;'.format(class_name))
