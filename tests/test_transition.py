import unittest
import requests

from transition_lib.transition_api_lib import Transition as Transition

class TestTransition(unittest.TestCase):
    def test_set_token(self):
        token = "test_token"
        Transition.set_token(token)
        self.assertEqual(Transition.TOKEN, token)

    def test_set_url(self):
        url = "test_url"
        Transition.set_url(url)
        self.assertEqual(Transition.BASE_URL, url)

    def test_build_body(self):
        username = "test_username"
        password = "test_password"
        body = Transition.build_body(username, password)
        self.assertEqual(body, {"usernameOrEmail": username, "password": password})

    def test_build_headers(self):
        token = "test_token"
        headers = Transition.build_headers(token)
        self.assertEqual(headers, {"Authorization": f"Bearer {token}"})

        