import json

import requests


def get_prediction(data):
    pickbans_in = data["pickbans"]
    use_max = data["use_max"]
    allow_dupes = data["allow_dupes"]
    use_rnn = data["use_rnn"]
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://37.97.191.14:5000/", data=json.dumps(data), headers=headers)
    return r.content, r.status_code
