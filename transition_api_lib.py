import requests
import configparser
import geojson
import os


# change working directory to the correct path
config_path = os.path.join(os.path.dirname(__file__))
os.chdir(config_path)

config = configparser.ConfigParser()
config.read('config.ini')


username = config['credentials']['username']
password = config['credentials']['password']

url = config['URL']['dev']

body = {
    "usernameOrEmail": username,
    "password": password
}

def call_api():
    try:
        
        response = requests.post(url, json=body)
        if response.status_code == 200:
            return f"Request successfull: {response.text}"
            
        else:
            return f"Request unsuccessfull: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Error: {e}"


def get_transition_paths():
    try:
        geojson_file = requests.post(url+"paths", json=body)
        if geojson_file.status_code == 200:
            result = geojson.loads(geojson_file.text)
            return result
        else:
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"


def get_transition_nodes():
    try:
        geojson_file = requests.post(url+"nodes", json=body)
        if geojson_file.status_code == 200:
            result = geojson.loads(geojson_file.text)
            return result
        else:
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    

def get_transition_scenarios():
    try:
        result = requests.post(url+"scenarios", json=body)
        if result.status_code == 200:
            return result
        else:
            return f"Request unsuccessfull: {result.status_code} {result.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
   
    
def get_transition_routing_modes():
    try:
        result = requests.post(url+"routing-modes", json=body)
        if result.status_code == 200:
            # Query returns the list as a string, so we need to parse it.
            # Can probably be done differently
            result = [x.replace("[", "").replace("]", "").replace('"', "") for x in result.text.split(",")]
            return result
        else:
            print(f"Routing modes request unsuccessfull: {result.status_code} {result.text}")
            return f"Request unsuccessfull: {result.status_code} {result.text}"
    except requests.RequestException as e:
        return f"Error: {e}"