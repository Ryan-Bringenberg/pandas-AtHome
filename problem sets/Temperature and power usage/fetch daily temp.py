import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import os
import time

from selenium.webdriver.chrome.options import Options

'''
Simple function to fetch weather data from 
wunderground. Chrome driver needs to be 
downloaded and installed. The location needs
to be entered in initialization of the driver,
see below for details. 
'''

TEMP_PATH = os.path.join('datasets', 'temperatures')

def fetch_daily_temp(page, date, temp_path=TEMP_PATH):
    '''Get daily weather from wunderground
       page: wunderground URL for location of desired weather
       date: date for desired location you wish to get weather data
       temp_path: locations to saves files
    '''
    
    #configure webdrive not to open windows
    chrome_options = Options()
    chrome_options.add_argument('headless')
    
    #initialize driver
    # Change XX to the location you installed the chrome driver
    #example location: C:\Users\rab53\OneDrive\Desktop\Python\chromedriver.exe
    driver = webdriver.Chrome(r'XX', options=chrome_options)
    
    #add requested date to wunderground url
    URL = str(page) + str(date)
    driver.get(URL)
    time.sleep(4)
    r = driver.page_source
    driver.quit()
    
    #parse webpage
    soup = BS(r, 'html.parser')
    container = soup.find('lib-city-history-observation')
    check = container.find('tbody')
    
    #use pandas to get table
    try:
        df = pd.read_html(str(container))[0]
    except ValueError:
        bad_dates.append(date)
        
    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)
        
    df.to_csv(os.path.join(temp_path, f'{date}.csv'))
    
    #pause again to prevent making too many requestions, robots.txt -> 3 seconds
    time.sleep(1)