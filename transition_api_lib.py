import requests
import configparser
import json
import geojson

username = "manel"
password = "ThisIsAPassword"
url = 'http://localhost:8080/api/' 

# we could prompt the user for the username and password
body = {
    "usernameOrEmail": username,
    "password": password
}

def call_api():
    try:
        
        response = requests.post(url, json=body)
        if response.status_code == 200:
            print(f"Request successfull: {response.text}")
            return f"Request successfull: {response.text}"
            
        else:
            print(f"Request unsuccessfull: {response.status_code} {response.text}")
            return f"Request unsuccessfull: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Error: {e}"


def get_transition_paths():
    try:
        geojson_file = requests.post(url+"paths", json=body)
        if geojson_file.status_code == 200:
            print(f"Paths request successfull")
            result = geojson.loads(geojson_file.text)
            return result
        else:
            print(f"Paths request unsuccessfull: {geojson_file.status_code} {geojson_file.text}")
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    
def get_transition_nodes():
    try:
        geojson_file = requests.post(url+"nodes", json=body)
        if geojson_file.status_code == 200:
            print(f"Nodes request successfull")
            result = geojson.loads(geojson_file.text)
            return result
        else:
            print(f"Nodes request unsuccessfull: {geojson_file.status_code} {geojson_file.text}")
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    
def get_transition_scenarios():
    try:
        geojson_file = requests.post(url+"scenarios", json=body)
        if geojson_file.status_code == 200:
            print(f"Scenarios request successfull")
            result = geojson.loads(geojson_file.text)
            return result
        else:
            print(f"Scenarios request unsuccessfull: {geojson_file.status_code} {geojson_file.text}")
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    
def get_transition_routing_modes():
    try:
        geojson_file = requests.post(url+"routing-modes", json=body)
        if geojson_file.status_code == 200:
            print(f"Routing modes request successfull")
            result = geojson.loads(geojson_file.text)
            return result
        else:
            print(f"Routing modes request unsuccessfull: {geojson_file.status_code} {geojson_file.text}")
            return f"Request unsuccessfull: {geojson_file.status_code} {geojson_file.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    

get_transition_paths()
get_transition_nodes()
get_transition_scenarios()
get_transition_routing_modes()