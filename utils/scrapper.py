# IMPORT NECCESSARY LIB
import os
import time
from selenium.common.exceptions import NoSuchElementException, JavascriptException        
from utils.formatter import format_description_text
from utils.tweet import tweet


path = os.getcwd()
default_media = path + '/blizzard.png'


def battle_shop_scrapper(driver, WebDriverWait, By, EC):
    driver.get('https://us.shop.battle.net/en-gb/family/hearthstone')
    driver.implicitly_wait(10)

    url = None

    main_cards_container = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "main#main-content-skip-link-anchor div#start-of-content")))
    all_cards_link = main_cards_container.find_elements(By.CSS_SELECTOR, "a.ng-star-inserted")
    
 
    for index, card_url in enumerate(all_cards_link):
        tweeted = False
        with open(path +"/data/tweeted_cards.txt") as f:
            for line in f:
                if line.strip() == card_url.get_attribute('href'):
                    tweeted = True
                    break
        if tweeted:
            continue  
        else: 
            with open(path +"/data/tweeted_cards.txt", 'a') as f:
                f.write(card_url.get_attribute('href') + '\n')
            url = card_url
            break

    if url == None:
        print('No new card available at the moment')        
    else:
        scrape_card_info(driver, By, url, index)
        driver.quit()
        print('done..............')         



def scrape_card_info(driver, By, url, i):
    if 'https://us.shop.battle.net/en-gb/product' not in url.get_attribute('href'): 
        return print('Items not the regular item')

    print(i)
    driver.get(url.get_attribute('href'))
    time.sleep(10)
    
    try:
        bg_img = driver.find_element(By.CSS_SELECTOR, "div.desktop").value_of_css_property("background-image").split('"')[1]
    except:
        bg_img = driver.find_element(By.CSS_SELECTOR, "div.mobile").value_of_css_property("background-image").split('"')[1]    

    header_info = driver.find_element(By.CSS_SELECTOR, "div.product-heading")
    topic_1 = driver.find_element(By.CSS_SELECTOR, "h1.meka-font-display--header-4 > span").text
    time.sleep(0.5)

    # Check Description
    try:
        description = header_info.find_element(By.CSS_SELECTOR, "p > p").text
    except NoSuchElementException:
        description = header_info.find_element(By.CSS_SELECTOR, "p").text

   

    # Check if "Availability Element is present"
    try:
        availability = driver.find_element(By.CSS_SELECTOR, "dd.product-notification").text
    except NoSuchElementException:
        availability = 'Available'
        print("Element does not exist") 

     # Check if "Price Element is present"
    try:
        p = driver.execute_script("return document.querySelector('meka-price-label').shadowRoot.querySelector('div div div span.meka-price-label--details__standard-price')").text
        price = f"${p.split(' ')[1]}"
    except JavascriptException:
        price = 'Free'

    url = driver.current_url
    intro = '📢---New shop offer spotted---📢'

    total_len = f"{intro}\n\n⚠️ {topic_1}\n💵 {price}\n📅 {availability}\n\n\" \"\n\nSource: {url}"
    print(len(total_len))

    desc = format_description_text(description, len(total_len))

    text = f"{intro}\n\n⚠️ {topic_1}\n💵 {price}\n📅 {availability}\n\n\"{desc}\"\n\nSource: {url}"


    # UPLOAD TO TWITTER
    tweet(text, bg_img)

    print('Closing.........................')
    driver.quit()
