import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

from utils import *

reminderMessage = message_from_file('reminder.txt')
print(reminderMessage)

print(f"Hello,Nice to meet you.")
print(f"Choose the option from below.")
print(f"1.Send reminders.")
print(f"2.Send custom message from the file.")
print(f"3.Remove Inactive Profiles.")
print(f"4.Remove Inactive Profiles by xpath.")
print(f"5.Get the count of the total online.")

number = input("What's your choice?")


CD_PATH = "C:\Program Files (x86)\chromedriver.exe"

# Initialize ChromeDriver 
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Exclude automation switch
options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension
service = Service(CD_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Execute JavaScript to modify navigator.webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => 'Batman'})")

driver.get("https://www.shaadi.com/registration/user/login?go=https%3A%2F%2Fmy.shaadi.com%2Fmy-shaadi")

# Locate the username input element and enter the username
username_element = driver.find_element(By.ID, 'email')
un = os.environ.get('SH_USERNAME')
username_element.send_keys(un)

# Locate the password input element and enter the password
password_element = driver.find_element(By.ID, 'password')
ps = os.environ.get('SH_PASSWORD')
password_element.send_keys(ps)

# Locate and click the login button
click_button_with_id(driver,By,'sign_in',time,10)

# Press the "Esc" key on the entire window
driver.switch_to.active_element.send_keys(Keys.ESCAPE)

# Press the "Esc" key on the entire window
driver.switch_to.active_element.send_keys(Keys.ESCAPE)


# Find and click the link with the exact text "Specific Link Text"
click_link_with_text(driver,By,'Inbox',time,5)

# Find and click the link with the exact text "Specific Link Text"
click_link_with_text(driver,By,'Sent',time,5)

# Locate and click the custom-Not Viewed by them button
#click_button_with_id(driver,By,'custom-Not Viewed by them',time,10)

sleepTime = 2
if number == "1":
    click_remind_and_sendreminder(driver,By,time,sleepTime,number)
elif number == "2":
    reminderMessage = message_from_file('reminder.txt')
    sleepTime = 8
    send_message_to_profiles(driver,By,time,sleepTime,number)
elif number == "3":
    remove_inactive_profiles(driver,By,time,sleepTime,number)
elif number == "4":
    remove_inactive_profiles_using_xpath(driver,By,time,sleepTime,number)
else:
    print("Option invalid. Please re-run.")

# Keep the browser open
try:
    print("Press Ctrl+C to close the browser...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Close the browser when the script is manually interrupted
    driver.quit()