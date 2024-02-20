import requests
import geojson
import os

class Transition:
    DEFAULT_URL = "http://localhost:8080"
    API_URL = f"{DEFAULT_URL}/api"
    
    @staticmethod
    def build_body():
        username = os.environ.get('TRANSITION_USERNAME')
        password = os.environ.get('TRANSITION_PASSWORD')

        if username is None or password is None:
            raise ValueError("Username or password not set.")
        
        body = {
            "usernameOrEmail": username,
            "password": password
        }
        return body

    @staticmethod
    def build_headers():
        token = os.environ.get('TRANSITION_TOKEN')
        if token is None:
            Transition.get_token()
            token = os.environ.get('TRANSITION_TOKEN')
        
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
                print(f"Request to /api successfull: {response.text}")
                return response
            else:
                print(f"Request to /api unsuccessfull: {response.status_code} {response.text}")
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
            body = Transition.build_body()
            response = requests.post(f"{Transition.DEFAULT_URL}/token", json=body)
            if response.status_code == 200:
                os.environ['TRANSITION_TOKEN'] = response.text
                return f"Request to /token successfull: {response.text}"
            else:
                return f"Request to /token unsuccessfull: {response.status_code} {response.text}"
        except requests.RequestException as error:
            return error
        

