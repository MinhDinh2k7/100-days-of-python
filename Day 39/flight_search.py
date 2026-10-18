import requests
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT  = "https://app.100daysofpython.dev/v1/flights/search"

class FlightSearch:
    def __init__(self):
        self.API_ID = os.getenv("API_ID")
        self.API_KEY = os.getenv("API_KEY")

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": self.API_KEY,
        }

        response = requests.get(ENDPOINT, params=params)
        data = response.json()

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data

# tomorrow         = datetime.now() + timedelta(days=1)
# six_month_later  = datetime.now() + timedelta(days=6 * 30)
# flightSearch = FlightSearch()
# SEARCH = flightSearch.check_flights("LHR", "FRA", 
#                                     tomorrow.strftime("%Y-%m-%d"),
#                                     six_month_later.strftime("%Y-%m-%d"))