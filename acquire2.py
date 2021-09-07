### Selinium script that loops through pages
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
import datetime

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath('chromedriver'))
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
chromedriver = dir_path + '/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver

df = pd.DataFrame()
if os.path.isfile('hotel_links_continued.csv'):
    df = pd.read_csv('hotel_reviews.csv')
    print("Continuing where left off")
    links = pd.read_csv('hotel_links_continued.csv')
else:
    links = pd.read_csv('hotel_links.csv')
    links = links.drop_duplicates()
#will convert reviews to int once, with
try:
    links.total_reviews = links['total_reviews'].str.split(' ', n=1 , expand= True)[0]
    links.total_reviews = links.total_reviews.str.replace(',','')
    links.total_reviews = links.total_reviews.astype(int)
except: pass

for link in range(len(links)):
    list_of_reviews = []
    index = 0
    page_num = 1
    url = links.links[link]
    driver = webdriver.Chrome(executable_path=chromedriver, options = options)
    driver.get(url)
    hotel_name = driver.find_element_by_class_name('_1mTlpMC3').text
    hotel_city_split = driver.find_element_by_class_name('breadcrumbs').text.split(" ")
    if hotel_city_split[6] == "San":
        hotel_city = 'San Antonio'
    else:
        hotel_city = hotel_city_split[6]
    print('Currently scraping {}'.format(hotel_name))
    while index <= links.total_reviews[link] / 5:
        if index <= 30:
            print('Review page {}'.format(page_num))
            inner_driver = webdriver.Chrome(executable_path=chromedriver, options = options)
            inner_driver.get(url)
            
            reviews = inner_driver.find_elements_by_class_name("_2wrUUKlw._3hFEdNs8")
            for review in reviews:
                rating_num = 0
                rating = review.find_element_by_class_name('nf9vGX55')
                if len(rating.find_elements_by_class_name('ui_bubble_rating.bubble_50')) == 1:
                    rating_num = 5
                elif len(rating.find_elements_by_class_name('ui_bubble_rating.bubble_40')) == 1:
                    rating_num = 4
                elif len(rating.find_elements_by_class_name('ui_bubble_rating.bubble_30')) == 1:
                    rating_num = 3
                elif len(rating.find_elements_by_class_name('ui_bubble_rating.bubble_20')) == 1:
                    rating_num = 2
                elif len(rating.find_elements_by_class_name('ui_bubble_rating.bubble_10')) == 1:
                    rating_num = 1
                else:
                    rating_num = 0
                
                
                review_text = review.find_element_by_class_name('cPQsENeY').text
                try:
                    date_of_stay = review.find_element_by_class_name('_34Xs-BQm').text
                except:
                    date_of_stay = np.nan
                
                dictionary = {'hotel_name': hotel_name,\
                              'hotel_city': hotel_city,\
                              'date_of_stay': date_of_stay,\
                              'review_rating': rating_num,\
                              'review': review_text}  
                
                list_of_reviews.append(dictionary)
   
            inner_driver.close()
            
            current_page = '-or{}-'.format(index)
            next_page = '-or{}-'.format(index + 5)
            url = url.replace(current_page, next_page)
            index += 5
            page_num += 1
        else:
            break
    df = df.append(list_of_reviews)
    df.to_csv('hotel_reviews.csv', index=False)
    links = links.iloc[1: , :]
    links.to_csv('hotel_links_continued.csv',index=False)
    print('{} links to go'.format(len(links)))
    
    driver.close()