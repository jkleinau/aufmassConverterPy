import requests
import json


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


url = "http://demo.hafas.de/openapi/vbb-proxy"
acces_ID = "kleinau-4b3e-a26d-1aecf90133f9"

parameters = {
    'accesId': acces_ID,
    'name': 'jkleinau',
    'format': 'json',

}

r = requests.get(url + "/location.name?input=berlin", params=parameters)
print(r.status_code)
#jprint(r.json())
