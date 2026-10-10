import smtplib
import datetime as dt
import random

my_email = "minhnguyen2976743@gmail.com"
password = "jtbbcvedofdncqka"

now = dt.datetime.now()
with open("Day 32/birthdays.csv") as file:
    birthdays = file.readlines()[1:]  # Skip the header line

for row in birthdays:
    data = row.strip().split(",")
    name = data[0]
    email = data[1]
    year = int(data[2])
    month = int(data[3])
    day = int(data[4])

    if now.month == month and now.day == day:
        letters = ["letter1.txt", "letter2.txt", "letter3.txt"]
        with open("Day 32/" + random.choice(letters)) as file:
            letter = file.read().replace("[NAME]", name)


        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, 
                                to_addrs=email, 
                                msg="Subject: Happy Birthday, " + name + "!\n\n" + letter)