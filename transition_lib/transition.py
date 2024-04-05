import requests
from datetime import time

class Transition:
    BASE_URL = ""
    TOKEN = ""

    @staticmethod
    def __set_parameters(url, token):
        url = Transition.BASE_URL if url is None else url
        token = Transition.TOKEN if token is None else token
        return url, token

    @staticmethod
    def set_token(token):
        if token is not None and token != "":
            Transition.TOKEN = token            
        else:
            raise ValueError("Token cannot be empty.")
        
    @staticmethod
    def set_url(url):
        if url is not None and url != "":
            Transition.BASE_URL = url
        else:
            raise ValueError("URL cannot be empty.")
    
    @staticmethod
    def __build_body(username, password):
        if username is None or password is None:
            raise ValueError("Username or password not set.")

        body = {
            "usernameOrEmail": username,
            "password": password
        }

        return body            

    @staticmethod
    def __build_headers(token=None):
        token = Transition.TOKEN if token is None else token
        if token is None or token == "":
            raise ValueError("Token not set.")
        
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return headers
    
    @staticmethod
    def request_token(username, password,url=None):
        url = Transition.BASE_URL if url is None else url
        body = Transition.__build_body(username, password)
        response = requests.post(f"{url}/token", json=body)
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_paths(url=None, token=None):
        url, token = Transition.__set_parameters(url, token)           
        headers = Transition.__build_headers(token)
        response = requests.get(f"{url}/api/paths", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_nodes(url=None, token=None):
        url, token = Transition.__set_parameters(url, token)
        headers = Transition.__build_headers(token)
        response = requests.get(f"{url}/api/nodes", headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_scenarios(url=None, token=None):
        url, token = Transition.__set_parameters(url, token)
        headers = Transition.__build_headers(token)
        response = requests.get(f"{url}/api/scenarios", headers=headers)
        response.raise_for_status()
        return response.json()
        
    @staticmethod    
    def get_routing_modes(url=None, token=None):
        url, token = Transition.__set_parameters(url, token)
        headers = Transition.__build_headers(token)
        response = requests.get(f"{url}/api/routing-modes", headers=headers)
        response.raise_for_status()
        response = [x.replace("[", "").replace("]", "").replace('"', "") for x in response.text.split(",")]
        return response

    @staticmethod
    def request_accessibility_map(coordinates,
                              scenario_id, 
                              departure_or_arrival_choice,
                              departure_or_arrival_time: time,
                              n_polygons,
                              delta_minutes,
                              delta_interval_minutes,
                              place_name,
                              max_total_travel_time_minutes,
                              min_waiting_time_minutes,
                              max_access_egress_travel_time_minutes,
                              max_transfer_travel_time_minutes,
                              max_first_waiting_time_minutes,
                              walking_speed_kmh,
                              with_geojson,
                              url=None, 
                              token=None
                              ):
        departure_or_arrival_time_seconds_from_midnight = departure_or_arrival_time.hour * 3600 + departure_or_arrival_time.minute * 60 + departure_or_arrival_time.second
        departure_time_seconds = departure_or_arrival_time_seconds_from_midnight if departure_or_arrival_choice == "Departure" else None
        arrival_time_seconds = departure_or_arrival_time_seconds_from_midnight if departure_or_arrival_choice == "Arrival" else None

        body = {
            "departureTimeSecondsSinceMidnight": departure_time_seconds,
            "arrivalTimeSecondsSinceMidnight": arrival_time_seconds,
            "deltaIntervalSeconds": delta_interval_minutes * 60,
            "deltaSeconds": delta_minutes * 60,
            "numberOfPolygons": n_polygons,
            "minWaitingTimeSeconds": min_waiting_time_minutes * 60,
            "maxTransferTravelTimeSeconds": max_transfer_travel_time_minutes * 60,
            "maxAccessEgressTravelTimeSeconds": max_access_egress_travel_time_minutes * 60,
            "maxFirstWaitingTimeSeconds": max_first_waiting_time_minutes * 60,
            "walkingSpeedMps": walking_speed_kmh * (1000/3600),
            "maxTotalTravelTimeSeconds": max_total_travel_time_minutes * 60,
            "locationGeojson": {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": coordinates
                }
            },
        "scenarioId": scenario_id
        }

        url, token = Transition.__set_parameters(url, token)
        headers = Transition.__build_headers(token)
        params = {'withGeojson': 'true' if with_geojson else 'false'}
        response = requests.post(f"{url}/api/accessibility", headers=headers, json=body, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def request_routing_result(modes, 
                           origin, 
                           destination, 
                           scenario_id, 
                           departure_or_arrival_choice, 
                           departure_or_arrival_time, 
                           max_travel_time_minutes, 
                           min_waiting_time_minutes,
                           max_transfer_time_minutes, 
                           max_access_time_minutes, 
                           max_first_waiting_time_minutes, 
                           with_geojson,
                           with_alternatives,
                           url=None,
                           token=None):
        departure_or_arrival_time = departure_or_arrival_time.hour * 3600 + departure_or_arrival_time.minute * 60 + departure_or_arrival_time.second
        departure_time = departure_or_arrival_time if departure_or_arrival_choice == "Departure" else None
        arrival_time = departure_or_arrival_time if departure_or_arrival_choice == "Arrival" else None

        body = {
            "routingModes" : modes,
            "withAlternatives" : "true" if with_alternatives else "false",
            "departureTimeSecondsSinceMidnight" : departure_time,
            "arrivalTimeSecondsSinceMidnight" : arrival_time,
            "minWaitingTimeSeconds" : min_waiting_time_minutes * 60, 
            "maxTransferTravelTimeSeconds" : max_transfer_time_minutes * 60,
            "maxAccessEgressTravelTimeSeconds" : max_access_time_minutes * 60,
            "maxFirstWaitingTimeSeconds" : max_first_waiting_time_minutes * 60,
            "maxTotalTravelTimeSeconds" : max_travel_time_minutes * 60,
            "scenarioId" : scenario_id,
            "originGeojson" : {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": origin }
            },
            "destinationGeojson" : {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": destination }
            }
        }
        
        url, token = Transition.__set_parameters(url, token)
        headers = Transition.__build_headers(token)
        params = {"withGeojson": "true" if with_geojson else "false"}
        response = requests.post(f"{url}/api/route", headers=headers, json=body, params=params)
        response.raise_for_status()
        return response.json()
        
