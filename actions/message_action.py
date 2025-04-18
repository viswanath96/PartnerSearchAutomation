from .base_action import ProfileAction
from config.config import READ_MORE_XPATH, WRITE_MESSAGE_XPATH,CHAT_NOW_XPATH,ONLINE_NOW_XPATH

class MessageAction(ProfileAction):
    def __init__(self, driver, By, time, sleepTime, message: str,broadcast: bool = False) -> None:
        super().__init__(driver, By, time, sleepTime)
        self.message = message
        self.broadcast = broadcast

    def process_page(self) -> None:
        links = self.driver.find_elements(self.By.XPATH, READ_MORE_XPATH)
        
        for link in links:
            try:
                self.process_single_profile(link)
            except Exception as e:
                print(f"Failed to process profile: {e}")
                self.cleanup_tabs()

    def process_single_profile(self, link) -> None:
        # Check if the chat is already opened in a new tab
        try:
            self.close_open_chat()
        except Exception as e:
            print(f"No open chat to close")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        
        # # Locate the <div> element with title="Chat Now"
        # chat_div = self.driver.find_element(self.By.XPATH, CHAT_NOW_XPATH)
        # # Check if there is a child element with text "online now"
        # child_elements = chat_div.find_elements(self.By.XPATH, ONLINE_NOW_XPATH)
        # if not child_elements:
        #     return
            
        link.click()
        self.time.sleep(self.sleepTime)
        
        # Switch to new tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        if not self.is_profile_online() and not self.broadcast:
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
        write_button = self.driver.find_elements(self.By.XPATH, WRITE_MESSAGE_XPATH)[0]
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

    def close_open_chat(self):
        close_button = self.driver.find_elements(
            self.By.XPATH, 
            '//*[@id="root"]/div/div/div/div[2]/div[3]/div[2]/div[1]/section/div[1]/div/button[2]'
        )[0]
        close_button.click()
        self.time.sleep(self.sleepTime)