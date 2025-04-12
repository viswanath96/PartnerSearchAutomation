from datetime import datetime
import inspect
import json
from Schedule import Schedule
# utils.py

# Data to be written
data = [
    {"day": "Tuesday",
    "date": "4/1/2025",
    "count": [{"12:00":"0"}]
    }
    ]


#Click link with text and sleep timer
def click_link_with_text(driver,By,link_text,time,sleepTime):
    # Find and click the link with the exact text "Specific Link Text"
    link_element = driver.find_element(By.LINK_TEXT, link_text)
    link_element.click()
    time.sleep(sleepTime)

#Click link with text and sleep timer
def click_button_with_id(driver,By,button_id,time,sleepTime):
    # Locate and click the login button
    login_button = driver.find_element(By.ID, button_id)
    login_button.click()
    time.sleep(sleepTime)


#Click the Remind and Send Reminder button
def click_remind_and_sendreminder(driver,By,time,sleepTime):
    # Find all buttons with the specific text "Button Text"
    buttons = driver.find_elements(By.XPATH, '//button[text()="Remind"]')

    # Iterate through the list of buttons and click each one
    for button in buttons:
        # Scroll the element to the middle of the screen using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        if button.is_enabled():
            # Button is enabled, click it
            button.click()
            time.sleep(sleepTime)
            # Find buttons with the specific text "Button Text"
            reminder_button = driver.find_elements(By.XPATH, '//button[text()="Send Reminder"]')
            # Check if any buttons with the specific text exist        
            reminder_button[0].click()
            time.sleep(sleepTime)
        time.sleep(sleepTime)

#Read the message from the file and return the text
def message_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except IOError:
        return "An error occurred while reading the file."

#Click the Remind and Send Reminder button
def click_remind_and_sendreminder(driver,By,time,sleepTime,number):
    # Find all buttons with the specific text "Button Text"
    buttons = driver.find_elements(By.XPATH, '//button[text()="Remind"]')

    # Iterate through the list of buttons and click each one
    for button in buttons:
        # Scroll the element to the middle of the screen using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        # Try to find and click the button
        try:
            button.click()
            time.sleep(sleepTime)
            # Find buttons with the specific text "Button Text"
            reminder_button = driver.find_elements(By.XPATH, '//button[text()="Send Reminder"]')
            # Check if any buttons with the specific text exist        
            reminder_button[0].click()
            time.sleep(sleepTime)
        except Exception as e:
            # Catch all exception types and do nothing
            print(f"An exception occurred: {e}. Skipping click.")

        time.sleep(sleepTime)
    
    click_next_and_remind_and_sendreminder(driver,By,time,2,number)

#Click next and then click the Remind and Send Reminder button 'Next→'

def click_next_and_remind_and_sendreminder(driver,By,time,sleepTime,number):
    # Find all buttons with the specific text "Button Text"
    try:
        next_button = driver.find_elements(By.XPATH, '//button[contains(text(), "Next")]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button[0])
        # Check if any buttons with the specific text exist        
        next_button[0].click()
        time.sleep(sleepTime)
    except Exception as e:
    # Catch all exception types and do nothing
        print(f"An exception occurred: {e}. Skipping click.")
        return
    if number == "1":
        click_remind_and_sendreminder(driver,By,time,sleepTime,number)
    elif number == "2":
        send_message_to_profiles(driver,By,time,sleepTime,number)
    elif number == "3":
        remove_inactive_profiles(driver,By,time,sleepTime,number)
    elif number == "4":
        remove_inactive_profiles_using_xpath(driver,By,time,sleepTime,number)
    elif number == "5":
        Get_the_count_of_the_total_online(driver,By,time,sleepTime,number)

#Send message instead of a reminder
def send_message_to_profiles(driver,By,time,sleepTime,number):
    reminderMessage = message_from_file('reminder.txt')
    # Find all buttons with the specific text "Button Text"
    links = driver.find_elements(By.XPATH, '//a[text()="Read More"]')

    # Iterate through the list of links and click each one
    for link in links:
        # Try to find and click the button
        try:
            # Scroll the element to the middle of the screen using JavaScript
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            
            link.click()
            time.sleep(sleepTime)

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])

            # Find links with the specific text "Button Text"
            write_message_button = driver.find_elements(By.XPATH, '//button[text()="Write Message"]')[0]
            write_message_button.click()
            time.sleep(sleepTime)
            # Find input with the specific place holder text
            text_field = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[3]/div[2]/div[1]/section/form/input[3]')[0]
            text_field.send_keys(reminderMessage)
            text_field.submit()
            time.sleep(sleepTime)
            # Find links with the specific text "Button Text"
            close_message_button = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[3]/div[2]/div[1]/section/div[1]/div/button[2]')[0]
            close_message_button.click()
            time.sleep(sleepTime)
            #close the new open tab
            driver.close()
            # Switch to the old tab
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(sleepTime)
            # Check if any links with the specific text exist        
        except Exception as e:
            # Catch all exception types and do nothing
            print(f"An exception occurred: {e}. Skipping click.")
             #close the new open tab
            driver.close()
            # Switch to the old tab
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(sleepTime)
            # Check if any links with the specific text exist  
            continue
    
    click_next_and_remind_and_sendreminder(driver,By,time,sleepTime,number)

    
#Remove inactive profiles
def remove_inactive_profiles(driver,By,time,sleepTime,number):
    # Find all buttons with the specific text "Button Text"
    links = driver.find_elements(By.XPATH, '//a[text()="Read More"]')

    # Iterate through the list of links and click each one
    for link in links:
        # Scroll the element to the middle of the screen using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        # Try to find and click the button
        try:
            link.click()
            time.sleep(sleepTime)

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])


            # Find links with the specific text "Button Text"
            online_now_text = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/span')[0]
            
            if online_now_text.text == "Online now":
                print("Online now so skip")
            else:            
                activity_text = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/span[2]')[0]
                if activity_text.text == "Online 2w ago" or activity_text.text == "Online 1w ago":
                    down_button = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/button')[0]
                    down_button.click()
                    time.sleep(1)
                    cancel_button = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/button')[0]
                    cancel_button.click()
                    time.sleep(sleepTime)
            
            #close the new open tab
            driver.close()
            # Switch to the old tab
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(sleepTime)
            # Check if any links with the specific text exist        
        except Exception as e:
            # Catch all exception types and do nothing
            print(f"An exception occurred: {e}. Skipping click.")
    
    click_next_and_remind_and_sendreminder(driver,By,time,sleepTime,number)

#Use relative XPATH for cancel reminders
def remove_inactive_profiles_using_xpath(driver,By,time,sleepTime,number):
    
    profile_container_xpath = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'
    container_div = driver.find_element(By.XPATH, profile_container_xpath)
    profile_divs = container_div.find_elements(By.XPATH, './div')

    # Iterate through the list of links and click each one
    for profile in profile_divs:
        # Scroll the element to the middle of the screen using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
        time.sleep(sleepTime)
        
        try:
            dropdown_button_xpath = './/*[@data-test-selector="listDropdown"]'
            dropdown_button = profile.find_element(By.XPATH, dropdown_button_xpath)

            if dropdown_button:
                chat_now_button_xpath = './/*[@title="Chat Now"]'
                status_text_element = profile.find_element(By.XPATH, chat_now_button_xpath)
                if status_text_element.text == "Online 2w ago" or status_text_element.text == "Online 1w ago":
                    print(status_text_element.text)
                    time.sleep(sleepTime)
                    dropdown_button.click()
                    cancel_button_xpath = './/*[@data-test-selector="cancelInvitationInboxPage"]'
                    cancel_button = profile.find_element(By.XPATH, cancel_button_xpath)
                    cancel_button.click()
                    time.sleep(sleepTime)
                else:
                    print(f"Profile {status_text_element.text}")
            else:
                print("Profile deactivated")
        except Exception as e:
            # Catch all exception types and do nothing
            print(f"An exception occurred: {e}. Skipping click.")

    click_next_and_remind_and_sendreminder(driver,By,time,sleepTime,number)


#Use relative XPATH for getting the count of the total online
def Get_the_count_of_the_total_online(driver,By,time,sleepTime,number):
    
    profile_container_xpath = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'
    container_div = driver.find_element(By.XPATH, profile_container_xpath)
    profile_divs = container_div.find_elements(By.XPATH, './div')
    data = handle_json_read("data.json")
    print(data)
    # Iterate through the list of links and click each one
    for profile in profile_divs:
        # Scroll the element to the middle of the screen using JavaScript
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
        time.sleep(sleepTime)
        
        try:
            dropdown_button_xpath = './/*[@data-test-selector="listDropdown"]'
            dropdown_button = profile.find_element(By.XPATH, dropdown_button_xpath)

            if dropdown_button:
                chat_now_button_xpath = './/*[@title="Chat Now"]'
                status_text_element = profile.find_element(By.XPATH, chat_now_button_xpath)
                if status_text_element.text == "Online now":
                    print(status_text_element.text)
                    # Get the current date and time
                    now = datetime.now()
                    # Display the results
                    print(f"Current Hour (24): {now.strftime("%H")}") # 24-hour format
                    print(f"Current Day: {now.strftime("%A")}") # Full day name
                    print(f"Current Date (MM-DD-YYYY): {now.strftime("%m-%d-%Y")}") # Month-Day-Year format
                    # Query and update
                    # Specify the time key to check
                    date_key = now.strftime("%m-%d-%Y")
                    time_key = now.strftime("%H")
                    found_date = False
                    for datum in data:
                        if datum["date"] == date_key:
                            today = datum
                            occurances = today.occurance
                            found_date = True
                            found_hour = False
                            for occurance in occurances:
                                if occurance["hour"] == time_key:
                                    occurance["count"] +=1
                                    found_hour = True
                                    break
                            if not found_hour:
                                occurances.append({"hour":now.strftime("%H"), "count":1})
                                break
                            break
                    if not found_date:
                        new_schedule = Schedule(day=now.strftime("%A"),date=now.strftime("%m-%d-%Y"),occurance=[{"hour": now.strftime("%H"), "count": 1}])
                        data.append(new_schedule)

                    time.sleep(sleepTime)
                else:
                    print(f"Profile {status_text_element.text}")
            else:
                print("Profile deactivated")
        except Exception as e:
            # Catch all exception types and do nothing
            print(f"An exception occurred: {e}. Skipping click.")

    click_next_and_remind_and_sendreminder(driver,By,time,sleepTime,number)


# Writing to a JSON file
with open("data.json", "w") as file:
    json.dump(data, file, indent=4)  # `indent` adds pretty formatting
print("Data written to file!")



def handle_json_write(json_data, file_name="data.json"):
    # Writing JSON data to the file
    with open(file_name, "w") as file:
        json.dump(json_data, file, indent=4)
    print(f"JSON data has been written to {file_name}.")
    
    
def handle_json_read(file_name="data.json"):
    # Reading JSON data back from the file
    with open(file_name, "r") as file:
        read_data = json.load(file)
    print("JSON data has been read back from the file.")
    return read_data

