import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time

load_dotenv()

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SIMILAR_ACCOUNT = "chefsteps"   # the account whose followers you'll follow
BASE_URL = "https://app.100daysofpython.dev/services/share-a-naan"
LOGIN_URL = f"{BASE_URL}/login"
ACC_URL = "https://app.100daysofpython.dev/services/share-a-naan/u/chefsteps/followers"
chrome_options = webdriver.ChromeOptions()
# Keep chrome browser open after program finishes
chrome_options.add_experimental_option("detach", True)

class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def login(self):
        self.driver.get(LOGIN_URL)
        time.sleep(2)

        self.driver.find_element(By.ID, "username").send_keys(EMAIL)
        password = self.driver.find_element(By.ID, "password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        time.sleep(3)

        self.driver.find_element(By.CLASS_NAME, "naan-popup-dismiss").click()
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Not Now')]").click()

    def find_followers(self):
        self.driver.get(ACC_URL)
        time.sleep(2)
        popup = self.driver.find_element(By.CSS_SELECTOR, ".followers-scroll")
        for _ in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            time.sleep(1)
        
    def follow(self):
        followers = self.driver.find_elements(By.CSS_SELECTOR, ".followers-scroll button")
        for follower in followers:
            try:
                follower.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                cancel = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                cancel.click()


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()