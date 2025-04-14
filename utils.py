from datetime import datetime
import inspect
import json
from abc import ABC, abstractmethod
from typing import Optional
from schedule import Schedule
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Base class for profile actions
class ProfileAction(ABC):
    """Base class for profile actions that process pages of profiles.
    
    This class implements the template method pattern where subclasses must
    implement process_page() to define how individual pages are processed.
    """
    def __init__(self, driver, By, time, sleepTime):
        self.driver = driver
        self.By = By
        self.time = time
        self.sleepTime = sleepTime

    @abstractmethod
    def process_page(self) -> None:
        """Process the current page of profiles.
        
        This method must be implemented by subclasses to define how to
        process profiles on the current page.
        
        Raises:
            NotImplementedError: If the subclass doesn't implement this method
        """
        raise NotImplementedError("Subclasses must implement process_page")

    def has_next_page(self) -> bool:
        try:
            next_button = self.driver.find_elements(self.By.XPATH, '//button[contains(text(), "Next")]')
            return len(next_button) > 0 and next_button[0].is_enabled()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def click_next_page(self) -> bool:
        try:
            next_button = self.driver.find_elements(self.By.XPATH, '//button[contains(text(), "Next")]')[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            next_button.click()
            self.time.sleep(self.sleepTime)
            return True
        except Exception as e:
            print(f"Failed to navigate to next page: {e}")
            return False

    def process_all_pages(self) -> None:
        page_number = 1
        while True:
            print(f"Processing page {page_number}")
            self.process_page()
            
            if not self.has_next_page():
                print("Reached last page")
                break
                
            if not self.click_next_page():
                print("Failed to navigate to next page")
                break
                
            page_number += 1

class ReminderAction(ProfileAction):
    def process_page(self) -> None:
        buttons = self.driver.find_elements(self.By.XPATH, '//button[text()="Remind"]')
        
        for button in buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                self.time.sleep(self.sleepTime)
                
                reminder_button = self.driver.find_elements(self.By.XPATH, '//button[text()="Send Reminder"]')[0]
                reminder_button.click()
                self.time.sleep(self.sleepTime)
            except Exception as e:
                print(f"Failed to process reminder: {e}")

class MessageAction(ProfileAction):
    def __init__(self, driver, By, time, sleepTime, message: str):
        super().__init__(driver, By, time, sleepTime)
        self.message = message

    def process_page(self) -> None:
        links = self.driver.find_elements(self.By.XPATH, '//a[text()="Read More"]')
        
        for link in links:
            try:
                self.process_single_profile(link)
            except Exception as e:
                print(f"Failed to process profile: {e}")
                self.cleanup_tabs()

    def process_single_profile(self, link) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        link.click()
        self.time.sleep(self.sleepTime)
        
        # Switch to new tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        if not self.is_profile_online():
            self.cleanup_tabs()
            return
            
        self.send_message()
        self.cleanup_tabs()

    def is_profile_online(self) -> bool:
        online_text = self.driver.find_elements(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div/span'
        )[0]
        return online_text.text == "Online now"

    def send_message(self) -> None:
        write_button = self.driver.find_elements(self.By.XPATH, '//button[text()="Write Message"]')[0]
        write_button.click()
        self.time.sleep(self.sleepTime)
        
        text_field = self.driver.find_elements(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[3]/div[2]/div[1]/section/form/input[3]'
        )[0]
        text_field.send_keys(self.message)
        text_field.submit()
        self.time.sleep(self.sleepTime)
        
        close_button = self.driver.find_elements(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[3]/div[2]/div[1]/section/div[1]/div/button[2]'
        )[0]
        close_button.click()
        self.time.sleep(self.sleepTime)

    def cleanup_tabs(self) -> None:
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.time.sleep(self.sleepTime)

class OnlineTracker(ProfileAction):
    def __init__(self, driver, By, time, sleepTime, data_file: str):
        super().__init__(driver, By, time, sleepTime)
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self) -> dict:
        return handle_json_read(self.data_file)

    def save_data(self) -> None:
        handle_json_write(self.data, self.data_file)

    def process_page(self) -> None:
        profile_container = self.driver.find_element(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'
        )
        profiles = profile_container.find_elements(self.By.XPATH, './div')
        
        for profile in profiles:
            self.process_single_profile(profile)
        
        self.save_data()

    def process_single_profile(self, profile) -> None:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
            self.time.sleep(self.sleepTime)
            
            status = self.get_profile_status(profile)
            if status == "Online now":
                self.update_statistics()
        except Exception as e:
            print(f"Failed to process profile status: {e}")

    def get_profile_status(self, profile) -> str:
        dropdown = profile.find_element(self.By.XPATH, './/*[@data-test-selector="listDropdown"]')
        status = profile.find_element(self.By.XPATH, './/*[@title="Chat Now"]')
        return status.text

    def update_statistics(self) -> None:
        now = datetime.now()
        date_key = now.strftime("%m-%d-%Y")
        time_key = now.strftime("%H")
        
        for datum in self.data:
            if datum["date"] == date_key:
                self.update_existing_date(datum, time_key)
                return
                
        self.add_new_date(now, time_key)

    def update_existing_date(self, datum: dict, time_key: str) -> None:
        for occurance in datum["occurance"]:
            if occurance["hour"] == time_key:
                occurance["count"] += 1
                return
        datum["occurance"].append({"hour": time_key, "count": 1})

    def add_new_date(self, now: datetime, time_key: str) -> None:
        new_schedule = Schedule(
            day=now.strftime("%A"),
            date=now.strftime("%m-%d-%Y"),
            occurance=[{"hour": time_key, "count": 1}]
        )
        self.data.append(new_schedule.to_dict())

class InactiveProfileRemover(ProfileAction):
    """Class for removing inactive profiles based on their last online status."""
    
    def process_page(self) -> None:
        """Process the current page and remove inactive profiles."""
        profile_container = self.driver.find_element(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'
        )
        profiles = profile_container.find_elements(self.By.XPATH, './div')
        
        for profile in profiles:
            self.process_single_profile(profile)
    
    def process_single_profile(self, profile) -> None:
        """Process a single profile and remove if inactive."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
            self.time.sleep(self.sleepTime)
            
            dropdown_button = profile.find_element(
                self.By.XPATH, 
                './/*[@data-test-selector="listDropdown"]'
            )
            
            if dropdown_button:
                status_element = profile.find_element(
                    self.By.XPATH, 
                    './/*[@title="Chat Now"]'
                )
                status_text = status_element.text
                
                if status_text in ["Online 2w ago", "Online 1w ago"]:
                    print(status_text)
                    self.time.sleep(self.sleepTime)
                    dropdown_button.click()
                    
                    cancel_button = profile.find_element(
                        self.By.XPATH,
                        './/*[@data-test-selector="cancelInvitationInboxPage"]'
                    )
                    cancel_button.click()
                    self.time.sleep(self.sleepTime)
                else:
                    print(f"Profile {status_text}")
            else:
                print("Profile deactivated")
                
        except Exception as e:
            print(f"An exception occurred: {e}. Skipping profile.")

# Helper functions
def message_from_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except IOError:
        return "An error occurred while reading the file."

def handle_json_write(json_data: dict, file_name: str = "data.json") -> None:
    with open(file_name, "w") as file:
        json.dump(json_data, file, indent=4)
    print(f"JSON data has been written to {file_name}.")

def handle_json_read(file_name: str = "data.json") -> dict:
    with open(file_name, "r") as file:
        read_data = json.load(file)
    print("JSON data has been read back from the file.")
    return read_data

# Main action functions that replace the original recursive functions
def process_reminders(driver, By, time, sleepTime) -> None:
    action = ReminderAction(driver, By, time, sleepTime)
    action.process_all_pages()

def process_messages(driver, By, time, sleepTime) -> None:
    message = message_from_file('reminder.txt')
    action = MessageAction(driver, By, time, sleepTime, message)
    action.process_all_pages()

def track_online_profiles(driver, By, time, sleepTime) -> None:
    action = OnlineTracker(driver, By, time, sleepTime)
    action.process_all_pages()

def remove_inactive_profiles(driver, By, time, sleepTime) -> None:
    """Initialize and run the inactive profile remover."""
    action = InactiveProfileRemover(driver, By, time, sleepTime)
    action.process_all_pages()

