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


class TestDummyAppLogging2(testing.TestCase):

    def setUp(self):
        super(TestDummyAppLogging2, self).setUp()
        self.temp = get_temp_folder(__file__, 'temp_dummy_app_logging2')
        self.app = dummy_application(
            self.app, secret='dummys', folder=self.temp)

    def test_dummy_app_logging_nosecret(self):
        temp = get_temp_folder(__file__, 'temp_dummy_app_logging_nosecret')
        self.app = dummy_application(secret=None, folder=temp)

        bodyin = json_dumps({'X': [0.1, 0.2]})
        result = self.simulate_post('/', body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_201)
        d = json_loads(result.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], (list, numpy.ndarray))
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)
        res = list(enumerate_parsed_logs(temp, secret=None))
        self.assertEqual(len(res), 2)
        for r in res:
            self.assertIn('dt', r)
            self.assertIn('code', r)
            self.assertIn('data', r)
        for _ in range(0, 10):
            result = self.simulate_post('/', body=bodyin)
            self.assertEqual(result.status, falcon.HTTP_201)


if __name__ == "__main__":
    unittest.main()
