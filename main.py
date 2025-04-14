from selenium.webdriver.common.by import By
import time

from browser import setup_driver, login, navigate_to_inbox
from actions.reminder_action import ReminderAction
from actions.message_action import MessageAction
from actions.online_tracker import OnlineTracker
from actions.inactive_remover import InactiveProfileRemover
from data_handlers import read_message
from config import REMINDER_SLEEP_TIME, MESSAGE_SLEEP_TIME

def main():
    print("Welcome to Partner Search Automation")
    print("Choose an option:")
    print("1. Send reminders")
    print("2. Send custom message from file")
    print("3. Remove inactive profiles")
    print("4. Track online profiles")
    
    choice = input("Enter your choice (1-4): ")
    
    driver = setup_driver()
    try:
        login(driver)
        navigate_to_inbox(driver)
        
        if choice == "1":
            action = ReminderAction(driver, By, time, REMINDER_SLEEP_TIME)
            action.process_all_pages()
        elif choice == "2":
            message = read_message()
            action = MessageAction(driver, By, time, MESSAGE_SLEEP_TIME, message)
            action.process_all_pages()
        elif choice == "3":
            action = InactiveProfileRemover(driver, By, time, REMINDER_SLEEP_TIME)
            action.process_all_pages()
        elif choice == "4":
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