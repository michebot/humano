import os, requests, json


# Google Maps JS API Key
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


def reverse_geocode(lat, lng):
    """Call Google Geocoding API"""

    payload = {"latlng": "{},{}".format(lat, lng),
               "key": os.environ["GOOGLE_API_KEY"]}

    url = "https://maps.googleapis.com/maps/api/geocode/json?"

    results = requests.get(url, params=payload).json()

    return results