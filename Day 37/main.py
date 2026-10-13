import requests
from datetime import datetime

USERNAME = "minhdinh2k7"
TOKEN = "12345678"

headers = {
    "X-USER-TOKEN": TOKEN
}

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# Creating user(done)
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

GRAPH_ID = "graph1"

graph_config = {
    "id": GRAPH_ID,
    "name": "Cardio graph",
    "unit": "Km",
    "type": "float",
    "color": "shibafu"
}

# Creating graph(done)
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now().strftime("%Y%m%d")

pixel_config = {
    "date": today,
    "quantity": "2.5"
}

# Creating today's pixel
response = requests.post(url=pixel_endpoint, json=pixel_config, headers=headers)
print(response.text)

# Try and retry if rejected due to not being a sponsor
import time

def try_request(request, endpoint, config = ""):
    while True:
        if request == "delete":
            response = requests.delete(
                url=endpoint,
                headers=headers
            )
        elif request == "update":
            response = requests.put(
                url=endpoint, 
                json=config, 
                headers=headers
            )
        else:
            print("Invalid request")
            break

        result = response.json()
        print(result)

        if result.get("isSuccess") is True:
            print("Request successful!")
            break

        elif result.get("isRejected") is True:
            print("Request rejected. Retrying...")
            time.sleep(1)

        else:
            print("Request failed for another reason. Stopping.")
            break

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today}"

update_config = {
    "date": today,
    "quantity": "2.0"
}

# # Updating today's pixel
# response = try_request("update", update_endpoint, update_config)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today}"

# Delete today's pixel
response = try_request("delete", delete_endpoint)