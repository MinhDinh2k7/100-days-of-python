import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")

# Click the language button
wait = WebDriverWait(driver, 0.5)
language_locator = (By.CLASS_NAME, "langSelectButton")
lang_button = wait.until(EC.visibility_of_element_located(language_locator))
lang_button.click()

# Initial coockie clicks for first product
cookie_button = driver.find_element(By.ID, value="bigCookie")
for i in range(114):
    cookie_button.click()

# While loop checking the upgrades
timeout = time.time() + 60*5   # 5 minutes from now
while True:
    if time.time() > timeout:
        break
    
    # Current number of cookies
    cookies = driver.find_elements(By.ID, value="cookies")

    # current cheapest items
    try: cheapest_product = driver.find_element(By.CSS_SELECTOR, value=".product.unlocked.enabled")
    except:
        cookie_button.click()
        continue

    # Check the product store
    products = driver.find_elements(By.CSS_SELECTOR, value=".product.unlocked.enabled")
    for product in products:
        price1 = cheapest_product.find_element(By.CLASS_NAME, value="price").text
        price2 = product.find_element(By.CLASS_NAME, value="price").text
        if price1 > price2:
            cheapest_product = product

    # Buy the cheapest product
    cheapest_product.click()

    cookie_button.click()

input("Window holder... ")

driver.quit()