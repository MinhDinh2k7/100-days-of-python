import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self):
        self.SHEETY_URL = "https://api.sheety.co/cd608f88b3431857e58e385b93eabe04/flights/sheet1"
        self.auth = (
            os.getenv("SHEETY_USERNAME"),
            os.getenv("SHEETY_PASSWORD")
        )

    def get_flights(self):
        response = requests.get(self.SHEETY_URL, auth=self.auth)
        result = response.json()
        return result["sheet1"]

    def update_flights(self, row_id, price):
        flight = {
            "lowestPrice": price
        }
        flight_put = {"sheet1": flight}
        response = requests.put(f"{self.SHEETY_URL}/{row_id}", auth=self.auth, json=flight_put)
        return response.json()