# pwsweatherupload
Upload weather data from Home Assistant to a PWS Weather station

**Setup**
Add the following lines to your Home Assistant configuraiton.yaml:
''
shell_command:
  curl_post: "curl -X POST \"{{ url }}\""
''

Create a Station in PWS Weather.
