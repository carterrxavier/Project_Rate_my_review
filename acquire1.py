### Selinium script that loops through pages. trial and error process
import pandas as pd
import numpy as np
import re
import requests, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
import time 

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath('chromedriver'))
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
chromedriver = dir_path + '/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver
#list of hotels, San antonio, Austin, Dallas, Houston
#utilize page number -oa(number) - to grab the links on the first 5 pages, 30 hotels at a time
list_of_hotels = []
list_of_links = []
#initialize starting links 
oa_num = 0
san_antonio = 'https://www.tripadvisor.com/Hotels-g60956-oa{}-San_Antonio_Texas-Hotels.html'.format(oa_num)
austin = 'https://www.tripadvisor.com/Hotels-g30196-oa{}-Austin_Texas-Hotels.html'.format(oa_num)
houston = 'https://www.tripadvisor.com/Hotels-g56003-oa{}-Houston_Texas-Hotels.html'.format(oa_num)
dallas = 'https://www.tripadvisor.com/Hotels-g55711-oa{}-Dallas_Texas-Hotels.html'.format(oa_num)
list_of_hotels.append(san_antonio)
list_of_hotels.append(austin)
list_of_hotels.append(dallas)
list_of_hotels.append(houston)
#30 hotels on each page, 120 hotels in should be page 5, to add more pages, up oa_num + or - 30
while oa_num <= 180:
    for hotel in list_of_hotels:
        print(hotel)
        driver = webdriver.Chrome(executable_path=chromedriver, options=options)     
        driver.get(hotel)
        ui.WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.ID, 'BODY_BLOCK_JQUERY_REFLOW')))
        elems = driver.find_elements_by_class_name('review_count')
        for elem in elems:
            try:
                link = elem.get_attribute('href')
                index = link.find('Reviews-')
                fixed_link = link[:index + 8] + 'or0-' + link[index+8:]
                dictionary = {'links': fixed_link,'total_reviews': elem.text}
                list_of_links.append(dictionary)
            except: pass             
        driver.close()
    oa_num += 30
    list_of_hotels = []
    san_antonio = 'https://www.tripadvisor.com/Hotels-g60956-oa{}-San_Antonio_Texas-Hotels.html'.format(oa_num)
    austin = 'https://www.tripadvisor.com/Hotels-g30196-oa{}-Austin_Texas-Hotels.html'.format(oa_num)
    houston = 'https://www.tripadvisor.com/Hotels-g56003-oa{}-Houston_Texas-Hotels.html'.format(oa_num)
    dallas = 'https://www.tripadvisor.com/Hotels-g55711-oa{}-Dallas_Texas-Hotels.html'.format(oa_num)
    list_of_hotels.append(san_antonio)
    list_of_hotels.append(austin)
    list_of_hotels.append(dallas)
    list_of_hotels.append(houston)
    
all_links = pd.DataFrame(list_of_links)
all_links.to_csv('hotel_links.csv',index = False)