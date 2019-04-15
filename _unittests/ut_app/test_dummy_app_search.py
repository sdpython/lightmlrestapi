# -*- coding: utf-8 -*-
"""
@brief      test log(time=4s)
"""
import unittest
import falcon
import falcon.testing as testing
import ujson
from lightmlrestapi.testing import dummy_application_neighbors


class TestDummyAppSearch(testing.TestBase):

    def before(self):
        dummy_application_neighbors(self.api)

    def test_dummy_app_search(self):
        bodyin = ujson.dumps({'X': [0.1, 0.2]})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 5)

    def test_dummy_error_search(self):
        bodyin = ujson.dumps({'X': [0.1, 0.2, 0.3]})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        d = ujson.loads(body)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn(
            'query data dimension must match training data dimension', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
