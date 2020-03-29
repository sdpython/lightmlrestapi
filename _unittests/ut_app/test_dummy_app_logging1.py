# -*- coding: utf-8 -*-
"""
@brief      test log(time=4s)
"""
import unittest
import numpy
import falcon
import falcon.testing as testing
from pyquickhelper.pycode import get_temp_folder
from lightmlrestapi.testing import dummy_application
from lightmlrestapi.mlapp import enumerate_parsed_logs
from lightmlrestapi.tools import json_loads, json_dumps


class TestDummyAppLogging1(testing.TestCase):

    def setUp(self):
        super(TestDummyAppLogging1, self).setUp()
        self.temp = get_temp_folder(__file__, 'temp_dummy_app_logging1')
        self.app = dummy_application(
            self.app, secret='dummys', folder=self.temp)

    def test_dummy_app_logging(self):
        bodyin = json_dumps({'X': [0.1, 0.2]})
        result = self.simulate_post('/', body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_201)
        d = json_loads(result.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], (list, numpy.ndarray))
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)
        res = list(enumerate_parsed_logs(self.temp, secret='dummys'))
        self.assertEqual(len(res), 2)
        for _ in range(0, 10):
            body = self.simulate_post(path='/', body=bodyin)
            self.assertEqual(body.status, falcon.HTTP_201)


if __name__ == "__main__":
    unittest.main()
