# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
import warnings
import falcon
import falcon.testing as testing
import ujson


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.lightmlrestapi.testing import dummy_application_auth


class TestDummyAppAuth(testing.TestBase):

    def get_client_api(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=ImportWarning)
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            warnings.filterwarnings('ignore', category=FutureWarning)
            app = dummy_application_auth("zoompwd")
            client = testing.TestClient(app)
        return client

    def test_dummy_app_auth(self):
        client = self.get_client_api()
        bodyin = ujson.dumps({'X': [0.1, 0.2]})
        body = client.simulate_request(
            path='/', method="POST", body=bodyin, protocol='http')
        self.assertIn("HTTPS Required", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_400)
        body = client.simulate_request(
            path='/', method="POST", body=bodyin, protocol='https')
        self.assertIn("token required", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_401)
        body = client.simulate_request(path='/', method="POST", body=bodyin, protocol='https',
                                       headers=dict(uid="me", token="dummy"))
        self.assertIn(body.status, (falcon.HTTP_200, falcon.HTTP_201))
        d = ujson.loads(body.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)

    def test_dummy_error(self):
        client = self.get_client_api()
        bodyin = ujson.dumps({'X': [0.1, 0.2, 0.3]})
        body = client.simulate_request(
            path='/', method="POST", body=bodyin, protocol='http')
        self.assertIn("HTTPS Required", str(body.content))
        body = client.simulate_request(
            path='/', method="POST", body=bodyin, protocol='https')
        self.assertIn("token required", str(body.content))
        self.assertEqual(body.status, falcon.HTTP_401)
        body = client.simulate_request(path='/', method="POST", body=bodyin, protocol='https',
                                       headers=dict(uid="me", token="dummy"))
        self.assertEqual(body.status, falcon.HTTP_400)
        d = ujson.loads(body.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn('X has 3 features per sample; expecting 2', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
