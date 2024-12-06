# PWS Weather Upload Blueprint
Upload weather data from Home Assistant to a PWS Weather station

## Setup
Add the following lines to your Home Assistant configuraiton.yaml:
```
shell_command:
  curl_post: "curl -X POST \"{{ url }}\""
```

Create an account and then a Station in [PWS Weather](https://www.pwsweather.com).

Import the Blueprint

Enter your Station ID and API Key, then any weather values to share.
Ensure you select an entity to trigger data uploads (e.g. a temperature sensor).
