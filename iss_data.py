# API usage
import json
import requests

# Request data about who's on the ISS
response = requests.get("http://api.open-notify.org/astros.json")
# print(response.status_code)

# Prints received JSON
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

# When will the ISS pass NYC? (API not available anymore)
# parameters = {
#     "lat": 40.71,
#     "lon": -74
# }
# response = requests.get("https://api.open-notify.org/iss-pass.json", params=parameters)

# jprint(response.json())

# Where is the ISS right now?
response = requests.get("http://api.open-notify.org/iss-now.json")
jprint(response.json())