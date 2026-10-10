import requests as req

resp = req.get("http://api.open-notify.org/iss-now.json")
resp.raise_for_status()

data = resp.json()

longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]

iss_position = (longitude, latitude)
print(iss_position)