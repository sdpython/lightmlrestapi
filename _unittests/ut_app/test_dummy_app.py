# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import unittest
import falcon
import falcon.testing as testing
import ujson
from pyquickhelper.loghelper import fLOG
from lightmlrestapi.testing import dummy_application


class TestDummyApp(testing.TestCase):

    def setUp(self):
        super(TestDummyApp, self).setUp()
        self.app = dummy_application(self.app)

    def test_dummy_app(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        bodyin = ujson.dumps({'X': [0.1, 0.2]})
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_201)
        d = ujson.loads(body.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 3)

    def test_dummy_error(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        bodyin = ujson.dumps({'X': [0.1, 0.2, 0.3]})
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        d = ujson.loads(body.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn('X has 3 features per sample; expecting 2', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
