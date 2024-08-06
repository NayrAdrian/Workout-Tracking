import requests
from datetime import datetime

GENDER = "male"  # Sample Value
WEIGHT_KG = 65  # Sample Value
HEIGHT_CM = 162.56  # Sample Value
AGE = 28  # Sample Value

API_ID = "3e39d761"
API_KEY = "2e3ca2ade1e9e40af700714e0e3d57cd"


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
get_sheety_endpoint = "https://api.sheety.co/b237e38ca30d773f18ac9108cc89a109/myWorkouts/workouts"
post_sheety_endpoint = "https://api.sheety.co/b237e38ca30d773f18ac9108cc89a109/myWorkouts/workouts"

exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,

}

bearer_headers = {
    "Authorization": "Bearer Wsu57s82bglaj17"
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(post_sheety_endpoint, json=sheet_inputs, headers=bearer_headers)
    print(sheet_response.text)