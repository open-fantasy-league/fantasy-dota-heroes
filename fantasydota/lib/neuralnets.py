import requests


def get_prediction(data):
    pickbans_in = data["pickbans"]
    use_max = data["use_max"]
    allow_dupes = data["allow_dupes"]
    use_rnn = data["use_rnn"]
    r = requests.post("http://localhost:5000", data=data, allow_redirects=True)
    return r.content
