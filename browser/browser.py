import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import SEE_All_LINK_XPATH ,PREFERENCE_CHECK_BOX
import time

def setup_driver():
    CD_PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(CD_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => 'Batman'})")
    return driver

def login(driver):
    driver.get("https://www.shaadi.com/registration/user/login?go=https%3A%2F%2Fmy.shaadi.com%2Fmy-shaadi")
    
    username_element = driver.find_element(By.ID, 'email')
    username_element.send_keys(os.environ.get('SH_USERNAME'))
    
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(os.environ.get('SH_PASSWORD'))
    
    login_button = driver.find_element(By.ID, 'sign_in')
    login_button.click()
    time.sleep(10)
    
    # Close any popups
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)

def navigate_to_inbox(driver):
    # Navigate to Inbox and then Sent
    inbox_link = driver.find_element(By.LINK_TEXT, 'Inbox')
    inbox_link.click()
    time.sleep(5)
    
    sent_link = driver.find_element(By.LINK_TEXT, 'Sent')
    sent_link.click()
    time.sleep(5)

def navigate_to_more_matches(driver):
    # Navigate to Matches for Me
    matches_link = driver.find_element(By.LINK_TEXT, 'More Matches')
    matches_link.click()
    time.sleep(5)

def navigate_to_see_all(driver,type = 1):
    LINK_XPATH = ""
    if type == 1:
        LINK_XPATH =SEE_All_LINK_XPATH
    see_all_button = driver.find_element(By.XPATH,LINK_XPATH)
    see_all_button.click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

def check_options_list(driver):
    for preference in PREFERENCE_CHECK_BOX:
        checkbox = driver.find_element(By.ID, preference)  # Select the preference one by one
        checkbox.click()
        time.sleep(5)


    