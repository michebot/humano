import os, requests, json


# Google Places Key
GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]


def lawyer_search_google_api_call():
    """Call Google Places Text Search API"""

    payload = {"query": "immigration",
              "location": "37.7886981,-122.4115725",
               "radius": 50000,
               "type": "lawyer",
               "key": os.environ["GOOGLE_PLACES_API_KEY"]}

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    results = requests.get(url, params=payload).json()

    return results



# def lawyer_search_google_api_call(lat, lng):
#     """Call Google Places Text Search API"""

#     # NEED TO CHANGE this allow user's to enter location or ask for user's location
#     # lat_lng = [37.7886981, -122.4115725]
#     # "location": "37.7886981,-122.4115725",

#     payload = {"query": "immigration",
#               "location": "lat,lng",
#                "radius": 50000,
#                "type": "lawyer",
#                "key": os.environ["GOOGLE_PLACES_API_KEY"]}

#     url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

#     results = requests.get(url, params=payload).json()

#     return results



def more_lawyers_google_api_call(next_pg_token):
    """Render more pages with lawyers"""

    payload = {'pagetoken': next_page_token,
               'key': os.environ['GOOGLE_API_KEY']
               }
               
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    results = requests.get(url, params=payload).json()

    return results