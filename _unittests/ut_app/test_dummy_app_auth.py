# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""
import base64
import unittest
import warnings
import numpy
import falcon
import falcon.testing as testing  # pylint: disable=R0402
from lightmlrestapi.testing import dummy_application_auth
from lightmlrestapi.tools import json_loads, json_dumps


class TestDummyAppAuth(testing.TestCase):

    def get_client_api(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=ImportWarning)
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            warnings.filterwarnings('ignore', category=FutureWarning)
            app = dummy_application_auth()
            client = testing.TestClient(app)
        return client

    def test_dummy_app_auth(self):
        client = self.get_client_api()
        bodyin = json_dumps({'X': [0.1, 0.2]})
        body = client.simulate_post('/', body=bodyin, protocol='http')
        self.assertIn("HTTPS Required", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_400)
        body = client.simulate_post('/', body=bodyin, protocol='https')
        self.assertIn("Missing Authorization Header", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_401)
        zoo = base64.b64encode("me:dummy".encode('utf-8')).decode('utf-8')
        body = client.simulate_post(path='/', body=bodyin, protocol='https',
                                    headers=dict(Authorization="Basic " + zoo))
        self.assertIn(body.status, (falcon.HTTP_200, falcon.HTTP_201))
        d = json_loads(body.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], (list, numpy.ndarray))
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)

    def test_dummy_error(self):
        client = self.get_client_api()
        bodyin = json_dumps({'X': [0.1, 0.2, 0.3]})
        body = client.simulate_request(
            path='/', method="POST", body=bodyin, protocol='http')
        self.assertIn("HTTPS Required", str(body.content))
        body = client.simulate_post('/', body=bodyin, protocol='https')
        self.assertIn("Missing Authorization Header", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_401)
        zoo = base64.b64encode("me:dummy".encode('utf-8')).decode('utf-8')
        body = client.simulate_post('/', body=bodyin, protocol='https',
                                    headers=dict(Authorization="Basic " + zoo))
        self.assertEqual(body.status, falcon.HTTP_400)
        d = json_loads(body.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn('X has 3 features', d['title'])
        self.assertIn('expecting 2 features', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
