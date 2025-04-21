import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import REMINDER_SLEEP_TIME,NAVIGATION_WAIT_TIME,SEE_All_LINK_XPATH ,PREFERENCE_CHECK_BOX,PREFERENCE_CHECK_BOX_MORE_FOCUS,PREFERENCE_CHECK_BOX_FOCUS,BROADER_SEE_All_LINK_XPATH, PREMIUM_SEE_All_LINK_XPATH,LARGE_BANNER_WAIT_TIME
import time
import datetime

def setup_driver():
    CD_PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(CD_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => 'Batman'})")
    return driver

def login(driver):
    driver.get(os.environ.get('SH_LOGIN_URL'))
    
    username_element = driver.find_element(By.ID, 'email')
    username_element.send_keys(os.environ.get('SH_USERNAME'))
    
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(os.environ.get('SH_PASSWORD'))
    
    login_button = driver.find_element(By.ID, 'sign_in')
    login_button.click()
    time.sleep(NAVIGATION_WAIT_TIME)
    
    # Close any popups
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    time.sleep(NAVIGATION_WAIT_TIME)
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    
    time.sleep(LARGE_BANNER_WAIT_TIME)
    

def navigate_to_inbox(driver):
    # Navigate to Inbox and then Sent
    inbox_link = driver.find_element(By.LINK_TEXT, 'Inbox')
    inbox_link.click()
    time.sleep(NAVIGATION_WAIT_TIME)
    
    sent_link = driver.find_element(By.LINK_TEXT, 'Sent')
    sent_link.click()
    time.sleep(NAVIGATION_WAIT_TIME)

def navigate_to_more_matches(driver):
    # Navigate to Matches for Me
    matches_link = driver.find_element(By.LINK_TEXT, 'More Matches')
    matches_link.click()
    time.sleep(NAVIGATION_WAIT_TIME)

def navigate_to_see_all(driver,type = 1):
    LINK_XPATH = ""
    if type == 1:
        LINK_XPATH =SEE_All_LINK_XPATH
    elif type == 2:
        LINK_XPATH = BROADER_SEE_All_LINK_XPATH
    elif type == 3:
        LINK_XPATH = PREMIUM_SEE_All_LINK_XPATH
    else:
        LINK_XPATH = SEE_All_LINK_XPATH
    see_all_button = driver.find_element(By.XPATH,LINK_XPATH)
    see_all_button.click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(10)


def check_options_list(driver,type = 1):
    CHECK_BOX_LIST = ""
    if type == 1:
        CHECK_BOX_LIST =PREFERENCE_CHECK_BOX
    elif type == 2:
        CHECK_BOX_LIST = PREFERENCE_CHECK_BOX_FOCUS
    elif type == 3:
        CHECK_BOX_LIST = PREFERENCE_CHECK_BOX_MORE_FOCUS
    else:
        CHECK_BOX_LIST = PREFERENCE_CHECK_BOX
    for preference in CHECK_BOX_LIST:
        try:
            checkbox = driver.find_element(By.ID, preference)  # Select the preference one by one
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(REMINDER_SLEEP_TIME)
            checkbox.click()
            time.sleep(NAVIGATION_WAIT_TIME)
        except Exception as e:
            print(f"{datetime.datetime.now().strftime("%m-%d-%Y %H:%M")} - An error occurred: {e}")
            time.sleep(NAVIGATION_WAIT_TIME)


    