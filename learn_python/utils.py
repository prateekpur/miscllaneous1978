import requests
REQUEST_TIMEOUT_SECONDS = 10

def check_input_num(prompt):
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input, please enter a number")

def check_input_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input, please enter a float")

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

def safe_get(res, field, default=None):
    if field in res :
        return res[field]
    return default