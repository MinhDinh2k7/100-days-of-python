import requests as req
from datetime import datetime

# Constants
MY_LAT = 42.262119
MY_LNG = -71.802238

params = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

resp = req.get("https://api.sunrise-sunset.org/v2", params=params)
resp.raise_for_status()
data = resp.json()
sunrise = data["sunrise"].split("T")[1].split(":")
sunset = data["sunset"].split("T")[1].split(":")

print(f"Sunrise: {sunrise[0]}:{sunrise[1]}")
print(f"Sunset: {sunset[0]}:{sunset[1]}")

time_now = datetime.now()
print(f"Current time: {time_now.hour}:{time_now.minute}")