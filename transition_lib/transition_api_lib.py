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
        