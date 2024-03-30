import unittest
import requests
from unittest.mock import patch
from datetime import time

from transition_lib.transition_api_lib import Transition as Transition

class TestTransition(unittest.TestCase):
    def setUp(self):
        self.test_url = 'https://example.com'
        self.test_token = 'test_token'
        self.test_username = 'test_username'
        self.test_password = 'test_password'
        self.mock_response = unittest.mock.Mock()

    def test_set_token(self):
        Transition.set_token(self.test_token)
        self.assertEqual(Transition.TOKEN, self.test_token)

    def test_set_url(self):
        Transition.set_url(self.test_url)
        self.assertEqual(Transition.BASE_URL, self.test_url)

    def test_build_body(self):
        body = Transition.build_body(self.test_username, self.test_password)
        self.assertEqual(body, {"usernameOrEmail": self.test_username, "password": self.test_password})

    def test_build_headers(self):
        headers = Transition.build_headers(self.test_token)
        self.assertEqual(headers, {"Authorization": f"Bearer {self.test_token}"})

    # Methods to test :
    # get_token(username, password,url=None)
    # get_paths(url=None, token=None)
    # get_nodes(url=None, token=None)
    # get_scenarios(url=None, token=None)
    # get routing_modes(url=None, token=None)
    # get_accssibility_map(coord_latitude,coord_longitude,scenario_id,departure_or_arrival_choice,
    # departure_or_arrival_time: time, n_polygons, delta_minutes, delta_interval_minutes, place_name,
    # max_total_travel_time_minutes, min_waiting_time_minutes, max_access_egress_travel_time_minutes, max_transfer_travel_time_minutes,
    # max_first_waiting_time_minutes, walking_speed_kmh, with_geojson, url=None, token=None):
        
    # get_routing_result(modes, origin, destination, scenario_id, departure_or_arrival_choice, departure_or_arrival_time, 
    # max_travel_time, min_waiting_time, max_transfer_time, max_access_time, max_first_waiting_time,with_geojson, url=None, token=None):
        
    @patch('transition_lib.transition_api_lib.requests.post')
    def test_get_token(self, mock_post):
        self.mock_response.raise_for_status.return_value = None
        self.mock_response.text = self.test_token
        mock_post.return_value = self.mock_response

        token = Transition.get_token(self.test_username, self.test_password, self.test_url)
        self.assertEqual(token, self.test_token)
        mock_post.assert_called_once_with(
            f'{self.test_url}/token',
            json={'usernameOrEmail': self.test_username, 'password': self.test_password}
        )
        
    @patch('transition_lib.transition_api_lib.requests.get')
    def test_get_paths(self, mock_get):
        self.mock_response.raise_for_status.return_value = None
        mock_get.return_value = self.mock_response

        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)
        Transition.get_paths()
        mock_get.assert_called_once_with(
            f'{self.test_url}/api/paths',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )

    @patch('transition_lib.transition_api_lib.requests.get')
    def test_get_nodes(self, mock_get):
        self.mock_response.raise_for_status.return_value = None
        mock_get.return_value = self.mock_response

        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)
        Transition.get_nodes()
        mock_get.assert_called_once_with(
            f'{self.test_url}/api/nodes',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )

    @patch('transition_lib.transition_api_lib.requests.get')
    def test_get_scenarios(self, mock_get):
        self.mock_response.raise_for_status.return_value = None
        mock_get.return_value = self.mock_response

        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)
        Transition.get_scenarios()
        mock_get.assert_called_once_with(
            f'{self.test_url}/api/scenarios',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )

    @patch('transition_lib.transition_api_lib.requests.get')
    def test_get_routing_modes(self, mock_get):
        self.mock_response.raise_for_status.return_value = None
        self.mock_response.text = '["mode1","mode2"]'
        mock_get.return_value = self.mock_response

        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)
        modes = Transition.get_routing_modes()
        self.assertEqual(modes, ['mode1', 'mode2'])
        mock_get.assert_called_once_with(
            f'{self.test_url}/api/routing-modes',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )

    @patch('transition_lib.transition_api_lib.requests.post')
    def test_get_accessibility_map(self, mock_get):
        self.mock_response.raise_for_status.return_value = None
        mock_get.return_value = self.mock_response
        departure_time = time(0, 0, 0)

        Transition.set_url(self.test_url)
        Transition.set_token(self.test_token)
        Transition.get_accessibility_map(0, 0, 0, 'departure', departure_time, 1, 1, 1, 'place', 1, 1, 1, 1, 1, 1, True)
        mock_get.assert_called_once_with(
            f'{self.test_url}/api/accessibility',
            headers={'Authorization': f'Bearer {self.test_token}'}
        )


if __name__ == '__main__':
    unittest.main()
        