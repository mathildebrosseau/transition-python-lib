# calls an http API
# the api is at http://localhost:8080/api

import requests
import configparser
import os

config = configparser.ConfigParser()
config_path = 'config.ini'

config.read(config_path)
username = config['credentials']['username']
password = config['credentials']['password']

def call_api():
    url = 'http://localhost:8080/api/' 
    try:
        # we could prompt the user for the username and password

        body = {
            "usernameOrEmail": username,
            "password": password
        }
        
        response = requests.post(url, json=body)
        if response.status_code == 200:
            print(f"Request successfull: {response.text}")
            return f"Request successfull: {response.text}"
            
        else:
            print(f"Request unsuccessfull: {response.status_code} {response.text}")
            return f"Request unsuccessfull: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    

call_api()
