"""
@brief      test tree node (time=8s)
"""


import sys
import os
import unittest
from pyquickhelper.pycode import get_temp_folder, ExtTestCase

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


from src.lightmlrestapi.cli.make_ml_store import start_mlreststor
from src.lightmlrestapi.__main__ import main


class TestStartMlRestApiStore(ExtTestCase):

    def test_start_mlreststor_help(self):
        rows = []

        def flog(*l):
            rows.append(l)

        main(args=['start_mlreststor', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: start_mlreststor [-h] [-l LOCATION]"):
            raise Exception(r)

    def test_start_mlreststor(self):
        rows = []

        def flog(*li):
            rows.append(" ".join(str(_) for _ in li))

        temp = get_temp_folder(__file__, "temp_start_mlreststor")
        app = start_mlreststor(location=temp, nostart=True, fLOG=flog)
        self.assertNotEmpty(app)
        log = "\n".join(rows)
        self.assertIn("[start_mlreststor] do not run serve", log)


if __name__ == "__main__":
    unittest.main()
