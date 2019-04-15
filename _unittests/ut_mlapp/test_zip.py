# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from lightmlrestapi.args.zip_helper import unzip_bytes, zip_dict


class TestZip(ExtTestCase):

    def test_zip(self):
        data = dict(one=b"1", two=b"2")
        u = zip_dict(data)
        b = unzip_bytes(u)
        self.assertEqual(data, b)


if __name__ == "__main__":
    unittest.main()
