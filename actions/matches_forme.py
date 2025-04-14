from .base_action import ProfileAction
from config.config import MORE_LINK_XPATH

class MatchesForMe(ProfileAction):
    def __init__(self, driver, By, time, sleepTime):
        super().__init__(driver, By, time, sleepTime)

    
