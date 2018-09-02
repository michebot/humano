import os, requests, json


# Google Places Key
GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]


def lawyer_details_api_call(g_place_id):
    """Call Google Place Details API"""

    payload = {"place_id": g_place_id,
               "fields": "name,rating,reviews,formatted_phone_number,opening_hours,formatted_address,geometry,url,website",
               "key": os.environ["GOOGLE_PLACES_API_KEY"]}

    url = "https://maps.googleapis.com/maps/api/place/details/json?"

    results = requests.get(url, params=payload).json()

    return results