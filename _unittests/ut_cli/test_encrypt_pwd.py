"""
@brief      test tree node (time=8s)
"""
import os
import unittest
import pandas
from pyquickhelper.loghelper import noLOG
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from lightmlrestapi.cli.make_encrypt_pwd import encrypt_pwd
from lightmlrestapi.__main__ import main


class TestEncryptPwd(ExtTestCase):

    def test_encrypt_pwd(self):
        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['encrypt_pwd', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: encrypt_pwd [-h] [-i INPUT] [-o OUTPUT] [-a ALGO]"):
            raise Exception(r)

    def test_encrypt_pwd2(self):
        temp = get_temp_folder(__file__, "temp_encrypt_pwd")
        pwd = os.path.join(temp, "pwd.txt")
        enc = os.path.join(temp, "pwd.txt")
        name = "xavier,pwdxavier"
        with open(pwd, "w", encoding="utf-8") as f:
            f.write(name)
        encrypt_pwd(pwd, enc, fLOG=noLOG)
        df = pandas.read_csv(enc, header=None)
        self.assertEqual(df.iloc[0, 0], "xavier")
        self.assertEqual(
            df.iloc[0, 1], "85155e3fb5c95d483d5508d41ca9abbb9a09c4e4468b31e3b805021e")


if __name__ == "__main__":
    unittest.main()
