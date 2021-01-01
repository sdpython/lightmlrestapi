"""
@brief      test tree node (time=8s)
"""
import unittest
from pyquickhelper.loghelper import fLOG
from lightmlrestapi.__main__ import main


class TestStartMlRestApi(unittest.TestCase):

    def test_start_mlrestapi(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['start_mlrestapi', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: start_mlrestapi"):
            raise Exception(r)

    def test_start_mlrestapi_notstart(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['start_mlrestapi', '--nostart=True'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)

    def test_start_mlrestapi_notstart_image(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['start_mlrestapi', '--nostart=True',
                   '--name=dummyimg'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)

    def test_start_mlrestapi_notstart_neighobrs_image(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['start_mlrestapi', '--nostart=True', '--name=dummyknnimg'],
             fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)


if __name__ == "__main__":
    unittest.main()
