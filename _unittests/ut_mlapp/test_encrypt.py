# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""
import unittest
import pandas
from pyquickhelper.pycode import ExtTestCase
from lightmlrestapi.args.encrypt_helper import encrypt_passwords, load_passwords


class TestEncrypt(ExtTestCase):

    def test_encrypt_passwords(self):
        users = [('login', 'pwd'), ('login2', 'pwd2')]
        enc = encrypt_passwords(users)
        self.assertEqual(len(enc), 2)
        self.assertEqual(enc[0][0], users[0][0])
        self.assertIsInstance(enc[0][1], str)

        df = pandas.DataFrame(users, columns=["aa", "bb"])
        df2 = encrypt_passwords(df)
        self.assertEqual(list(df.iloc[:, 0]), list(
            df2.iloc[:, 0].values))  # pylint: disable=E1101
        self.assertEqual(list(df.columns), list(df2.columns))

    def test_load_password(self):
        res = {'a': 'pwd', 'b': 'rrrr'}
        d = load_passwords(res)
        self.assertEqual(res, d)
        t = 'a,pwd\nb,rrrr'
        d = load_passwords(t)
        self.assertEqual(res, d)
        t = [('a', 'pwd'), ('b', 'rrrr')]
        d = load_passwords(t)
        self.assertEqual(res, d)


if __name__ == "__main__":
    unittest.main()
