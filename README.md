# PWS Weather Upload Blueprint
Upload weather data from Home Assistant to a PWS Weather station

## Setup
1. Add the following lines to your Home Assistant `configuration.yaml`. This
   defines a `rest_command` named `pws_upload` that the blueprint uses to send
   data to PWSWeather without spawning an external process. Your Station ID and
   API key will be passed as part of the request URL:
```
rest_command:
  pws_upload:
    url: "{{ url }}"
    method: POST
```

2. Restart Home Assistant.
3. Create an account and then a Station in [PWS Weather](https://www.pwsweather.com).

4. Import the Blueprint:

  <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fbarneyonline%2Fpwsweatherupload%2Fblob%2Fmain%2Fpws_weather_upload.yaml" target="_blank" rel="noreferrer noopener"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a>

5. Enter your Station ID and API Key, then any weather values to share.
6. Ensure you select an entity to trigger data uploads (e.g. a temperature sensor).
7. Optionally set a **Minimum Upload Interval** if you want to throttle how
   often data is sent to PWSWeather.
8. Save Automation.

The file `PWSweather-API_string_2020.txt` lists all parameters supported by the
PWSWeather API. Use it as a reference when deciding which sensors to include.

`PWS_Upload_sample.py` can be run from the command line to test API requests
without Home Assistant. Replace the placeholder Station ID and API key in the
script before running.

## Credits
* [David Defreest House](https://github.com/OurColonial) for sharing PWS Weather API spec in the [WeatherLink-to-PWSweather](https://github.com/OurColonial/WeatherLink-to-PWSweather) script
* [Dirk van Donkelaar](https://community.home-assistant.io/u/dvandonkelaar/summary) for providing baseline blueprint structure as part of the [WUnderground data uploader blueprint](https://community.home-assistant.io/t/wunderground-data-uploader/330332)
