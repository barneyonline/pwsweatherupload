# PWS Weather Upload Blueprint
Upload weather data from Home Assistant to a PWS Weather station

## Setup
1. Add the following lines to your Home Assistant configuraiton.yaml:
```
shell_command:
  curl_post: "curl -X POST \"{{ url }}\""
```

2. Restart Home Assistant.
3. Create an account and then a Station in [PWS Weather](https://www.pwsweather.com).

4. Import the Blueprint:

  <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fbarneyonline%2Fpwsweatherupload%2Fblob%2Fmain%2Fpws_weather_upload.yaml" target="_blank" rel="noreferrer noopener"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a>

5. Enter your Station ID and API Key, then any weather values to share.
6. Ensure you select an entity to trigger data uploads (e.g. a temperature sensor).
7. Save Automation.

## Credits
* [David Defreest House](https://github.com/OurColonial) for sharing PWS Weather API spec in the [WeatherLink-to-PWSweather](https://github.com/OurColonial/WeatherLink-to-PWSweather) script
* [Dirk van Donkelaar](https://community.home-assistant.io/u/dvandonkelaar/summary) for providing baseline blueprint structure as part of the [WUnderground data uploader blueprint](https://community.home-assistant.io/t/wunderground-data-uploader/330332)
