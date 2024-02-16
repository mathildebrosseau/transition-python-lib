import requests
import geojson
import os

class Transition:

    DEFAULT_URL = "http://localhost:8080/api/"
    
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
            raise ValueError("No token found.")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return headers

    @staticmethod
    def call_api():
        try:
            body = Transition.build_body()
            response = requests.post(Transition.DEFAULT_URL, json=body)
            if response.status_code == 200:
                print(f"Request successfull: {response.text}")
                return response
            else:
                print(f"Request unsuccessfull: {response.status_code} {response.text}")
                return response
        except requests.RequestException as error:
            return error

    @staticmethod
    def get_transition_paths():
        try:
            body = Transition.build_body()
            geojson_file = requests.post(f"{Transition.DEFAULT_URL}paths", json=body)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
        except requests.RequestException as error:
            return error
        
    @staticmethod
    def get_transition_nodes():
        try:
            body = Transition.build_body()
            geojson_file = requests.post(f"{Transition.DEFAULT_URL}nodes", json=body)
            if geojson_file.status_code == 200:
                result = geojson.loads(geojson_file.text)
                return result
            else:
                return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
        except requests.RequestException as error:
            return error
    
    @staticmethod
    def get_transition_scenarios():
        try:
            body = Transition.build_body()
            result = requests.post(f"{Transition.DEFAULT_URL}scenarios", json=body)
            if result.status_code == 200:
                scenarios = [entry['name'] for entry in result.json()['collection']]
                return scenarios
            else:
                return f"Request unsuccessfull: {result.status_code} {result.text}"
        except requests.RequestException as error:
            return error
        
    @staticmethod    
    def get_transition_routing_modes():
        try:
            body = Transition.build_body()
            result = requests.post(f"{Transition.DEFAULT_URL}routing-modes", json=body)
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

    # @staticmethod     
    # def call_api_queries():
    #     try:
    #         headers = Transition.build_headers()
    #         response = requests.post(f"{Transition.DEFAULT_URL}queries", headers=Transition.headers)
    #         if response.status_code == 200:
    #             print(f"Request successfull: {response.text}")
    #             return f"Request successfull: {response.text}"
    #         else:
    #             print(f"Request unsuccessfull: {response.status_code} {response.text}")
    #             return f"Request unsuccessfull: {response.status_code} {response.text}"
    #     except requests.RequestException as e:
    #         return f"Error: {e}"
        
    # @staticmethod
    # def get_token():
    #     try:
    #         body = Transition.build_body()
    #         response = requests.get(f"{Transition.DEFAULT_URL}token", json=body)
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
        

