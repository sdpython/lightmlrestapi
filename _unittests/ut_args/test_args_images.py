# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import unittest
import falcon.testing as testing
from pyquickhelper.loghelper import fLOG
from lightmlrestapi.args import image2base64, base642image, image2array
from lightmlrestapi.testing.data import get_wiki_img


class TestArgsImages(testing.TestCase):

    def test_dummy_app(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        img = get_wiki_img()
        ext, b64 = image2base64(img)
        self.assertEqual(ext, "image/png")
        img = base642image(b64)
        size = img.size
        self.assertEqual(size, (456, 415))
        arr = image2array(img)
        self.assertEqual(arr.shape, (415, 456, 3))


if __name__ == "__main__":
    unittest.main()
