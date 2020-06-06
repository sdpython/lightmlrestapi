# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import os
import unittest
import falcon
import falcon.testing as testing
import ujson
from lightmlrestapi.testing import dummy_application_neighbors_image
from lightmlrestapi.testing.data import get_wiki_img
from lightmlrestapi.args import image2base64, image2array, base642image


class TestDummyAppSearchImg(testing.TestCase):

    def setUp(self):
        super(TestDummyAppSearchImg, self).setUp()
        self.app = dummy_application_neighbors_image(self.app)

    def test_dummy_search_app_search_img(self):
        # With a different image than the original.
        img2 = os.path.join(os.path.dirname(__file__),
                            "data", "wiki_modified.png")
        b64 = image2base64(img2)[1]
        try:
            bodyin = ujson.dumps({'X': b64}, reject_bytes=False)
        except TypeError as e:
            raise AssertionError(
                "Issue with type '{}'.".format(type(b64))) from e
        body = self.simulate_post('/', body=bodyin)
        if body.status != falcon.HTTP_201:
            res = ujson.loads(body)
            raise Exception("Failure\n{0}".format(res))
        self.assertEqual(body.status, falcon.HTTP_201)
        d = ujson.loads(body.content)
        self.assertTrue('Y' in d)
        self.assertIsInstance(d['Y'], list)
        self.assertEqual(len(d['Y']), 1)
        self.assertEqual(len(d['Y'][0]), 1)
        self.assertEqual(d['Y'][0][0][0], 0)
        self.assertGreater(d['Y'][0][0][1], 0.21)
        self.assertEqual(d['Y'][0][0][2], {
                         'description': 'image from wikipedia: 114064', 'name': 'wiki.png'})

    def test_dummy_error_img(self):
        img = get_wiki_img()
        ext_b64 = image2base64(img)
        img2 = base642image(ext_b64[1])
        arr = image2array(img2)
        bodyin = ujson.dumps({'X': arr.tolist()})

        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        d = ujson.loads(body.content)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn(
            "argument should be a bytes-like object or ASCII string, not 'list'", d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
