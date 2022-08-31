# IMPORT NECCESSARY LIB
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.scrapper import battle_shop_scrapper

# CONFIG FOR DEVELOPMENT ENV
PATH = "C:\Program Files (x86)\chromedriver.exe"    # Replace with your chromedriver path 

# CONFIG FOR PRODUCTION ENV
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")


while True:
    driver = webdriver.Chrome(PATH)               # CONFIG FOR DEVELOPMENT ENV 
    # driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    print('Scraping shop.battle.net...........................')
    battle_shop_scrapper(driver, WebDriverWait, By, EC)

    # Sleep for 1 min then continue
    time.sleep(60)

