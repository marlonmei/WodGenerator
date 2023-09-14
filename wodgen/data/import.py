import requests


url = "http://localhost:8000/UploadWorkout"
filename = 'scraped_workouts.csv'

with open(f"./processed/{filename}", "rb") as csv_file:
    files = {"file": (f"{filename}", csv_file, "text/csv")}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
