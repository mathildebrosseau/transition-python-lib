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
            'password': '',
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
    def set_credentials(username, password):
        if username is not None and password is not None and username != "" and password != "":
            Transition.config['credentials']['username'] = username
            Transition.config['credentials']['password'] = password
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
    def build_body():
        username = Transition.config['credentials']['username']
        password = Transition.config['credentials']['password']

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
    def call_api():
        try:
            headers = Transition.build_headers()
            response = requests.get(Transition.API_URL, headers=headers)
            if response.status_code == 200:
                print(f"Request to /api successfull")
            else:
                print(f"Request to /api unsuccessfull")
            return response
        except requests.RequestException as error:
            return error

    @staticmethod
    def get_transition_paths():
        try:
            headers = Transition.build_headers()
            geojson_file = requests.get(f"{Transition.API_URL}/paths", headers=headers)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request to /paths unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_transition_nodes():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/nodes", headers=headers)
            if result.status_code == 200:
                geojson_file = geojson.loads(result.text)
                return geojson_file
            else:
                return f"Request to /nodes unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
    
    @staticmethod
    def get_transition_scenarios():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/scenarios", headers=headers)
            if result.status_code == 200:
                scenarios = [entry['name'] for entry in result.json()['collection']]
                return scenarios
            else:
                return f"Request to /scenarios unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
        
    @staticmethod    
    def get_transition_routing_modes():
        try:
            headers = Transition.build_headers()
            result = requests.get(f"{Transition.API_URL}/routing-modes", headers=headers)
            if result.status_code == 200:
                # Query returns the list as a string, so we need to parse it.
                # Can probably be done differently
                result = [x.replace("[", "").replace("]", "").replace('"', "") for x in result.text.split(",")]
            return result
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_accessibility_map(with_geometry,
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
            arrival_time_seconds = departure_or_arrival_time_seconds_from_midnight if departure_or_arrival_choice == "Departure" else None

            parameters = {
                "departureTimeSecondsSinceMidnight": departure_time_seconds,
                "arrivalTimeSecondsSinceMidnight": arrival_time_seconds,
                "deltaIntervalSeconds": delta_interval_minutes * 60,
                "deltaSeconds": delta_minutes * 60,
                "numberOfPolygons": n_polygons,
                "minWaitingTimeSeconds": min_waiting_time_minutes * 60,
                "maxTransferTravelTimeSeconds": max_transfer_travel_time_minutes * 60,
                "maxAccessEgressTravelTimeSeconds": max_access_egress_travel_time_minutes * 60,
                #"maxWalkingOnlyTravelTimeSeconds": 1800,
                "maxFirstWaitingTimeSeconds": max_first_waiting_time_minutes * 60,
                "walkingSpeedMps": walking_speed_kmh * (3600/1000),
                "maxTotalTravelTimeSeconds": max_total_travel_time_minutes * 60,
                #"locationColor": "rgba(47, 138, 243, 1.0)",
                "locationGeojson": {
                    "type": "Feature",
                    #"id": 1,
                    #"properties": {
                    #"id": 1,
                    #"color": "rgba(47, 138, 243, 1.0)",
                    #"location": "accessibilityMapLocation"
                    #},
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
            print(parameters)

            headers = Transition.build_headers()
            result = requests.post(f"{Transition.API_URL}/accessibility/true", headers=headers, json=parameters)
            if result.status_code == 200:
                geojson_file = geojson.dumps(result.json()['strokes']['features'][0])
                with open("access.geojson", 'w') as file:
                    file.write(geojson_file)
                return geojson_file
            return result
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_token():
        try:
            body = Transition.build_body()
            response = requests.post(f"{Transition.BASE_URL}/token", json=body)
            print(response.text)
            if response.status_code == 200:
                os.environ['TRANSITION_TOKEN'] = response.text
            return response
        except requests.RequestException as error:
            return error

        