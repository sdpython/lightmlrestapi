# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase


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

from src.lightmlrestapi.args.zip_helper import unzip_bytes, zip_dict


class TestZip(ExtTestCase):

    def test_zip(self):
        data = dict(one=b"1", two=b"2")
        u = zip_dict(data)
        b = unzip_bytes(u)
        self.assertEqual(data, b)


if __name__ == "__main__":
    unittest.main()
