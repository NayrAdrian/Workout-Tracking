import sys
import requests
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_ID = os.getenv('API_ID').strip()
API_KEY = os.getenv('API_KEY').strip()


class WorkoutTrackerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Workout Tracker")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #000217;")

        # Create and set up the layout
        self.create_widgets()

        # Update the date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def create_widgets(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Date and time display
        self.date_time_label = QLabel()
        self.date_time_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.update_time()

        # Create a container for the logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_label = QLabel()
        logo_pixmap = QPixmap("workoutTracker_logo.PNG")  # Replace with the path to your logo
        logo_label.setPixmap(logo_pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        logo_container.setLayout(logo_layout)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Exercise input
        self.exercise_input = QLineEdit()
        self.exercise_input.setPlaceholderText("Tell me what exercises you did today...")
        self.exercise_input.setStyleSheet(
            "padding: 10px; border-radius: 5px; border: 1px solid #ffffff; color: #ffffff; background-color: #000000;")
        form_layout.addRow(QLabel("Exercise:"), self.exercise_input)
        form_layout.labelForField(self.exercise_input).setStyleSheet("color: #ffffff; font-size: 14px;")

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
            background-color: #1E90FF; color: white; padding: 12px; border: none;
            border-radius: 5px; font-size: 16px; font-weight: bold;""")
        submit_button.clicked.connect(self.submit_exercise)
        form_layout.addRow(submit_button)

        # View workout sheet button
        sheet_button = QPushButton("View Workout Sheet")
        sheet_button.setStyleSheet("""
            background-color: #32CD32; color: white; padding: 12px; border: none;
            border-radius: 5px; font-size: 16px; font-weight: bold;""")
        sheet_button.clicked.connect(self.open_workout_sheet)
        form_layout.addRow(sheet_button)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff; font-size: 14px;")

        # Add widgets to main layout
        main_layout.addWidget(self.date_time_label, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addWidget(logo_container)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def update_time(self):
        now = datetime.now().strftime("%m/%d/%Y %I:%M %p")
        self.date_time_label.setText(now)

    def submit_exercise(self):
        exercise_text = self.exercise_input.text()
        if not exercise_text:
            QMessageBox.warning(self, "Input Error", "Please enter an exercise")
            return

        exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
        post_sheety_endpoint = "https://api.sheety.co/b237e38ca30d773f18ac9108cc89a109/myWorkouts/workouts"

        headers = {
            "x-app-id": API_ID,
            "x-app-key": API_KEY
        }

        bearer_headers = {
            "Authorization": "Bearer Wsu57s82bglaj17"
        }

        parameters = {
            "query": exercise_text,
            "gender": "male",
            "weight_kg": 65,
            "height_cm": 162.56,
            "age": 28
        }

        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        if response.status_code != 200:
            QMessageBox.critical(self, "API Error", f"Error: {response.status_code}\n{response.text}")
            return

        result = response.json()

        today_date = datetime.now().strftime("%d/%m/%Y")
        now_time = datetime.now().strftime("%X")

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
                if sheet_response.status_code == 200:
                    self.status_label.setText("Workout logged successfully!")
                else:
                    self.status_label.setText("Failed to log workout.")
        else:
            self.status_label.setText("No exercises found in the response.")

        # Clear the input box
        self.exercise_input.clear()

    def open_workout_sheet(self):
        url = "https://docs.google.com/spreadsheets/d/179e3Keh2tIvu7YhHlbTvR8J11OFV9QbbWwv_R_Quih4/edit?gid=0#gid=0"
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkoutTrackerApp()
    window.show()
    sys.exit(app.exec_())
