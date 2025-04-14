from pathlib import Path

# File paths
CHROME_DRIVER_PATH = r"C:\Program Files (x86)\chromedriver.exe"
DATA_FILE = Path(__file__).parent / "data.json"
REMINDER_FILE = Path(__file__).parent / "reminder.txt"
ZDATA_PATH = Path(__file__).parent.parent / "zdata"  # Path to zdata directory
ZDATA_DATA_FILE = ZDATA_PATH / "data.json"  # Path to data.json in zdata directory
ZDATA_REMINDER_FILE = ZDATA_PATH / "reminder.txt"

# URLs
LOGIN_URL = "https://www.shaadi.com/registration/user/login?go=https%3A%2F%2Fmy.shaadi.com%2Fmy-shaadi"

# Browser settings
POPUP_WAIT_TIME = 10
NAVIGATION_WAIT_TIME = 5
REMINDER_SLEEP_TIME = 2
MESSAGE_SLEEP_TIME = 4

# XPath selectors
NEXT_BUTTON_XPATH = '//button[contains(text(), "Next")]'
REMIND_BUTTON_XPATH = '//button[text()="Remind"]'
SEND_REMINDER_XPATH = '//button[text()="Send Reminder"]'
READ_MORE_XPATH = '//a[text()="Read More"]'
WRITE_MESSAGE_XPATH = '//button[text()="Write Message"]'
PROFILE_STATUS_XPATH = './/*[@title="Chat Now"]'
DROPDOWN_SELECTOR = './/*[@data-test-selector="listDropdown"]'
CANCEL_INVITATION_XPATH = './/*[@data-test-selector="cancelInvitationInboxPage"]'
PROFILE_CONTAINER_XPATH = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'