# calls an http API
# the api is at http://localhost:8080/api

import requests

def call_api():
    url = 'http://localhost:8080/api/' 
    try:
        # we could prompt the user for the username and password
        username = 'manel'
        password = 'ThisIsAPassword'

        body = {
            "usernameOrEmail": username,
            "password": password
        }
        
        response = requests.get(url, json=body)
        if response.status_code == 200:
            return f"Request successfull: {response.text}"
        else:
            return f"Request unsuccessfull: {response.status_code} {response.text}"
    except requests.RequestException as e:
        return f"Error: {e}"
    

call_api()
