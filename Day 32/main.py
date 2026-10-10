import smtplib
import datetime as dt
import random

my_email = "minhnguyen2976743@gmail.com"
password = "jtbbcvedofdncqka"

now = dt.datetime.now()
print(now)
# date_of_birth = dt.datetime(year=2007, month=5, day=18)

if now.weekday() == 2:  # Check if today is Wednesday (0=Monday, 1=Tuesday, 2=Wednesday, etc.)
    with open("Day 32/quotes.txt") as file:
        quotes = file.readlines()
        random_quote = random.choice(quotes)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs="minhnguyen2976@yahoo.com", 
                            msg="Subject: Wednesday Wisdom\n\n" + random_quote)