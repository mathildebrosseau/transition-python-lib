import unittest
from unittest.mock import patch
import requests
import requests_mock
from datetime import time

from ..transition_lib.transition import Transition

class TestTransition(unittest.TestCase):
    def setUp(self):
        self.test_url = "https://example.com"
        self.test_token = "test_token"
        self.test_username = "test_username"
        self.test_password = "test_password"
        self.mock_response = unittest.mock.Mock()
        self.test_accessibility_params = {
            "departureTimeSecondsSinceMidnight": 0,
            "arrivalTimeSecondsSinceMidnight": None,
            "deltaIntervalSeconds": 60,
            "deltaSeconds": 60,
            "numberOfPolygons": 1,
            "minWaitingTimeSeconds": 60,
            "maxTransferTravelTimeSeconds": 60,
            "maxAccessEgressTravelTimeSeconds": 60,
            "maxFirstWaitingTimeSeconds": 60,
            "walkingSpeedMps": (1000/3600),
            "maxTotalTravelTimeSeconds": 60,
            "locationGeojson": {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        0,
                        0
                    ]
                }
            },
        "scenarioId": "scenario-id"
        }
        self.test_route_params = {
            "routingModes": ["mode1", "mode2"],
            "withAlternatives": "false",
            "departureTimeSecondsSinceMidnight": 0,
            "arrivalTimeSecondsSinceMidnight": None,
            "minWaitingTimeSeconds": 60, 
            "maxTransferTravelTimeSeconds": 60,
            "maxAccessEgressTravelTimeSeconds":  60,
            "maxFirstWaitingTimeSeconds":  60,
            "maxTotalTravelTimeSeconds":  60,
            "scenarioId": "scenario-id",
            "originGeojson": {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": [0,0] }
            },
            "destinationGeojson": {
                "type": "Feature",
                "id": 1,
                "geometry": { "type": "Point", "coordinates": [0,0] }
            }
        }
        self.test_options = { "withGeojson": "true", "withAlternatives": False }
        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)

    def test_set_token(self):
        Transition.set_token(self.test_token)
        self.assertEqual(Transition.TOKEN, self.test_token)

    def test_set_token_empty(self):
        self.assertRaises(ValueError, Transition.set_token, None)

    def test_set_url(self):
        Transition.set_url(self.test_url)
        self.assertEqual(Transition.BASE_URL, self.test_url)
    
    def test_set_url_empty(self):
        self.assertRaises(ValueError, Transition.set_url, None)

    def test_build_body(self):
        body = Transition._Transition__build_body(self.test_username, self.test_password)
        self.assertEqual(body, {"usernameOrEmail": self.test_username, "password": self.test_password})

    def test_build_body_empty(self):
        self.assertRaises(ValueError, Transition._Transition__build_body, None, None)

    def test_build_headers(self):
        headers = Transition._Transition__build_headers(self.test_token)
        self.assertEqual(headers, {"Authorization": f"Bearer {self.test_token}"})

    def test_build_headers_empty(self):
        Transition.TOKEN = None
        self.assertRaises(ValueError, Transition._Transition__build_headers, None)
        self.assertRaises(ValueError, Transition._Transition__build_headers)

    def test_request_token(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/token", text=self.test_token, status_code=200)
            res = Transition.request_token(self.test_username, self.test_password, self.test_url)
            self.assertTrue(m.called)
            self.assertEqual(res, self.test_token)

    def test_request_token_error(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/token", text=self.test_token, status_code=400)
            self.assertRaises(requests.exceptions.HTTPError, Transition.request_token, self.test_username, self.test_password)
            self.assertTrue(m.called_once)

    def test_get_paths(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/paths", json={"key": "value"}, status_code=200)
            res = Transition.get_paths()
            self.assertTrue(m.called_once)
            self.assertEqual(res, {"key": "value"})

    def test_get_paths_error(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/paths", json={"key": "value"}, status_code=400)
            self.assertRaises(requests.exceptions.HTTPError, Transition.get_paths)
            self.assertTrue(m.called_once)

    def test_get_nodes(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/nodes",json={"key": "value"}, status_code=200)
            res = Transition.get_nodes()
            self.assertTrue(m.called_once)
            self.assertEqual(res, {"key": "value"})
    
    def test_get_nodes_error(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/nodes",json={"key": "value"}, status_code=400)
            self.assertRaises(requests.exceptions.HTTPError, Transition.get_nodes)
            self.assertTrue(m.called_once)

    def test_get_scenarios(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/scenarios", json={"key": "value"}, status_code=200)
            res = Transition.get_scenarios()
            self.assertTrue(m.called_once)
            self.assertEqual(res, {"key": "value"})
        
    def test_get_scenarios_error(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/scenarios", json={"key": "value"}, status_code=400)
            self.assertRaises(requests.exceptions.HTTPError, Transition.get_scenarios)
            self.assertTrue(m.called_once)

    def test_get_routing_modes(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/routing-modes", text='["mode1","mode2"]', status_code=200)
            modes = Transition.get_routing_modes()
            self.assertTrue(m.called_once)
            self.assertEqual(modes, ["mode1", "mode2"])
        
    def test_get_routing_modes_error(self):
        with requests_mock.Mocker() as m:
            m.get(f"{self.test_url}/api/routing-modes", text='["mode1","mode2"]', status_code=400)
            self.assertRaises(requests.exceptions.HTTPError, Transition.get_routing_modes)
            self.assertTrue(m.called_once)

    def test_request_accessibility_map(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/api/accessibility",json={"key": "value"}, status_code=200)
            res = Transition.request_accessibility_map(
                coordinates=[0, 0],
                scenario_id="scenario-id",
                departure_or_arrival_choice="Departure",
                departure_or_arrival_time=time(0, 0, 0),
                n_polygons=1,
                delta_minutes=1,
                delta_interval_minutes=1,
                place_name="place",
                max_total_travel_time_minutes=1,
                min_waiting_time_minutes=1,
                max_access_egress_travel_time_minutes=1,
                max_transfer_travel_time_minutes=1,
                max_first_waiting_time_minutes=1,
                walking_speed_kmh=1,
                with_geojson=True
            )
            self.assertTrue(m.called_once)
            self.assertEqual(res, {"key": "value"})
            self.assertEqual(m.last_request.json(), self.test_accessibility_params)

    def test_request_accessibility_map_error(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/api/accessibility",json={"key": "value"}, status_code=400)
            self.assertRaises(
                requests.exceptions.HTTPError, 
                Transition.request_accessibility_map, 
                coordinates=[0, 0],
                scenario_id="scenario-id",
                departure_or_arrival_choice="Departure",
                departure_or_arrival_time=time(0, 0, 0),
                n_polygons=1,
                delta_minutes=1,
                delta_interval_minutes=1,
                place_name="place",
                max_total_travel_time_minutes=1,
                min_waiting_time_minutes=1,
                max_access_egress_travel_time_minutes=1,
                max_transfer_travel_time_minutes=1,
                max_first_waiting_time_minutes=1,
                walking_speed_kmh=1,
                with_geojson=True
            )
            self.assertTrue(m.called_once)
            self.assertEqual(m.last_request.json(), self.test_accessibility_params)

    def test_request_routing_result(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/api/route", json={"key": "value"}, status_code=200)
            res = Transition.request_routing_result(modes=["mode1", "mode2"], 
                origin=[0, 0], 
                destination=[0, 0], 
                scenario_id="scenario-id", 
                departure_or_arrival_choice="Departure", 
                departure_or_arrival_time=time(0, 0, 0), 
                max_travel_time_minutes=1, 
                min_waiting_time_minutes=1,
                max_transfer_time_minutes=1, 
                max_access_time_minutes=1, 
                max_first_waiting_time_minutes=1,
                with_geojson=True,
                with_alternatives=False
            )
            self.assertTrue(m.called_once)
            self.assertEqual(res, {"key": "value"})
            self.assertEqual(m.last_request.json(), self.test_route_params)

    def test_request_routing_result_error(self):
        with requests_mock.Mocker() as m:
            m.post(f"{self.test_url}/api/route", json={"key": "value"}, status_code=400)
            self.assertRaises(
                requests.exceptions.HTTPError,
                Transition.request_routing_result,
                modes=["mode1", "mode2"], 
                origin=[0, 0], 
                destination=[0, 0], 
                scenario_id="scenario-id", 
                departure_or_arrival_choice="Departure", 
                departure_or_arrival_time=time(0, 0, 0), 
                max_travel_time_minutes=1,
                min_waiting_time_minutes=1,
                max_transfer_time_minutes=1, 
                max_access_time_minutes=1, 
                max_first_waiting_time_minutes=1,
                with_geojson=True,
                with_alternatives=False
            )
            self.assertTrue(m.called_once)
            self.assertEqual(m.last_request.json(), self.test_route_params)

if __name__ == "__main__":
    unittest.main()
        