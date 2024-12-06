# Example script to upload weather data to PWS Weather Station

import requests
from datetime import datetime, timezone

url = "https://pwsupdate.pwsweather.com/api/v1/submitwx?"

payload = {
    "ID": "<yourStationID>",
    "PASSWORD": "<yourStationAPIKey>",
    "dateutc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    "tempf": 27,
    "humidity": 94,
    "winddir": 290,
    "windspeedmph": 1,
    "windgustmph": 3,
    "baromin": 5,
    "dewptf": 34,
    "rainin": 3,
    "dailyrainin": 0.1,
    "solarradiation": 300,
    "UV": 5,
    "softwaretype": "HomeAssistant",
    "action" : "updateraw"
}

response = requests.post(url, data=payload) 

print(response.status_code)
print(response.json())
