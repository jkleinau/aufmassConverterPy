import json
import requests



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


USER_AGENT = 'jkleinau'
API_KEY = '5e5218e14b0315bc56d3991d49b53675'


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


r = requests.get("https://api.chucknorris.io/jokes/random")
jprint(r.json()['value'])

# requests_cache.install_cache()
#
# r = lastfm_get({
#     'method': 'chart.gettopartists'
# })
# print(r.status_code)
# jprint(r.json()['artists']['@attr'])
#
# parameters = {
#     "lat": 40.71,
#     "lon": -74,
#     "n": 20
# }
# response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# print(response.status_code)
#
# pass_times = response.json()['response']
#
# risetimes = []
#
# for d in pass_times:
#     time = d['risetime']
#     risetimes.append(time)
#
# times = []
#
# for rt in risetimes:
#     time = datetime.fromtimestamp(rt)
#     times.append(time)
#     print(time)
