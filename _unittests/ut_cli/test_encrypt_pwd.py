"""
@brief      test tree node (time=8s)
"""


import sys
import os
import unittest

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


from src.lightmlrestapi.cli.encrypt_pwd import _encrypt_pwd


class TestEncryptPwd(unittest.TestCase):

    def test_encrypt_pwd(self):
        rows = []

        def flog(*l):
            rows.append(l)

        _encrypt_pwd(args=['-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: encrypt_pwd [-h] [-i INPUT] [-o OUTPUT] [-s SECRET]"):
            raise Exception(r)


if __name__ == "__main__":
    unittest.main()
