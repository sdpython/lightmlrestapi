# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""

import sys
import os
import unittest
import pandas
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

from src.lightmlrestapi.mlapp.encrypt_helper import encrypt_passwords


class TestEncrypt(ExtTestCase):

    def test_encrypt_passwords(self):
        users = [('login', 'pwd'), ('login2', 'pwd2')]
        enc = encrypt_passwords(users, "zoo")
        self.assertEqual(len(enc), 2)
        self.assertEqual(enc[0][0], users[0][0])
        self.assertIsInstance(enc[0][1], str)

        df = pandas.DataFrame(users, columns=["aa", "bb"])
        df2 = encrypt_passwords(df, "zoo")
        self.assertEqual(list(df.iloc[:, 0]), list(
            df2.iloc[:, 0].values))  # pylint: disable=E1101
        self.assertEqual(list(df.columns), list(df2.columns))


if __name__ == "__main__":
    unittest.main()
