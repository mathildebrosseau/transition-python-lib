import requests
import geojson
import os

class Transition:

    DEFAULT_URL = "http://localhost:8080/api/"

    def __init__(self):
        self.username = None
        self.password = None
        self.token = None
        self.body = None

    def build_body(self):
        self.username = os.environ.get('TRANSITION_USERNAME')
        self.password = os.environ.get('TRANSITION_PASSWORD')

        if self.username is None or self.password is None:
            raise ValueError("Username or password not set.")
        
        self.body = {
            "usernameOrEmail": self.username,
            "password": self.password
        }

    def build_headers(self):
        self.token = os.environ.get('TRANSITION_TOKEN')
        if self.token is None:
            raise ValueError("No token found.")
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def call_api(self):
        try:
            self.build_body()
            response = requests.post(self.DEFAULT_URL, json=self.body)
            if response.status_code == 200:
                print(f"Request successfull: {response.text}")
                return response
            else:
                print(f"Request unsuccessfull: {response.status_code} {response.text}")
                return response
        except requests.RequestException as error:
            return error

    def get_transition_paths(self):
        try:
            self.build_body()
            geojson_file = requests.post(f"{self.DEFAULT_URL}paths", json=self.body)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
        except requests.RequestException as error:
            return error
        
    def get_transition_nodes(self):
        try:
            self.build_body()
            geojson_file = requests.post(f"{self.DEFAULT_URL}nodes", json=self.body)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
        except requests.RequestException as error:
            return error
        
    def get_transition_scenarios(self):
        try:
            self.build_body()
            result = requests.post(f"{self.DEFAULT_URL}scenarios", json=self.body)
            if result.status_code == 200:
                scenarios = [entry['name'] for entry in result.json()['collection']]
                return scenarios
            else:
                return f"Request unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
        
    def get_transition_routing_modes(self):
        try:
            self.build_body()
            result = requests.post(f"{self.DEFAULT_URL}routing-modes", json=self.body)
            if result.status_code == 200:
                # Query returns the list as a string, so we need to parse it.
                # Can probably be done differently
                result = [x.replace("[", "").replace("]", "").replace('"', "") for x in result.text.split(",")]
                return result
            else:
                print(f"Routing modes request unsuccessfull: {result.status_code} {result.text}")
                return f"Request unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
        
    
    # The following methods are not used with the current endpoint implementation,
    # but will be used when tha API is updated to include the token.
            
    # def call_api_queries(self):
    #     try:
    #         self.build_headers()
    #         response = requests.post(f"{self.DEFAULT_URL}queries", headers=self.headers)
    #         if response.status_code == 200:
    #             print(f"Request successfull: {response.text}")
    #             return f"Request successfull: {response.text}"
    #         else:
    #             print(f"Request unsuccessfull: {response.status_code} {response.text}")
    #             return f"Request unsuccessfull: {response.status_code} {response.text}"
    #     except requests.RequestException as e:
    #         return f"Error: {e}"
        
    # def get_token(self):
    #     try:
    #         response = requests.get(f"{self.DEFAULT_URL}token", json=self.body)
    #         if response.status_code == 200:
    #             # Update the token in the config file
    #             config['credentials']['token'] = response.text
    #             with open('config.ini', 'w') as configfile:
    #                 config.write(configfile)
    #             return f"Request successfull: {response.text}"
    #         else:
    #             print(f"Request unsuccessfull: {response.status_code} {response.text}")
    #             return f"Request unsuccessfull: {response.status_code} {response.text}"
    #     except requests.RequestException as e:
    #         return f"Error: {e}"
        

