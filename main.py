import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

from utils import process_reminders, process_messages, track_online_profiles, remove_inactive_profiles, message_from_file

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

def main():
    print("Welcome to Partner Search Automation")
    print("Choose an option:")
    print("1. Send reminders")
    print("2. Send custom message from file")
    print("3. Track online profiles")
    print("4. Remove inactive profiles")
    
    choice = input("Enter your choice (1-4): ")
    
    driver = setup_driver()
    try:
        login(driver)
        navigate_to_inbox(driver)
        
        if choice == "1":
            process_reminders(driver, By, time, 2)
        elif choice == "2":
            process_messages(driver, By, time, 4)
        elif choice == "3":
            track_online_profiles(driver, By, time, 2)
        elif choice == "4":
            remove_inactive_profiles(driver, By, time, 2)
        else:
            print("Invalid option selected")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            input("Press Enter to close the browser...")
        except KeyboardInterrupt:
            pass
        driver.quit()

if __name__ == "__main__":
    main()