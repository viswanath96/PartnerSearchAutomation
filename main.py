from selenium.webdriver.common.by import By
import time
import json
from browser.browser import setup_driver, login, navigate_to_inbox, navigate_to_more_matches, navigate_to_see_all,check_options_list
from actions.reminder_action import ReminderAction
from actions.message_action import MessageAction
from actions.online_tracker import OnlineTracker
from actions.inactive_remover import InactiveProfileRemover
from actions.matches_forme import MatchesForMe
from data.data_handlers import read_message
from config.config import REMINDER_SLEEP_TIME, POPUP_WAIT_TIME,NAVIGATION_WAIT_TIME, MESSAGE_SLEEP_TIME

def main():

    print("Welcome to Partner Search Automation")
    print("Choose an option:")
    print("1. Send reminders")
    print("2. Send custom message from file")
    print("3. Send custom message from file (Broadcast)")
    print("4. Remove inactive profiles")
    print("5. Open all profiles that are looking for me.")
    print("6. Open all profiles that in a broader scope.")
    print("7. Open all profiles that in a premium scope.")
    print("8. Track online profiles")

    try:
        # Load configuration from config.json
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        WINDOWS_SERVICE_OPTIONS = config.get("WINDOWS_SERVICE_OPTIONS", [])
    except Exception as e:
            print(f"An error occurred: {e}")


    if WINDOWS_SERVICE_OPTIONS:
        choice = WINDOWS_SERVICE_OPTIONS[0]
    else:
        choice = input("Enter your choice (1-8): ")
    
    driver = setup_driver()
    try:
        login(driver)
        
        if choice == "1":
            navigate_to_inbox(driver)
            action = ReminderAction(driver, By, time, REMINDER_SLEEP_TIME)
            action.process_all_pages()
        elif choice == "2":
            navigate_to_inbox(driver)
            message = read_message()
            action = MessageAction(driver, By, time, MESSAGE_SLEEP_TIME, message)
            action.process_all_pages()
        elif choice == "3":
            navigate_to_inbox(driver)
            message = read_message()
            action = MessageAction(driver, By, time, MESSAGE_SLEEP_TIME, message,True)
            action.process_all_pages()
        elif choice == "4":
            navigate_to_inbox(driver)
            action = InactiveProfileRemover(driver, By, time, REMINDER_SLEEP_TIME)
            action.process_all_pages()
        elif choice == "5":
            navigate_to_more_matches(driver)
            navigate_to_see_all(driver, 1)
            check_options_list(driver,1)
            action = MatchesForMe(driver, By, time, NAVIGATION_WAIT_TIME)
            action.process_all_pages()
        elif choice == "6":
            navigate_to_more_matches(driver)
            navigate_to_see_all(driver, 2)
            check_options_list(driver,2)
            action = MatchesForMe(driver, By, time, NAVIGATION_WAIT_TIME)
            action.process_all_pages()
        elif choice == "7":
            navigate_to_more_matches(driver)
            navigate_to_see_all(driver, 3)
            check_options_list(driver,3)
            action = MatchesForMe(driver, By, time, NAVIGATION_WAIT_TIME)
            action.process_all_pages()
        elif choice == "8":
            navigate_to_inbox(driver)
            action = OnlineTracker(driver, By, time, REMINDER_SLEEP_TIME)
            action.process_all_pages()
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