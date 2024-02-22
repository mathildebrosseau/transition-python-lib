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
            'base_url': 'http://localhost:8080',
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_path)

    @staticmethod
    def set_base_url():
        url = os.environ.get('TRANSITION_BASE_URL')
        if url is not None and url != "":
            Transition.BASE_URL = url
            Transition.API_URL = f"{Transition.BASE_URL}/api"
            Transition.config['URL']['base_url'] = Transition.BASE_URL
            with open(Transition.config_path, 'w') as configfile:
                Transition.config.write(configfile)

    
    @staticmethod
    def build_body():
        username = os.environ.get('TRANSITION_USERNAME')
        password = os.environ.get('TRANSITION_PASSWORD')

        if username is None or password is None:
            raise ValueError("Username or password not set.")

        # save the username in the config file
        Transition.config['credentials']['username'] = username

        with open(Transition.config_path, 'w') as configfile:
            Transition.config.write(configfile)
        
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

            with open(Transition.config_path, 'w') as configfile:
                Transition.config.write(configfile)
        
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
                return response
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
            geojson_file = requests.get(f"{Transition.API_URL}/nodes", headers=headers)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request to /nodes unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
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
            else:
                return f"Request to /routing-modes unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_token():
        try:
            Transition.set_base_url()
            body = Transition.build_body()
            response = requests.post(f"{Transition.BASE_URL}/token", json=body)
            print(response.text)
            if response.status_code == 200:
                os.environ['TRANSITION_TOKEN'] = response.text
                return response
            else:
                return response
        except requests.RequestException as error:
            return error
        