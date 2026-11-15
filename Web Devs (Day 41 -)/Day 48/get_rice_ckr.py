from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.com/Instant-Pot-Plus-60-Programmable/dp/B01NBKTPTS/?th=1")

# Bypass amazon bot-block
# time.sleep(.5)
# button = driver.find_element(By.CLASS_NAME, value="a-button-text")
# button.click()
# time.sleep(1.5)

# driver.get("https://www.amazon.com/Instant-Pot-Plus-60-Programmable/dp/B01NBKTPTS/?th=1")
price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
price_cent = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
print(f"{price_dollar.text}{price_cent.text}")

input("Window holder... ")

driver.quit()