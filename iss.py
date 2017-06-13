import requests

API_HOST = 'http://api.open-notify.org/iss-pass.json'


def get_next_passes(lat, lng, n=5):

    params = {
        'lat': lat, 
        'lon': lng, 
        'n': n
    }

    data = requests.get(API_HOST, params=params).json()
    response = data.get('response')

    return response

