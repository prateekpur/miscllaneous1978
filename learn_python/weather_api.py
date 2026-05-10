import requests
from utils import check_input_float, check_input_num
from dataclasses import dataclass

REQUEST_TIMEOUT_SECONDS = 10

@dataclass
class Location:
    lat: float
    lon: float

def call_get_api(url, params):
    try : 
        if params is None :
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        else :
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)

    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)

    except requests.exceptions.Timeout as e:
        print("Request timed out:", e)

    except requests.exceptions.RequestException as e:
        print("General request error:", e)


def get_weather(location):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.lat,
        "longitude": location.lon,
        "current_weather": True
    }
    data = call_get_api(url, params)
    if data is not None :
        if "current_weather" in data:
            jsonobj = data["current_weather"]
            for key, value in jsonobj.items():
                print (key , " : ", value)

def get_input():
    option = check_input_num("Enter 1 for lat long input, 2 for city : ")
    lat: float = 0.0
    lon: float = 0.0
    if option == 1 :
        lat = check_input_float("Input latitude : ")
        lon = check_input_float("Input longitude : ")
    elif option == 2 :
        city = input("Enter city name : ")
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city}

        geo_data = call_get_api(geo_url, geo_params)
        if geo_data is None : 
            return None
        if "results" in geo_data and len(geo_data["results"]) > 0:
            if "longitude" in geo_data["results"][0] and "latitude" in geo_data["results"][0] :
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
        else : 
            print("Wrong city entered")
            return None
    return Location(lat, lon)

if __name__ == "__main__":
    location = get_input()
    if location is not None :
        get_weather(location)
