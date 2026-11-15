import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# Import exceptions
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException

PROMISED_DOWN = 1000
PROMISED_UP = 1000
my_email = os.getenv("my_email")
password = os.getenv("password")
Y_LOGIN_URL = "https://app.100daysofpython.dev/services/y/login"

SPEED_TEST_URL = "https://www.speedtest.net"

chrome_options = webdriver.ChromeOptions()
# Keep the browser open if the script finishes or crashes.
# If True, you need to *manually* QUIT Chrome before you re-run the script.
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

class InternetSpeedTwitterBot():
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = 0
        self.up = 0
        self.wait = WebDriverWait(self.driver, 20)

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        start_bt = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label^="start speed test"]')))
        start_bt.click()

        WebDriverWait(self.driver, 180).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.my-4.uppercase')))

        down, up = self.driver.find_elements(By.CSS_SELECTOR, 'h3.font-mono.py-2.text-5xl.MuiBox-root')
        # print(down.text, up.text)

        down_speed = float(down.text)
        up_speed = float(up.text)

        self.driver.quit()
        return down_speed, up_speed
    
    def tweet_at_provider(self):
        self.driver.get(Y_LOGIN_URL)
        # login_btn = self.wait.until(ec.element_to_be_clickable((By.ID, "y-login-link")))
        # login_btn.click()

        email_input = self.wait.until(ec.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys(my_email)

        password_input = self.driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)

        submit_bt = self.wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "y-login-submit")))
        submit_bt.click()

        time.sleep(3)
        tweet_compose = self.driver.find_element(By.CSS_SELECTOR, value='div[aria-label="Post text"]')
        tweet = f"Hey Internet Provider, why is my speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?!"
        tweet_compose.send_keys(tweet)

        time.sleep(2)
        tweet_button = self.driver.find_element(By.CSS_SELECTOR, value='.x-compose-form button')
        tweet_button.click()

        time.sleep(2)
        self.driver.quit()
        

bot = InternetSpeedTwitterBot()
down, up = bot.get_internet_speed()
print(down, up)
if up < PROMISED_UP or down < PROMISED_DOWN:
    bot.tweet_at_provider()
    