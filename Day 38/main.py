import requests
import os
from dotenv import load_dotenv
from datetime import datetime

today = datetime.now().strftime("%Y/%m/%d")
current_time = datetime.now().strftime("%I:%M:%S %p")

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
ENDPOINT = "https://app.100daysofpython.dev"

WEIGHT = 75
HEIGHT = 174
AGE = 20
GENDER = "male"

NUTRI_URL = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
SHEETY_URL = "https://api.sheety.co/cd608f88b3431857e58e385b93eabe04/workoutTracking/workouts"

auth = (
    os.getenv("SHEETY_USERNAME"),
    os.getenv("SHEETY_PASSWORD")
)

# Check if env vars loaded
print("API_ID loaded:", API_ID is not None)
print("API_KEY loaded:", API_KEY is not None)
print("Username loaded:", auth[0] is not None)
print("Password loaded:", auth[1] is not None)

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
}

work = input("Tell me which exercise you did: ")
data = {
  "query": work,
  "weight_kg": WEIGHT,
  "height_cm": HEIGHT,
  "age": AGE,
  "gender": GENDER
}

response = requests.post(NUTRI_URL, headers=headers, json=data)
result = response.json()

print(result["exercises"][0])

# Loop post all exercises
for i in result["exercises"]:
    workout = {
        "date": today,
        "time": current_time,
        "exercise": i["name"].title(),
        "duration": i["duration_min"],
        "calories": i["nf_calories"]
    }
    workout_put = {"workout": workout}
    response = requests.post(SHEETY_URL, headers=headers, json=workout_put, auth=auth)
    result = response.json()
    print(response.status_code)
    print(response.text)

# response = requests.get(SHEETY_URL)
# print(response.status_code)
# print(response.text)