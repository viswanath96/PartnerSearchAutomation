import datetime
from .base_action import ProfileAction
from config.config import MORE_XPATH

class MatchesForMe(ProfileAction):
    def __init__(self, driver, By, time, sleepTime):
        super().__init__(driver, By, time, sleepTime)

    def process_page(self) -> None:
        links = self.driver.find_elements(self.By.XPATH, MORE_XPATH)
        
        for link in links:
            try:
                link.click()
                self.time.sleep(self.sleepTime)
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.time.sleep(self.sleepTime)
            except Exception as e:
                print(f"{datetime.datetime.now().strftime("%m-%d-%Y %H:%M")} - Failed to process profile: {e}")
                self.cleanup_tabs()
