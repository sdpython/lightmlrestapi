# -*- coding: utf-8 -*-
"""
@brief      test log(time=5s)
"""
import os
import unittest
import falcon
import falcon.testing as testing
from PIL import Image
import ujson
from lightmlrestapi.testing import dummy_application_image
from lightmlrestapi.testing.data import get_wiki_img
from lightmlrestapi.testing.dummy_applications import _distance_img
from lightmlrestapi.args import image2base64, image2array, base642image


class TestDummyAppImg(testing.TestCase):

    def setUp(self):
        super(TestDummyAppImg, self).setUp()
        self.app = dummy_application_image(self.app)

    def test_dummy_app_img(self):
        # With a different image than the original.
        img2 = os.path.join(os.path.dirname(__file__),
                            "data", "wiki_modified.png")
        b64 = image2base64(img2)[1]
        bodyin = ujson.dumps({'X': b64}, reject_bytes=False)
        result = self.simulate_post('/', body=bodyin)
        if result.status != falcon.HTTP_201:
            res = ujson.loads(result.content)
            raise Exception("Failure\n{0}".format(res))
        self.assertEqual(result.status, falcon.HTTP_201)
        d = ujson.loads(result.content)
        self.assertTrue('Y' in d)
        self.assertGreater(d['Y'], 0.21)

        # With the same image.
        img = get_wiki_img()
        ext_b64 = image2base64(img)

        bodyin = ujson.dumps({'X': ext_b64[1]}, reject_bytes=False)
        result = self.simulate_post('/', body=bodyin)
        if result.status != falcon.HTTP_201:
            res = ujson.loads(result.content)
            raise Exception("Failure\n{0}".format(res))
        self.assertEqual(result.status, falcon.HTTP_201)
        d = ujson.loads(result.content)
        self.assertTrue('Y' in d)
        self.assertEqual(d['Y'], 0)

    def test_dummy_error_img(self):
        img = get_wiki_img()
        ext_b64 = image2base64(img)
        img2 = base642image(ext_b64[1])
        arr = image2array(img2)
        bodyin = ujson.dumps({'X': arr.tolist()})
        result = self.simulate_post('/', body=bodyin)
        self.assertEqual(result.status, falcon.HTTP_400)
        d = ujson.loads(result.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn(
            "argument should be a bytes-like object or ASCII string, not 'list'", d['title'])
        self.assertIn('.py', d['description'])

    def test_image_distance(self):
        img1 = os.path.join(os.path.dirname(__file__), "data", "white.png")
        img2 = os.path.join(os.path.dirname(__file__), "data", "black.png")
        i1 = Image.open(img1).convert('RGB')
        i2 = Image.open(img2).convert('RGB')
        d = _distance_img(i1, i2)
        self.assertEqual(d, 1)


if __name__ == "__main__":
    unittest.main()
