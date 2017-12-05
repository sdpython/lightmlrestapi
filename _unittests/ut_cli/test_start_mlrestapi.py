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


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..", "..", "pyquickhelper", "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


from pyquickhelper.loghelper import fLOG
from src.lightmlrestapi.cli.make_ml_app import _start_mlrestapi


class TestStartMlRestApi(unittest.TestCase):

    def test_start_mlrestapi(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*l):
            rows.append(l)

        _start_mlrestapi(args=['-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: start_mlrestapi [-h] [-n NAME] [-ho HOST]"):
            raise Exception(r)

    def test_start_mlrestapi_notstart(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*l):
            rows.append(l)

        _start_mlrestapi(args=['--nostart=True'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)

    def test_start_mlrestapi_notstart_image(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*l):
            rows.append(l)

        _start_mlrestapi(args=['--nostart=True', '--name=dummyimg'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)

    def test_start_mlrestapi_notstart_neighobrs_image(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*l):
            rows.append(l)

        _start_mlrestapi(args=['--nostart=True', '--name=dummyknnimg'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)


if __name__ == "__main__":
    unittest.main()
