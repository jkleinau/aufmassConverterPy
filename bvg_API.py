import requests
import json


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


URL = "http://demo.hafas.de/openapi/vbb-proxy"
ID = "kleinau-4b3e-a26d-1aecf90133f9"

parameters = {
    'accesId': ID,
    'name': 'jkleinau',
    'format': 'json',

}

r = requests.get(URL + "/location.name?input=berlin", params=parameters)
print(r.status_code)
jprint(r.json())
