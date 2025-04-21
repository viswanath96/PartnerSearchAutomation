import datetime
from .base_action import ProfileAction
from config.config import (
    PROFILE_CONTAINER_XPATH,
    DROPDOWN_SELECTOR,
    PROFILE_STATUS_XPATH,
    CANCEL_INVITATION_XPATH
)

class InactiveProfileRemover(ProfileAction):
    def process_page(self) -> None:
        profile_container = self.driver.find_element(
            self.By.XPATH, 
            PROFILE_CONTAINER_XPATH
        )
        profiles = profile_container.find_elements(self.By.XPATH, './div')
        
        for profile in profiles:
            self.process_single_profile(profile)

    def process_single_profile(self, profile) -> None:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile)
            self.time.sleep(self.sleepTime)
            
            dropdown_button = profile.find_element(
                self.By.XPATH, 
                DROPDOWN_SELECTOR
            )
            
            if dropdown_button:
                status_element = profile.find_element(
                    self.By.XPATH, 
                    PROFILE_STATUS_XPATH
                )
                status_text = status_element.text
                
                if status_text in ["Online 2w ago", "Online 1w ago"]:
                    print(status_text)
                    self.time.sleep(self.sleepTime)
                    dropdown_button.click()
                    
                    cancel_button = profile.find_element(
                        self.By.XPATH,
                        CANCEL_INVITATION_XPATH
                    )
                    cancel_button.click()
                    self.time.sleep(self.sleepTime)
                else:
                    print(f"{datetime.datetime.now().strftime("%m-%d-%Y %H:%M")} - Profile {status_text}")
            else:
                print("Profile deactivated")
                
        except Exception as e:
            print(f"{datetime.datetime.now().strftime("%m-%d-%Y %H:%M")} - An exception occurred: {e}. Skipping profile.")