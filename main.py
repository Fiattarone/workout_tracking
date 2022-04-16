import datetime as dt
import requests

# App ID's & Keys
NUTRITIONIX_APP_ID: str
NUTRITIONIX_API_KEY: str

# API Endpoints
SHEETY_ENDPOINT: str
NUTRITIONIX_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

nx_header = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "x-remote-user-id": "0",
    "Content-Type": "application/json"
}

params = {
    "query": input("What did you do today? ")
}

response = requests.post(url=NUTRITIONIX_EXERCISE_ENDPOINT, json=params, headers=nx_header)
# response.raise_for_status()

data = response.json()
# print(data)

# return all data from sheet
sheety_response = requests.get(url=SHEETY_ENDPOINT)
sheety_response.raise_for_status()

current_date = dt.datetime.now()
print(sheety_response.json())

for idx, exercise in enumerate(data["exercises"]):
    sheety_json = {
        "sheet1": {
            "date": str(dt.datetime.now()),
            "exercise": str(exercise['user_input']),
            "duration": str(exercise['duration_min']),
            "calories burned": str(exercise['nf_calories'])
        }
    }

    sheety_post_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_json)
    print(sheety_post_response.text)
