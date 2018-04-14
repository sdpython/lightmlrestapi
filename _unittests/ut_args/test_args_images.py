# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""

import sys
import os
import unittest
import falcon.testing as testing


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
from src.lightmlrestapi.args import image2base64, base642image, image2array
from src.lightmlrestapi.testing.data import get_wiki_img


class TestArgsImages(testing.TestBase):

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
