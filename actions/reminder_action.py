from .base_action import ProfileAction
from config.config import REMIND_BUTTON_XPATH, SEND_REMINDER_XPATH

class ReminderAction(ProfileAction):
    def process_page(self) -> None:
        buttons = self.driver.find_elements(self.By.XPATH, REMIND_BUTTON_XPATH)
        
        for button in buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                self.time.sleep(self.sleepTime)
                
                reminder_button = self.driver.find_elements(self.By.XPATH, SEND_REMINDER_XPATH)[0]
                reminder_button.click()
                self.time.sleep(self.sleepTime)
            except Exception as e:
                print(f"Failed to process reminder: {e}")