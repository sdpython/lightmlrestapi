# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
from datetime import datetime
import falcon
import falcon.testing as testing
from pyquickhelper.pycode import get_temp_folder
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

from src.lightmlrestapi.testing import dummy_application
from src.lightmlrestapi.mlapp import enumerate_parsed_logs


class TestDummyAppLogging(testing.TestBase):

    def test_dummy_app_logging(self):
        temp = get_temp_folder(__file__, 'temp_dummy_app_logging')
        dummy_application(self.api, secret='dummys', folder=temp)

        bodyin = ujson.dumps({'X': [0.1, 0.2]})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)
        res = list(enumerate_parsed_logs(temp, secret='dummys'))
        self.assertEqual(len(res), 2)
        for _ in range(0, 10):
            body = self.simulate_request(
                '/', decode='utf-8', method="POST", body=bodyin)
            self.assertEqual(self.srmock.status, falcon.HTTP_201)

    def test_parsed_logs(self):
        data = os.path.join(os.path.dirname(__file__), 'data', 'logs')
        res = list(enumerate_parsed_logs(data, 'dummys'))
        self.assertEqual(len(res), 1)
        rec = res[0]
        self.assertIn('dt', rec)
        data = res[0]['data']
        self.assertIsInstance(rec['dt'], datetime)
        self.assertEqual(data['X'], [0.1, 0.2])
        self.assertEqual(data['Y'], {'shape': [1, 3],
                                     'data': [[0.499421617904304, 0.4514893598914066, 0.04908902220428942]]})


if __name__ == "__main__":
    unittest.main()
