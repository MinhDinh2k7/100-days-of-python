from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# Import exceptions
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
import os
from time import time, sleep

URL = "https://app.100daysofpython.dev/services/tindog/u/JMZmtw-C4kmJfUPyUsjvfPN3nG4-TPtI"
my_email = os.getenv("my_email")
password = os.getenv("password")

chrome_options = webdriver.ChromeOptions()
# Keep the browser open if the script finishes or crashes.
# If True, you need to *manually* QUIT Chrome before you re-run the script.
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 5)

driver.get(URL)

# ----------------  Network Resilience ----------------

# Simple retry wrapper
def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise

# Function to perform entire login process with retry
def login():
    # Store the handle of the main website window
    main_window = driver.current_window_handle

    try:
        login_btn = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-tindog-login")))
        login_btn.click()
        log_face_btn = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-facebark")))
        log_face_btn.click()

        # Wait until the facebark login in opened
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        for handle in driver.window_handles: # Switch focus to facebark login window
            if handle != main_window:
                driver.switch_to.window(handle)
                break
        email_input = wait.until(ec.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys(my_email)

        password_input = driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password)

        submit_button = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        submit_button.click()

        # Wait until Facebark closes then switch focus back to main window
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
        driver.switch_to.window(main_window)
    except TimeoutException as e:
        print(f"Login timed out: {e}")
        raise

    # Click on all the submit buttons
    while True:
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
            submit_button.click()
        except: break

# Put the entire login flow into the retry-wrapper
retry(login, description="login")

# Step 4 — like all 20 dogs
for n in range(20):
    sleep(1)
    try:
        like_button = driver.find_element(By.CLASS_NAME, value='btn-like')
        like_button.click()
    except ElementClickInterceptedException:
        # Match popup is in the way — dismiss it and continue
        try:
            driver.find_element(By.CSS_SELECTOR, value='.match-popup a').click()
        except NoSuchElementException:
            sleep(2)
    except NoSuchElementException:
        # Like button not loaded yet OR all dogs have been swiped — wait and retry
        sleep(2)

input("Window holder... ")

driver.quit()