# Un nou script de afiliere pentru folos intern; 
#
###############################################
#
#   Author: Andrei C. Cojocaru
#   LinkedIn: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#   Site: webautomation.ro && ideisioferte.ro
#
###############################################
# 
#
#
# import needed libaries; 
#
import requests
from bs4 import BeautifulSoup 
#
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
#
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
from time import sleep
import csv
import pandas as pd
#
from fake_useragent import UserAgent 
#
import pickle # for loaded cookie session;
#
# import libraries for beautiful introduction screen;
#
from termcolor import colored
from pyfiglet import Figlet
from pyfiglet import figlet_format
#
#
######################################################################


############################## ---> the logic of code <--- ###########
#
def configure_driver():

    options = webdriver.FirefoxOptions()

    # declare a user_agent variable; 
    user_agent = UserAgent()

    options.set_preference("general.useragent.override", user_agent.random) # random UserAgent;
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headles = False # if True, browser don't show;

    # declare a firefox; 
    firefox_service = Service(executable_path='path-ul-catre-firefixul-tau') # <--------------- Aici introduci pathul catre driverul tau.

    # set new driver; 
    driver = webdriver.Firefox(service=firefox_service, options=options)

    return driver


# return a soup object with one function; 
#
def get_affiliate_links(driver, keyword: str):

    try:

        driver.get('https://www.libris.ro')

        # pickle.dump(driver.get_cookies(), open('libris_cookies', 'wb')) <------- Intai de toate inscrii cookies;

        # load cookies;
        #for cookie in pickle.load(open('libris_cookies', 'rb')): <--------------- Dupa care face load la cookies;
            #driver.add_cookie(cookie)

        # check if cookie load;
        print("Cookie loaded!")
        sleep(1)

        # input label and click;
        input_label = driver.find_element(By.ID, 'autoComplete').send_keys(keyword)
        input_click = driver.find_element(By.ID, 'autoCompleteButton').click()
        sleep(2)
        
        new_soup = BeautifulSoup(driver.page_source, 'lxml')
        product_list = new_soup.find('div', class_='products-list').find_all('div', class_='pr-history-item')
        
        # try to return a list of links; 
        lst_of_afiliate_links = []
        for item in product_list: 
            link = item.find('a').get('href')
            
            try: 
                price = item.find('div', class_='item-price').find_all('p')[0].text
                price = price[0:5] + ' lei'
            except:
                price = '-'

            title = item.find('div', class_='item-title').find('h2', class_='pr-title-categ-pg').text

            affiliate_link = 'link-ul-tau-unic-de-afiliere' + 'www.libris.ro' + link # <-------------- Creezi link-ul tau unic de afiliere;

            lst_of_afiliate_links.append([title, affiliate_link, price])


        header = ['title', 'affiliate_link', 'price']
        df = pd.DataFrame(lst_of_afiliate_links, columns = header)
        df.to_csv(f"cartile-lui-{keyword}.csv", encoding="utf8")
        print('Done!')   

    except Exception as ex: 
        print(ex)

    finally: 
        sleep(5)
        driver.quit()
    
    

# def main function ----> for all logic of code; 
#
def main():

    # beautiful screen introduction;
    introduction = Figlet(font = 'big')
    print(colored(introduction.renderText('Powered by:'), 'green'))
    print(figlet_format("webautomation.ro", font = "banner3", width = 600))

    keword_from_user = input('Ce vrei sa cauti pe libris.ro?: ')

    if keword_from_user:
        driver = configure_driver()
        get_affiliate_links(driver, keword_from_user)
    else: 
        print('Ceva nu a reusit!')


if __name__ == "__main__":
    main()
    
