from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Sample values
GENDER = "male"
WEIGHT_KG = 65
HEIGHT_CM = 162.56
AGE = 28

# Load environment variables from .env file
load_dotenv()

# Retrieve and strip environment variables
API_ID = os.getenv('API_ID').strip()
API_KEY = os.getenv('API_KEY').strip()

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
post_sheety_endpoint = "https://api.sheety.co/b237e38ca30d773f18ac9108cc89a109/myWorkouts/workouts"

exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
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

# Make request to Nutritionix API
response = requests.post(exercise_endpoint, json=parameters, headers=headers)


if response.status_code != 200:
    print(f"Error: Received status code {response.status_code}")
    print(response.text)
else:
    result = response.json()
    print(result)

    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    # Check if the "exercises" key is in the result
    if "exercises" in result:
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
    else:
        print("Error: 'exercises' key not found in the response")
