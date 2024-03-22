import requests
import geojson
import os
import configparser

from datetime import time

class Transition:
    BASE_URL = "http://localhost:8080"
    API_URL = f"{BASE_URL}/api"

    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    
    if not os.path.isfile(config_path):
        config['credentials'] = {
            'username': '',
            'token': ''
        }
        config['URL'] = {
            'development': 'http://localhost:8080',
            'production': ''
        }
        with open(config_path, 'w') as config_file:
            config.write(config_file)
    else:
        config.read(config_path)
            
    @staticmethod
    def set_username(username):
        if username is not None and username != "":
            Transition.config['credentials']['username'] = username
            with open(Transition.config_path, 'w') as config_file:
                Transition.config.write(config_file)
        else:
            raise ValueError("Username or password cannot be empty.")

    @staticmethod
    def set_token(token):
        if token is not None and token != "":
            Transition.config['credentials']['token'] = token
            with open(Transition.config_path, 'w') as config_file:
                Transition.config.write(config_file)
        else:
            raise ValueError("Token cannot be empty.")
        
    @staticmethod
    def set_url(url):
        if url is not None and url != "":
            Transition.BASE_URL = Transition.config['URL'][url]
            Transition.API_URL = f"{Transition.BASE_URL}/api"
        else:
            raise ValueError("URL cannot be empty.")
        
    @staticmethod
    def get_configurations():
        return Transition.config
    
    @staticmethod
    def build_body(username, password):
        if username is None or password is None:
            raise ValueError("Username or password not set.")
        
        body = {
            "usernameOrEmail": username,
            "password": password
        }

        return body            

    @staticmethod
    def build_headers():
        token = Transition.config['credentials']['token']

        if token is None or token == "":
            token = Transition.get_token().text
            Transition.config['credentials']['token'] = token

            with open(Transition.config_path, 'w') as config_file:
                Transition.config.write(config_file)
        
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return headers

    @staticmethod
    def get_paths():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/paths", headers=headers)
            result.raise_for_status()
            return result.json()
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_nodes():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/nodes", headers=headers)
            result.raise_for_status()
            return result.json()
        except requests.RequestException as error:
            return error
    
    @staticmethod
    def get_scenarios():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/scenarios", headers=headers)
            result.raise_for_status()
            return result
        except requests.RequestException as error:
            return error
        
    @staticmethod    
    def get_routing_modes():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/routing-modes", headers=headers)
            result.raise_for_status()
            if result.status_code == 200:
                result = [x.replace("[", "").replace("]", "").replace('"', "") for x in result.text.split(",")]
            return result
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_accessibility_map(with_geojson,
                              departure_or_arrival_choice,
                              departure_or_arrival_time: time,
                              n_polygons,
                              delta_minutes,
                              delta_interval_minutes,
                              scenario_id, 
                              place_name,
                              max_total_travel_time_minutes,
                              min_waiting_time_minutes,
                              max_access_egress_travel_time_minutes,
                              max_transfer_travel_time_minutes,
                              max_first_waiting_time_minutes,
                              walking_speed_kmh,
                              coord_latitude,
                              coord_longitude
                              ):
        try:
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
                        "coordinates": [
                            coord_longitude,
                            coord_latitude
                        ]
                    }
                },
            "scenarioId": scenario_id
            }

            headers = Transition.build_headers()
            params = {'withGeojson': 'true' if with_geojson else 'false'}
            result = requests.post(f"{Transition.API_URL}/accessibility", headers=headers, json=body, params=params)
            if result.status_code == 200:
                geojson_file = geojson.dumps(result.json()['polygons'])
                with open("access.geojson", 'w') as file:
                    file.write(geojson_file)
                return geojson_file
            return result
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_token(username, password):
        try:
            body = Transition.build_body(username, password)
            response = requests.post(f"{Transition.BASE_URL}/token", json=body)
            if response.status_code == 200:
                Transition.config['credentials']['token'] = response.text

            with open(Transition.config_path, 'w') as config_file:
                Transition.config.write(config_file)
            return response
        except requests.RequestException as error:
            return error

        