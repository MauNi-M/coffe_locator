from pprint import pprint

import requests


def get_lat_lon_location(cafe_object):
    location_url = cafe_object.map_url
    # print(f"requested url: {location_url}")
    custom_headers = headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(location_url, allow_redirects=False)
    # print(response.status_code)
    # for key, value in response.headers.items():
    # print(f"{key} |------| {value}")
    # status code 302, means the request was found but a redirection was needed
    # the history attribute of the response object tracks this redirection
    # in order to prevent redirection, you use the allow_redirects parameter and set it to false
    # this allows me to get the location key of the headers dictionary of the not redirected response
    # which has the latitude and longitude of the shortened address link that i need for the mapbox api
    # print(response.status_code)
    # print(response.history)
    return response.headers["location"]


def get_latitude_longitude_from_google_address(google_address):
    # print(google_address)
    # print(google_address.split("/"))
    try:
        at = [item for item in google_address.split("/") if "@" in item][0]
        latitude = float(at.split(",")[0].replace("@", ""))
        longitude = float(at.split(",")[1])
    except:
        print(google_address)
        print(google_address.split("/"))
        return None
    return [longitude, latitude]
