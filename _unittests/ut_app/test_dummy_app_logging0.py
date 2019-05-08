# -*- coding: utf-8 -*-
"""
@brief      test log(time=4s)
"""
import os
import unittest
from datetime import datetime
from pyquickhelper.pycode import ExtTestCase
from lightmlrestapi.mlapp import enumerate_parsed_logs


class TestDummyAppLogging1(ExtTestCase):

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
