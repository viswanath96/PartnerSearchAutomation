from abc import ABC, abstractmethod
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from config.config import NEXT_BUTTON_XPATH

class ProfileAction(ABC):
    """Base class for profile actions that process pages of profiles."""
    
    def __init__(self, driver, By, time, sleepTime):
        self.driver = driver
        self.By = By
        self.time = time
        self.sleepTime = sleepTime

    @abstractmethod
    def process_page(self) -> None:
        """Process the current page of profiles."""
        raise NotImplementedError("Subclasses must implement process_page")

    def has_next_page(self) -> bool:
        try:
            next_button = self.driver.find_elements(self.By.XPATH, NEXT_BUTTON_XPATH)
            return len(next_button) > 0 and next_button[0].is_enabled()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def click_next_page(self) -> bool:
        try:
            next_button = self.driver.find_elements(self.By.XPATH, NEXT_BUTTON_XPATH)[0]
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