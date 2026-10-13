from alpha_vantage import *
from twilio.rest import Client
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

# CONST
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALP_API_KEY = os.getenv("ALP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILLIO_SID = os.getenv("TWILLIO_SID")
TWILLIO_AUTH_TOKEN = os.getenv("TWILLIO_AUTH_TOKEN")
                               
ALP_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"

ALP_PARAMS = {"function": "TIME_SERIES_DAILY", "symbol": STOCK, "apikey": ALP_API_KEY}

NEW_PARAMS = {
    "q": COMPANY_NAME,
    "pageSize": 3,
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY,
}

## ## ## ## ## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

alp_response = requests.get(url=ALP_URL, params=ALP_PARAMS)
alp_response.raise_for_status()
alp_data = alp_response.json()
# print(alp_data)

prices = alp_data["Time Series (Daily)"]

dates = sorted(prices.keys(), reverse=True)

yesterday_close = float(prices[dates[0]]["4. close"])
previous_close = float(prices[dates[1]]["4. close"])

change = ((yesterday_close - previous_close) / previous_close) * 100

# if change >= 5 or change <= -5:
#     print("Get News")
# else: print("N/A")

## ## ## ## ## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if change >= 5 or change <= -5:
    news_response = requests.get(url=NEWS_URL, params=NEW_PARAMS)
    news_response.raise_for_status()
    news_data = news_response.json()
    if news_data["status"] == "error":
        print(news_data["message"])
    else:
        with open("output.json", "w", encoding="utf-8") as json_file:
            # indent=4 makes the file human-readable (pretty-printed)
            json.dump(news_data, json_file, indent=4, ensure_ascii=False)

    #     # Printing the news with the links
    #     for articles in news_data["articles"]:
    #         print(f"""===========================================================================================================================================\n
    # Author: {articles["author"]}\n
    # Title: {articles["title"]}\n
    # Description: {articles["description"]}\n
    # Url: {articles["url"]}\n
    # Time of publish: {articles["publishedAt"]}\n
    # Content: {articles["content"]}""")
    # print("===========================================================================================================================================")

## ## ## ## ## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
client = Client(TWILLIO_SID, TWILLIO_AUTH_TOKEN)

if change >= 5 or change <= -5:
    formatted_articles = [
        f"TSLA: {'🔺' if change > 0 else '🔻'}{abs(change):.2f}%\n"
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in news_data["articles"]
    ]

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+15086156953",
            to="+15086156953"
        )
        print(f"SMS sent: {message.sid}")

# Test send message
if True:
    message = client.messages.create(
        body="article",
        from_="TWILLIO PHONE NUMEBR HERE",
        to="+15086156953"
    )

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
