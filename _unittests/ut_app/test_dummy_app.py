# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import unittest
import numpy
import falcon
import falcon.testing as testing
from pyquickhelper.loghelper import fLOG
from lightmlrestapi.testing import dummy_application
from lightmlrestapi.tools import json_loads, json_dumps


class TestDummyApp(testing.TestCase):

    def setUp(self):
        super(TestDummyApp, self).setUp()
        self.app = dummy_application(self.app)

    def test_dummy_app(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        bodyin = json_dumps({'X': [0.1, 0.2]})
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_201)
        d = json_loads(body.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], (list, numpy.ndarray))
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)

    def test_dummy_error(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        bodyin = json_dumps({'X': [0.1, 0.2, 0.3]})
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        d = json_loads(body.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn('X has 3 features per sample; expecting 2', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
