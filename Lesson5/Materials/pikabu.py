from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://pikabu.ru/')

for i in range(5):
    articles = driver.find_elements_by_tag_name('article')
    actions = ActionChains(driver)

    # actions.key_down(Keys.LEFT_CONTROL).key_down(Keys.C).key_up(Keys.LEFT_CONTROL).key_up(Keys.C)
    actions.move_to_element(articles[-1])
    actions.perform()
    time.sleep(3)