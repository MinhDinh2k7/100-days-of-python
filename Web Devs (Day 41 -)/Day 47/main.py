import requests
import smtplib
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("my_email")
password = os.getenv("password")

header = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    )
}

test_url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(test_url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")


price = f"{soup.find(class_='a-price-whole').getText()}{soup.find(class_='a-price-fraction').getText()}"
if float(price) < 100.0:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs="minhnguyen2976@yahoo.com", 
                            msg="Rice cooker price alert!!!! Only " + price)