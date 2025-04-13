from datetime import datetime
from .base_action import ProfileAction
from data_handlers import read_json_data, write_json_data
from config import PROFILE_CONTAINER_XPATH, PROFILE_STATUS_XPATH
from schedule import Schedule

class OnlineTracker(ProfileAction):
    def __init__(self, driver, By, time, sleepTime):
        super().__init__(driver, By, time, sleepTime)
        self.data = read_json_data()

    def process_page(self) -> None:
        profile_container = self.driver.find_element(
            self.By.XPATH, 
            PROFILE_CONTAINER_XPATH
        )
        profiles = profile_container.find_elements(self.By.XPATH, './div')
        
        for profile in profiles:
            self.process_single_profile(profile)
        
        write_json_data(self.data)

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
        status = profile.find_element(self.By.XPATH, PROFILE_STATUS_XPATH)
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