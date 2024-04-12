# MIT License

# Copyright (c) 2024 Polytechnique Montréal

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
from datetime import time
import json

class Transition:
    def __init__(self, url, username, password, token=None):
        if url is None or url == "":
            raise ValueError("URL cannot be empty.")
        self.base_url = url

        # To instantiate Transition instance from token only
        if username is None and password is None and token is not None:
            self.token = token
        
        # To instantiate Transition instance from username and password authentication
        else:
            self.token = self.__request_token(username, password)

    # TODO : ajouter self
    def __build_body(self, username, password):
        if username is None or password is None:
            raise ValueError("Username or password empty.")

        body = {
            "usernameOrEmail": username,
            "password": password
        }

        return body            

    def __build_headers(self):
        if self.token is None or self.token == "":
            raise ValueError("Token not set.")
        
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return headers

    def __request_token(self, username, password):
        body = self.__build_body(username, password)
        response = requests.post(f"{self.base_url}/token", json=body)
        response.raise_for_status()
        return response.text

    def get_paths(self):      
        headers = self.__build_headers()
        response = requests.get(f"{self.base_url}/api/paths", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_nodes(self):
        headers = self.__build_headers()
        response = requests.get(f"{self.base_url}/api/nodes", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_scenarios(self):
        headers = self.__build_headers()
        response = requests.get(f"{self.base_url}/api/scenarios", headers=headers)
        response.raise_for_status()
        return response.json()
 
    def get_routing_modes(self):
        headers = self.__build_headers()
        response = requests.get(f"{self.base_url}/api/routing-modes", headers=headers)
        response.raise_for_status()
        return json.loads(response.text)

    def request_routing_result(self,
                               modes, 
                               origin, 
                               destination, 
                               scenario_id, 
                               departure_or_arrival_choice, 
                               departure_or_arrival_time, 
                               max_travel_time_minutes, 
                               min_waiting_time_minutes,
                               max_transfer_time_minutes, 
                               max_access_time_minutes, 
                               max_first_waiting_time_minutes, 
                               with_geojson,
                               with_alternatives):
        departure_or_arrival_time = departure_or_arrival_time.hour * 3600 + departure_or_arrival_time.minute * 60 + departure_or_arrival_time.second
        departure_time = departure_or_arrival_time if departure_or_arrival_choice == "Departure" else None
        arrival_time = departure_or_arrival_time if departure_or_arrival_choice == "Arrival" else None

        body = {
            "routingModes" : modes,
            "withAlternatives" : with_alternatives,
            "departureTimeSecondsSinceMidnight" : departure_time,
            "arrivalTimeSecondsSinceMidnight" : arrival_time,
            "minWaitingTimeSeconds" : min_waiting_time_minutes * 60, 
            "maxTransferTravelTimeSeconds" : max_transfer_time_minutes * 60,
            "maxAccessEgressTravelTimeSeconds" : max_access_time_minutes * 60,
            "maxFirstWaitingTimeSeconds" : max_first_waiting_time_minutes * 60,
            "maxTotalTravelTimeSeconds" : max_travel_time_minutes * 60,
            "scenarioId" : scenario_id,
            "originGeojson" : {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": origin }
            },
            "destinationGeojson" : {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": destination }
            }
        }
        
        headers = self.__build_headers()
        params = {"withGeojson": "true" if with_geojson else "false"}
        response = requests.post(f"{self.base_url}/api/route", headers=headers, json=body, params=params)
        response.raise_for_status()
        return response.json()

    def request_accessibility_map(self,
                                  coordinates,
                                  scenario_id, 
                                  departure_or_arrival_choice,
                                  departure_or_arrival_time: time,
                                  n_polygons,
                                  delta_minutes,
                                  delta_interval_minutes,
                                  place_name,
                                  max_total_travel_time_minutes,
                                  min_waiting_time_minutes,
                                  max_access_egress_travel_time_minutes,
                                  max_transfer_travel_time_minutes,
                                  max_first_waiting_time_minutes,
                                  walking_speed_kmh,
                                  with_geojson):
        departure_or_arrival_time_seconds_from_midnight = departure_or_arrival_time.hour * 3600 + departure_or_arrival_time.minute * 60 + departure_or_arrival_time.second
        departure_time_seconds = departure_or_arrival_time_seconds_from_midnight if departure_or_arrival_choice == "Departure" else None
        arrival_time_seconds = departure_or_arrival_time_seconds_from_midnight if departure_or_arrival_choice == "Arrival" else None

        body = {
            "departureTimeSecondsSinceMidnight": departure_time_seconds,
            "arrivalTimeSecondsSinceMidnight": arrival_time_seconds,
            "deltaIntervalSeconds": delta_interval_minutes * 60,
            "deltaSeconds": delta_minutes * 60,
            "numberOfPolygons": n_polygons,
            "minWaitingTimeSeconds": min_waiting_time_minutes * 60,
            "maxTransferTravelTimeSeconds": max_transfer_travel_time_minutes * 60,
            "maxAccessEgressTravelTimeSeconds": max_access_egress_travel_time_minutes * 60,
            "maxFirstWaitingTimeSeconds": max_first_waiting_time_minutes * 60 if max_first_waiting_time_minutes else None,
            "walkingSpeedMps": walking_speed_kmh * (1000/3600),
            "maxTotalTravelTimeSeconds": max_total_travel_time_minutes * 60,
            "locationGeojson": {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": coordinates
                }
            },
        "scenarioId": scenario_id
        }

        headers = Transition.__build_headers()
        params = {'withGeojson': 'true' if with_geojson else 'false'}
        response = requests.post(f"{self.base_url}/api/accessibility", headers=headers, json=body, params=params)
        response.raise_for_status()
        return response.json()
    