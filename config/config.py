from pathlib import Path

# File paths
CHROME_DRIVER_PATH = r"C:\Program Files (x86)\chromedriver.exe"
DATA_FILE = Path(__file__).parent / "data.json"
REMINDER_FILE = Path(__file__).parent / "reminder.txt"
ZDATA_PATH = Path(__file__).parent.parent.parent / "zdata"  # Path to zdata directory
ZDATA_DATA_FILE = ZDATA_PATH / "data.json"  # Path to data.json in zdata directory
ZDATA_REMINDER_FILE = ZDATA_PATH / "reminder.txt"


# Browser settings
POPUP_WAIT_TIME = 10
NAVIGATION_WAIT_TIME = 5
REMINDER_SLEEP_TIME = 2
MESSAGE_SLEEP_TIME = 4
PREFERENCE_CHECK_BOX = ['photostatus-visible','recently_joined-1 Week','countryofresidence-India','diet-Non-Veg','diet-Eggetarian','diet-Vegan']
PREFERENCE_CHECK_BOX_MAX = ['photostatus-visible','recently_joined-1 Week','countryofresidence-India','annualincome-INR 4 Lakh to 7 Lakh','annualincome-INR 7 Lakh to 10 Lakh','annualincome-INR 1 Lakh to 2 Lakh','annualincome-INR 2 Lakh to 4 Lakh','diet-Non-Veg','diet-Eggetarian','diet-Vegan']

# XPath selectors
NEXT_BUTTON_XPATH = '//button[contains(text(), "Next")]'
REMIND_BUTTON_XPATH = '//button[text()="Remind"]'
SEND_REMINDER_XPATH = '//button[text()="Send Reminder"]'
READ_MORE_XPATH = '//a[text()="Read More"]'
MORE_XPATH = '//a[text()="More"]'
WRITE_MESSAGE_XPATH = '//button[text()="Write Message"]'
PROFILE_STATUS_XPATH = './/*[@title="Chat Now"]'
DROPDOWN_SELECTOR = './/*[@data-test-selector="listDropdown"]'
CANCEL_INVITATION_XPATH = './/*[@data-test-selector="cancelInvitationInboxPage"]'
PROFILE_CONTAINER_XPATH = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[1]'
SEE_All_LINK_XPATH = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div[1]/div[3]/div[4]/a'