# -*- coding: utf-8 -*-
"""
@brief      test log(time=4s)
"""
import unittest
import falcon
import falcon.testing as testing
import ujson
from lightmlrestapi.testing import dummy_application_neighbors


class TestDummyAppSearch(testing.TestCase):

    def setUp(self):
        super(TestDummyAppSearch, self).setUp()
        self.app = dummy_application_neighbors(self.app)

    def test_dummy_app_search(self):
        bodyin = ujson.dumps({'X': [0.1, 0.2]})
        result = self.simulate_post('/', body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_201)
        d = ujson.loads(result.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 5)

    def test_dummy_error_search(self):
        bodyin = ujson.dumps({'X': [0.1, 0.2, 0.3]})
        result = self.simulate_post('/', body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_400)
        d = ujson.loads(result.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn(
            'query data dimension must match training data dimension', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
