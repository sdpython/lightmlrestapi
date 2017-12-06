#-*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""

import sys
import os
import unittest
import ujson
import falcon
import falcon.testing as testing
from PIL import Image


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


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

from pyquickhelper.loghelper import fLOG
from src.lightmlrestapi.testing import dummy_application_image
from src.lightmlrestapi.testing.data import get_wiki_img
from src.lightmlrestapi.testing.dummy_applications import _distance_img
from src.lightmlrestapi.args import image2base64, image2array, base642image


class TestDummyAppImg(testing.TestBase):

    def before(self):
        dummy_application_image(self.api)

    def test_dummy_app_img(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        # With a different image than the original.
        img2 = os.path.join(os.path.dirname(__file__),
                            "data", "wiki_modified.png")
        b64 = image2base64(img2)[1]
        bodyin = ujson.dumps({'X': b64})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        if self.srmock.status != falcon.HTTP_201:
            res = ujson.loads(body)
            raise Exception("Failure\n{0}".format(res))
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertGreater(d['Y'][0], 0.21)

        # With the same image.
        img = get_wiki_img()
        ext_b64 = image2base64(img)

        bodyin = ujson.dumps({'X': ext_b64[1]})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        if self.srmock.status != falcon.HTTP_201:
            res = ujson.loads(body)
            raise Exception("Failure\n{0}".format(res))
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(d['Y'][0], 0)

    def test_dummy_error_img(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        img = get_wiki_img()
        ext_b64 = image2base64(img)
        img2 = base642image(ext_b64[1])
        arr = image2array(img2)
        bodyin = ujson.dumps({'X': arr.tolist()})

        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        d = ujson.loads(body)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn("argument should be a bytes-like object or ASCII string, not 'list'", d['title'])
        self.assertIn('.py', d['description'])

    def test_image_distance(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        img1 = os.path.join(os.path.dirname(__file__), "data", "white.png")
        img2 = os.path.join(os.path.dirname(__file__), "data", "black.png")
        i1 = Image.open(img1).convert('RGB')
        i2 = Image.open(img2).convert('RGB')
        d = _distance_img(i1, i2)
        self.assertEqual(d, 1)


if __name__ == "__main__":
    unittest.main()
