import json
import requests
import geojson
import os
import configparser

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
                # print(result.text)
                # scenarios = [entry['name'] for entry in result.json()['collection']]
                return result
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

    @staticmethod
    def get_routing_result(modes, 
                           origin, 
                           destination, 
                           scenario_id, 
                           max_travel_time, 
                           min_waiting_time,
                           max_transfer_time, 
                           max_access_time, 
                           departure_or_arrival_time, 
                           departure_or_arrival_label, 
                           max_first_waiting_time, 
                           with_geojson):
        try:
            departure_or_arrival_time = departure_or_arrival_time.hour * 3600 + departure_or_arrival_time.minute * 60 + departure_or_arrival_time.second
            departure_time = departure_or_arrival_time if departure_or_arrival_label == "Departure" else None
            arrival_time = departure_or_arrival_time if departure_or_arrival_label == "Arrival" else None

            options = {
                "withGeojson": "true" if with_geojson else "false"
            }

            parameters = {
                "routingModes" : modes,
                "withAlternatives" : "false",
                "departureTimeSecondsSinceMidnight" : departure_time,
                "arrivalTimeSecondsSinceMidnight" : arrival_time,
                "minWaitingTimeSeconds" : min_waiting_time * 60, 
                "maxTransferTravelTimeSeconds" : max_transfer_time * 60,
                "maxAccessEgressTravelTimeSeconds" : max_access_time * 60,
                "maxFirstWaitingTimeSeconds" : max_first_waiting_time * 60,
                "maxTotalTravelTimeSeconds" : max_travel_time * 60,
                "scenarioId" : scenario_id,
                "originGeojson" : {
                    "type": "Feature",
                    "id": 1,
                    "properties": { "id": 1, "color": "rgba(140, 212, 0, 1.0)", "location": "origin" },
                    "geometry": { "type": "Point", "coordinates": origin }
                },
                "destinationGeojson" : {
                    "type": "Feature",
                    "id": 1,
                    "properties": { "id": 2, "color": "rgba(212, 35, 14, 1.0)", "location": "destination" },
                    "geometry": { "type": "Point", "coordinates": destination }
                }
            }
            headers = Transition.build_headers()
            result = requests.post(f"{Transition.API_URL}/route", headers=headers, json=parameters, params=options)
            return result
        except requests.RequestException as error:
            return error
